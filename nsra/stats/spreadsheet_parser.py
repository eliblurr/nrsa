# Extract NRSA data from spreadsheets this should support following data formats
# 1. xlsx
# 2. xls
# 3. ods
# 4. csv

import openpyxl
import xlrd
from pyexcel_ods import get_data
import os

from .data_extractor import format_1
import logging
from io import BytesIO


def convert_xlsx_to_csv(file) -> str:
    logging.info('called xlsx')
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    csv_str = ""

    for row in sheet.rows:
        line = []
        for cell in row:
            line.append(cell.value)
        if any(line):
            csv_str += ",".join(map(lambda x: str(x), line)) + "\n"
    # logging.info(f"Csv Final str: {csv_str}")
    return csv_str


def convert_xls_to_csv(file) -> str:
    sheet = xlrd.open_workbook_xls(file).sheet_by_index(0)

    csv_str = ""
    for row in range(sheet.nrows):
        if any(sheet.row_values(row)):
            csv_str += ",".join(map(lambda x: str(x),
                                    sheet.row_values(row))) + "\n"

    return csv_str


def convert_ods_to_csv(file) -> str:
    data = get_data(file)

    csv_str = ""
    for sheet in data.values():
        for row in sheet:
            if any(row):
                csv_str += ",".join(map(lambda x: str(x), row)) + "\n"

    return csv_str


# get filename and retrieve extension
def file_ext_check(File):
    ext = File.name.split('.')[-1].lower()
    file = BytesIO(File.read())
    logging.info(File.name)

    #  convert to csv from extension
    if ext == 'xlsx':
        csv_str = convert_xlsx_to_csv(file)
    elif ext == 'xls':
        csv_str = convert_xls_to_csv(file)
    elif ext == 'ods':
        csv_str = convert_ods_to_csv(file)
    else:
        logging.info(f'no ext found: {ext}')
        csv_str = None

    return csv_str