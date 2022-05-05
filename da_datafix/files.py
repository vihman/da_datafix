import logging
import pickle
import re
from datetime import datetime
from typing import Optional

from da_datafix.model import DataModel

logger = logging.getLogger(__file__)

months = {
    "jaan": "Jan",
    "dets": "Dec",
    "okt": "Oct"
}


def _make_dtype(r, delimiter, timestamp_column):
    result = []
    cols = r.split(delimiter)
    for col_no, col in enumerate(cols):
        if col_no == timestamp_column:
            result.append(("timestamp", "datetime64[s]"))
        else:
            result.append((col.strip(), "float"))
    return result


def _convert_types(rowarr: list, timestamp_col) -> tuple:
    result = []
    for no, elem in enumerate(rowarr):
        if no == timestamp_col:
            # timezone element %Z can be undefined and raise exception on some platform C library.
            # Better not to use it. Let's strip Timezone for now, maybe later use or convert UTC.
            _elem, _ = elem.rsplit(" ", maxsplit=1)

            try:  # Feb 22 and newer format: 01-Mar-22 12:35:00 AM EET
                result.append(datetime.strptime(_elem, "%d-%b-%y %I:%M:%S %p"))
                continue
            except ValueError as e:
                logger.debug("Date conversion failed for Feb 22 format: row_no:[%s] [%s]: %s. Trying next format.",
                             no, _elem, e, )

            try:  # Jan 22 and older format: 1 jaan 2022 0:05:00 EET
                # Change months from estonian if needed
                for k, v in months.items():
                    _elem = re.sub(k, v, _elem)
                result.append(datetime.strptime(_elem, "%d %b %Y %H:%M:%S"))
                continue
            except ValueError as e:
                logger.debug("Date conversion failed for Sep 21 format: row_no:[%s] [%s]: %s. Trying next format"
                             , no, _elem, e, )
            try:  # Aug 21 and older format: 22:45 07.08.2020
                result.append(datetime.strptime(elem, "%H:%M %d.%m.%Y"))
            except ValueError as e:
                logger.error("Date conversion failed: row_no:[%s] [%s]: %s", no, elem, e)
                raise e
        else:
            try:
                result.append(float(elem))
            except Exception as e:
                logger.error("Cannot convert line %s", rowarr)
                raise e
    return tuple(result)


def _convert_line(line: str, delimiter, timestamp_column):
    if '"' in line:  # This is old style format - "34,56","78,90"
        elements = re.split(r',(?=["n])', line)  # nan is without quotes
        elements = [re.sub(r'"?(\d+),(\d+)"?', r"\1.\2", e) for e in elements]  # commas to dots & strip quotes if needed
    else:
        elements = line.split(delimiter)
    converted_line = _convert_types(elements, timestamp_column)
    return converted_line


def from_csv(filename: str, headerline: Optional[bool] = True) -> DataModel:
    """
    Parse `Annelinna csv format`_ file and generate model from it.

    Args:
        filename: of the csv.
        headerline: bool header line for extracting datafields.

    Returns: model

    ..  _Annelinna csv format:
        https://livettu.sharepoint.com/:f:/s/SmartCityChallenge-Buildingenergyandindoorclimateaudit/Eua5ItsGNzxEvO58IygI6LMBluAV2q31a5ttRl_cGE-22Q
    """
    timestamp_column = 0
    delimiter = ","
    result = []
    dtype = []
    with open(filename) as f:
        for row_no, row in enumerate(f):
            if headerline and row_no == 0:
                dtype = _make_dtype(row, delimiter, timestamp_column)
            else:
                result.append(_convert_line(row, delimiter, timestamp_column))
    return DataModel(result, dtype)


def to_pickle_pd(filename: str, model: DataModel):
    """
    Save model to Pandas pickle.

    Args:
        filename: to save
        model: to save
    """
    dat = model.get_data_pd()
    with open(filename, "wb") as f:
        pickle.dump(dat, f)


def to_pickle(filename: str, model: object):
    """
    Save object to pickle (e.g. model)

    Args:
        filename: to save,
        model: object to save,
    """
    with open(filename, "wb") as f:
        pickle.dump(model, f)


def from_pickle(filename):
    """
    Loads object from pickle.

    Args:
        filename: to load.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)
