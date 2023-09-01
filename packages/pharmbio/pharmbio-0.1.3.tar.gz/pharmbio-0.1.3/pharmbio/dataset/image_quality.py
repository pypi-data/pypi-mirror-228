import polars as pl
from typing import Union, List
from .. import config as cfg
from ..config import DATABASE_SCHEMA

from ..logger import (
    log_info,
    log_warning,
)

from ..database.queries import (
    experiment_metadata_sql_query,
)

from ..utils import (
    get_file_extension,
    read_file,
)


def get_image_quality_ref(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None,
):  # sourcery skip: low-code-quality
    query = experiment_metadata_sql_query(
        name, DATABASE_SCHEMA, cfg.IMAHGE_QUALITY_METADATA_TYPE
    )
    image_quality_reference = pl.read_database(query, cfg.DB_URI)
    data_dict = (
        image_quality_reference.select(
            [
                DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"],
                DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"],
            ]
        )
        .groupby(DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"])
        .agg(pl.col(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]))
        .to_dicts()
    )
    unique_project_count = image_quality_reference.unique(
        DATABASE_SCHEMA["EXPERIMENT_NAME_COLUMN"]
    ).height

    if unique_project_count == 0:
        message = f"Quering the db for {name} returned nothing."
    elif unique_project_count > 1:
        message = (
            f"Quering the db for {name} found {unique_project_count} studies: "
            f"{image_quality_reference.unique(DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN'])[DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN']].to_list()}"
        )
    else:
        message = (
            f"Quering the db for {name} found {unique_project_count} study: "
            f"{image_quality_reference.unique(DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN'])[DATABASE_SCHEMA['EXPERIMENT_NAME_COLUMN']].to_list()}"
        )
    log_info(f"{message}\n{'_'*50}")

    if unique_project_count != 0:
        for i, study in enumerate(data_dict, start=1):
            log_info(i)
            for value in study.values():
                log_info("\t" + str(value))
    log_info("\n" + "_" * 50)

    grouped_replicates = image_quality_reference.groupby(
        DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]
    )

    for plate_name, group in grouped_replicates:
        if len(group) > 1:
            log_warning(
                (
                    f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with "
                    f"{DATABASE_SCHEMA['EXPERIMENT_ANALYSIS_ID_COLUMN']} of {sorted(group[DATABASE_SCHEMA['EXPERIMENT_ANALYSIS_ID_COLUMN']].to_list())}"
                )
            )
    if image_quality_reference.filter(
        pl.col(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]).is_duplicated()
    ).is_empty():
        log_info("No replicated analysis has been found!")
    if drop_replication == "Auto" and keep_replication == "None":
        # keeping the highest analysis_id value of replicated rows
        image_quality_reference = (
            image_quality_reference.sort(
                DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"], descending=True
            )
            .unique(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"], keep="first")
            .sort(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"])
        )
    elif isinstance(drop_replication, list):
        # drop rows by analysis_id
        image_quality_reference = image_quality_reference.filter(
            ~pl.col(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"]).is_in(
                drop_replication
            )
        )
    elif isinstance(keep_replication, list):
        # keep rows by analysis_id
        image_quality_reference = image_quality_reference.filter(
            pl.col(DATABASE_SCHEMA["EXPERIMENT_ANALYSIS_ID_COLUMN"]).is_in(
                keep_replication
            )
        )

    if filter is None:
        return image_quality_reference
    
    conditions = []
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
    return image_quality_reference.filter(final_condition)


def get_image_quality_data(
    filtered_image_quality_info: pl.DataFrame,
    force_merging_columns: Union[bool, str] = False,
):
    # Add image_quality_data_file column based on RESULT_DIRECTORY_COLUMN and PLATE_BARCODE_COLUMN
    filtered_image_quality_info = filtered_image_quality_info.with_columns(
        (
            pl.col(DATABASE_SCHEMA["EXPERIMENT_RESULT_DIRECTORY_COLUMN"])
            + cfg.IMAGE_QUALITY_FILE_PREFIX
            + pl.col(DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"])
        ).alias("image_quality_data_file")
    )
    log_info("\n")
    # Read and process all the files in a list, skipping files not found
    dfs = []
    for row in filtered_image_quality_info.iter_rows(named=True):
        ext = get_file_extension(row["image_quality_data_file"])
        if ext is not None:
            df = read_file(row["image_quality_data_file"], ext)
            df = df.with_columns(
                pl.lit(row[DATABASE_SCHEMA["EXPERIMENT_PLATE_ACQID_COLUMN"]]).alias(
                    "Metadata_AcqID"
                ),
                pl.lit(row[DATABASE_SCHEMA["EXPERIMENT_PLATE_BARCODE_COLUMN"]]).alias(
                    "Metadata_Barcode"
                ),
            )
            # Cast all numerical f64 columns to f32
            for name, dtype in zip(df.columns, df.dtypes):
                if dtype == pl.Float64:
                    df = df.with_columns(pl.col(name).cast(pl.Float32))
                elif dtype == pl.Int64:
                    df = df.with_columns(pl.col(name).cast(pl.Int32))
            dfs.append(df)
            log_info(
                f"Successfully imported {df.shape}: {row['image_quality_data_file']}{ext}"
            )

    if force_merging_columns == "keep":
        concat_method = "diagonal"  # keep all columns and fill missing values with null
    elif force_merging_columns == "drop":
        concat_method = (
            "vertical"  # merge dfs horizontally, only keeps matching columns
        )
        common_columns = set(dfs[0].columns)
        for df in dfs[1:]:
            common_columns.intersection_update(df.columns)
        dfs = [df.select(sorted(common_columns)) for df in dfs]
    else:
        # Check if all dataframes have the same shape, if not print a message
        if len({df.shape[1] for df in dfs}) > 1:
            log_warning(
                "\nDataframes have different shapes and cannot be stacked together!"
            )
            return None
        concat_method = "vertical"  # standard vertical concatenation

    log_info(f"\n{'_'*50}\nQuality control data of {len(dfs)} plates imported!\n")
    # Concatenate all the dataframes at once and return it
    return (
        pl.concat(dfs, how=concat_method)
        .with_columns(
            (
                pl.col("Metadata_AcqID").cast(pl.Utf8)
                + "_"
                + pl.col("Metadata_Well")
                + "_"
                + pl.col("Metadata_Site").cast(pl.Utf8)
            ).alias("ImageID")
        )
        .sort(["Metadata_Barcode", "Metadata_Well", "Metadata_Site", "ImageID"])
        # reorder columns to match desired order
        .select(pl.col(["ImageID", "Metadata_AcqID", "Metadata_Barcode", "Metadata_Well", "Metadata_Site", "ImageNumber",]),
                pl.exclude(["ImageID", "Metadata_AcqID", "Metadata_Barcode", "Metadata_Well", "Metadata_Site", "ImageNumber",])
        )
        if dfs
        else None
    )
