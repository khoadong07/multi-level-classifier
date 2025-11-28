"""File handling utilities"""
import pandas as pd
from io import BytesIO
from typing import BinaryIO


def load_excel(file: BinaryIO) -> pd.DataFrame:
    """Load Excel file into DataFrame"""
    return pd.read_excel(file)


def save_excel(df: pd.DataFrame, filename: str):
    """Save DataFrame to Excel file"""
    df.to_excel(filename, index=False, engine='xlsxwriter')


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to Excel bytes for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Classified Data')
    return output.getvalue()
