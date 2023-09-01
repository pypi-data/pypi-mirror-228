import os
import subprocess
import polars as pl
import pandas as pd
from typing import Union, Literal
from .logger import (
    log_error,
)

def has_gpu():
    try:
        subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    
def get_file_extension(filename):
    """Helper function to get file extension"""
    possible_extensions = [".parquet", ".csv", ".tsv"]
    for ext in possible_extensions:
        full_filename = filename + ext
        if os.path.isfile(full_filename):
            return ext
    log_error(
        f"No file with extensions {possible_extensions} was not found for {filename}."
    )
    return None


def read_file(filename, extension):
    """Helper function to read file based on its extension"""
    if extension == ".parquet":
        df = pl.read_parquet(filename + extension)
    elif extension in [".csv", ".tsv"]:
        delimiter = "," if extension == ".csv" else "\t"
        df = pl.read_csv(filename + extension, separator=delimiter)
    else:
        return None
    # Change column type to float32 if all values are null (unless in some case it changes to str)
    for name in df.columns:
        if df[name].is_null().sum() == len(df[name]):
            df = df.with_columns(df[name].cast(pl.Float32))
    return df

def normalize_df(df: Union[pl.DataFrame, pd.DataFrame], method: Literal["zscore", "minmax"] = "zscore"):
    # Check if data is in pandas DataFrame, if so convert to polars DataFrame
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    methods = {
        "minmax": lambda x: (x - x.min()) / (x.max() - x.min()),
        "zscore": lambda x: (x - x.mean()) / x.std(ddof=1),
    }

    df = df.select(
        [
            (
                methods[method](df[col])
                if df[col].dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]
                else df[col]
            ).alias(col)
            for col in df.columns
        ]
    )
    return df
