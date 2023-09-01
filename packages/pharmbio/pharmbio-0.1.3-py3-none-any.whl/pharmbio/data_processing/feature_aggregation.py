import polars as pl


def aggregate_morphology_data_cpu(
    df, columns_to_aggregate, groupby_columns, aggregation_function="mean"
):
    grouped = df.lazy().groupby(groupby_columns)
    retain_cols = [c for c in df.columns if c not in columns_to_aggregate]
    retained_metadata_df = df.lazy().select(retain_cols)

    # Aggregate only the desired columns.
    agg_exprs = [
        getattr(pl.col(col), aggregation_function)().alias(col)
        for col in columns_to_aggregate
    ]

    # Execute the aggregation.
    agg_df = grouped.agg(agg_exprs)
    agg_df = agg_df.join(retained_metadata_df, on=groupby_columns, how="left")

    return agg_df.sort(groupby_columns).collect()


def aggregate_morphology_data_gpu(
    df, columns_to_aggregate, groupby_columns, aggregation_function="mean"
):
    try:
        import importlib
        import numpy as np

        cudf = importlib.import_module("cudf")
        # Convert the Polars DataFrame to Arrow table and then to cuDF DataFrame
        # This will avoid copying the data and thus more efficient
        arrow_table = df.to_arrow()
        df = cudf.DataFrame.from_arrow(arrow_table)
        
        # Check for special case where 'mean' should map to 'nanmean'
        if aggregation_function == "mean":
            agg_func = np.nanmean
        elif aggregation_function == "median":
            agg_func = np.nanmedian
        else:
            agg_func = getattr(np, aggregation_function)

        agg_dict = {col: agg_func for col in columns_to_aggregate}
        agg_df = df.groupby(groupby_columns).agg(agg_dict).reset_index()

        agg_df = agg_df.sort_values(by=groupby_columns)

        return pl.from_arrow(agg_df.to_arrow())

    except ImportError as e:
        raise ImportError(
            "cuDF is not available. Please install it to use GPU acceleration."
        ) from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e
