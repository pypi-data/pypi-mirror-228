import polars as pl
import cudf

def aggregate_morphology_data(
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


def aggregate_morphology_data_cudf(
    df, columns_to_aggregate, groupby_columns, aggregation_function="mean"
):
    # Convert the polars DataFrame to cuDF DataFrame
    df = cudf.from_pandas(df.to_pandas())

    # Retain the metadata columns (the ones you don't want to aggregate)
    retained_metadata_df = df[groupby_columns]

    agg_dict = {col: aggregation_function for col in columns_to_aggregate}
    agg_df = df.groupby(groupby_columns).agg(agg_dict).reset_index()

    # Remove duplicates from retained_metadata_df (optional)
    retained_metadata_df = retained_metadata_df.drop_duplicates()

    # Join the aggregated DataFrame and the retained metadata DataFrame
    agg_df = agg_df.merge(retained_metadata_df, on=groupby_columns, how="left")

    # Sort the DataFrame based on groupby_columns
    agg_df = agg_df.sort_values(by=groupby_columns)

    return pl.DataFrame(agg_df.to_pandas())
