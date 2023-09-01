import os
import re
import polars as pl
import polars.selectors as cs
from pathlib import Path
from tqdm.notebook import tqdm
from .. import config as cfg
from ..utils import has_gpu
from ..data_processing import feature_aggregation as fa
from ..database.queries import (
    experiment_metadata_sql_query,
    plate_layout_sql_query,
)
from ..logger import (
    log_info,
    log_warning,
)


def get_cell_morphology_ref(
    name: str,
    filter: dict = None,
):
    query = experiment_metadata_sql_query(
        name,
        cfg.DATABASE_SCHEMA,
        cfg.CELL_MORPHOLOGY_METADATA_TYPE,
    )
    df = pl.read_database(query, cfg.DB_URI)

    if filter is None:
        return df
    conditions = []
    # Iterate over each key-value pair in the filter dictionary
    for key, values in filter.items():
        # Create an OR condition for each value associated with a key
        key_conditions = [pl.col(key).str.contains(val) for val in values]
        combined_key_condition = key_conditions[0]
        for condition in key_conditions[1:]:
            combined_key_condition = combined_key_condition | condition
        conditions.append(combined_key_condition)
    # Combine all conditions with AND
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition = final_condition & condition
    # Apply the condition to the DataFrame
    return df.filter(final_condition)


def get_cell_morphology_data(
    cell_morphology_ref_df: pl.DataFrame,
    aggregation_level="cell",
    aggregation_method=None,
    path_to_save: str = "data",
    use_gpu=False,
):
    if aggregation_method is None:
        aggregation_method = {
            "cell": "median",
            "site": "median",
            "well": "median",
            "plate": "mean",
            "compound": "mean",
        }
    object_file_names = cfg.OBJECT_FILE_NAMES
    plate_acq_id = cfg.DATABASE_SCHEMA["EXPERIMENT_PLATE_ACQID_COLUMN"]
    plate_acq_name = cfg.DATABASE_SCHEMA["EXPERIMENT_PLATE_AQNAME_COLUMN"]

    # Create output directory if it doesn't exist
    saving_dir = Path(path_to_save)
    saving_dir.mkdir(parents=True, exist_ok=True)

    # Set up progress bar for feedback
    total_iterations = cell_morphology_ref_df.height * len(object_file_names)
    progress_bar = tqdm(total=total_iterations, desc="Processing")

    all_dataframes = []

    for index, plate_metadata in enumerate(
        cell_morphology_ref_df.iter_rows(named=True)
    ):
        # Print separator and progress info
        separator = "\n" if index else ""
        log_info(
            (
                f"{separator}{'_'*50}"
                f"\nProcessing plate {plate_metadata[plate_acq_name]} ({index + 1} of {cell_morphology_ref_df.height}):"
            )
        )

        # Define and check for existing output files
        output_filename = f"{saving_dir}/{plate_metadata[plate_acq_id]}_{plate_metadata[plate_acq_name]}.parquet"
        if os.path.exists(output_filename):
            log_info(f"File already exists, reading data from: {output_filename}")
            existing_df = pl.read_parquet(output_filename)
            all_dataframes.append(existing_df)
            progress_bar.update(len(object_file_names))
            continue

        # Load and process feature datasets
        object_feature_dataframes = {}
        unusful_col_pattern = r"^(FileName|PathName|ImageNumber|Number_Object_Number)"

        for object_file_name in object_file_names:
            object_feature_file_path = f"{plate_metadata[cfg.DATABASE_SCHEMA['EXPERIMENT_RESULT_DIRECTORY_COLUMN']]}{object_file_name}.parquet"

            # Read the parquet file and adjust column names
            columns_names = pl.scan_parquet(object_feature_file_path).columns
            object_feature_df = pl.read_parquet(
                object_feature_file_path,
                columns=[
                    col
                    for col in columns_names
                    if not re.match(unusful_col_pattern, col)
                ],
            ).rename({"ObjectNumber": "id"})
            object_name = object_file_name.split("_")[-1]
            object_feature_df.columns = [
                f"{col}_{object_name}" for col in object_feature_df.columns
            ]

            object_feature_dataframes[object_name] = object_feature_df
            log_info(
                f"\tReading features {object_feature_df.shape} - {object_name}: \t{object_feature_file_path}"
            )

            progress_bar.update(1)

        log_info("Merging the data")
        # Join nuclei and cell data on specified columns
        df_combined = object_feature_dataframes["cells"].join(
            object_feature_dataframes["nuclei"],
            left_on=[
                "Metadata_AcqID_cells",
                "Metadata_Barcode_cells",
                "Metadata_Well_cells",
                "Metadata_Site_cells",
                "id_cells",
            ],
            right_on=[
                "Metadata_AcqID_nuclei",
                "Metadata_Barcode_nuclei",
                "Metadata_Well_nuclei",
                "Metadata_Site_nuclei",
                "Parent_cells_nuclei",
            ],
            how="left",
            suffix="_nuclei",
        )

        # Further join with cytoplasm data on specified columns
        df_combined = df_combined.join(
            object_feature_dataframes["cytoplasm"],
            left_on=[
                "Metadata_AcqID_cells",
                "Metadata_Barcode_cells",
                "Metadata_Well_cells",
                "Metadata_Site_cells",
                "id_cells",
            ],
            right_on=[
                "Metadata_AcqID_cytoplasm",
                "Metadata_Barcode_cytoplasm",
                "Metadata_Well_cytoplasm",
                "Metadata_Site_cytoplasm",
                "Parent_cells_cytoplasm",
            ],
            how="left",
            suffix="_cytoplasm",
        )

        # Renaming columns for better consistency
        rename_map = {
            "Metadata_AcqID_cells": "Metadata_AcqID",
            "Metadata_Barcode_cells": "Metadata_Barcode",
            "Metadata_Well_cells": "Metadata_Well",
            "Metadata_Site_cells": "Metadata_Site",
            "Children_cytoplasm_Count_cells": "Cell_cytoplasm_count",
            "Children_nuclei_Count_cells": "Cell_nuclei_count",
        }
        df_combined = df_combined.rename(rename_map)

        # Create ImageID column by concatenating other columns
        image_id = (
            df_combined["Metadata_AcqID"]
            + "_"
            + df_combined["Metadata_Barcode"]
            + "_"
            + df_combined["Metadata_Well"]
            + "_"
            + df_combined["Metadata_Site"]
        ).alias("ImageID")
        df_combined = df_combined.with_columns([image_id])

        # Create CellID column by concatenating other columns
        cell_id = (df_combined["ImageID"] + "_" + df_combined["id_cells"]).alias(
            "CellID"
        )
        df_combined = df_combined.with_columns([cell_id])

        drop_map = [
            "Children_cytoplasm_Count_nuclei",
            "Parent_precells_cells",
            "Parent_nuclei_cytoplasm",
            "id_cells",
            "id_nuclei",
            "id_cytoplasm",
        ]
        df_combined = df_combined.drop(drop_map)

        # Ensure data type consistency for certain columns
        cast_cols = [
            pl.col("Metadata_AcqID").cast(pl.Utf8),
            pl.col("Metadata_Site").cast(pl.Utf8),
        ]
        df_combined = df_combined.with_columns(cast_cols)

        # ordering the columns

        morphology_feature_cols = df_combined.select(
            cs.by_dtype(pl.NUMERIC_DTYPES)
        ).columns
        morphology_feature_cols.remove("Cell_nuclei_count")
        morphology_feature_cols.remove("Cell_cytoplasm_count")
        non_numeric_cols = df_combined.select(cs.by_dtype(pl.Utf8)).columns
        new_order = (
            sorted(non_numeric_cols)
            + ["Cell_nuclei_count", "Cell_cytoplasm_count"]
            + morphology_feature_cols
        )

        df_combined = df_combined.select(new_order)

        barcode_list = df_combined["Metadata_Barcode"].unique().to_list()
        barcode_str = ", ".join([f"'{item}'" for item in barcode_list])

        query = plate_layout_sql_query(cfg.DATABASE_SCHEMA, barcode_str)

        df_plates = pl.read_database(query, cfg.DB_URI)

        # Join data with df_plates
        df_combined = df_combined.join(
            df_plates,
            how="left",
            left_on=["Metadata_Barcode", "Metadata_Well"],
            right_on=["barcode", "well_id"],
        )
        aggregated_data = df_combined.drop_nulls(subset="batch_id")

        # Mapping of aggregation levels to their grouping columns
        grouping_columns_map = {
            "cell": [
                "CellID",
                "ImageID",
                "Metadata_AcqID",
                "Metadata_Barcode",
                "Metadata_Well",
                "Metadata_Site",
                "batch_id",
            ],
            "site": [
                "ImageID",
                "Metadata_AcqID",
                "Metadata_Barcode",
                "Metadata_Well",
                "Metadata_Site",
                "batch_id",
            ],
            "well": ["Metadata_AcqID", "Metadata_Barcode", "Metadata_Well", "batch_id"],
            "plate": ["Metadata_AcqID", "Metadata_Barcode", "batch_id"],
            "compound": ["batch_id"],
        }
        
        if use_gpu and not has_gpu():
            raise EnvironmentError("GPU is not available on this machine. Install NVIDIA System Management Interface (nvidia-smi) to enable this check.")

        # Iterate over the levels and aggregate data progressively
        for level in ["cell", "site", "well", "plate", "compound"]:
            aggregation_func = fa.aggregate_morphology_data_gpu if use_gpu else fa.aggregate_morphology_data_cpu
            aggregated_data = aggregation_func(
                df=aggregated_data,
                columns_to_aggregate=morphology_feature_cols,
                groupby_columns=grouping_columns_map[level],
                aggregation_function=aggregation_method[level],
            )
            if aggregation_level == level:
                break

        # Write the aggregated data to a parquet file
        aggregated_data.write_parquet(output_filename)
        all_dataframes.append(aggregated_data)

    progress_bar.close()

    return (
        pl.concat(all_dataframes)
        if len(all_dataframes) > 1
        else all_dataframes[0]
    )
