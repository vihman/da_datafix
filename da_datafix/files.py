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
    # "nov": None,
    # data/12.2021/Report_CO2.csv
}


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
    delimiter = ","
    timestamp_column = 0

    def make_dtype(r):
        result = []
        cols = r.split(delimiter)
        for col_no, col in enumerate(cols):
            if col_no == timestamp_column:
                result.append(("timestamp", "datetime64[s]"))
            else:
                result.append((col.strip(), "float"))
        return result

    def convert_line(line: str, timestamp_col: int = 0):

        def convert_types(rowarr: list) -> tuple:
            result = []
            for no, elem in enumerate(rowarr):
                if no == timestamp_col:
                    try:
                        # timezone element %Z can be undefined and raise exception on some platform C library.
                        # Better not to use it. Let's strip Timezone for now, maybe later use or convert it.
                        elem, _ = elem.rsplit(" ", maxsplit=1)
                    except Exception as e:
                        logger.error("Timezone value expected but not found.")
                        raise e
                    try:  # Feb 22 and newer format
                        result.append(datetime.strptime(elem, "%d-%b-%y %I:%M:%S %p"))
                        continue
                    except ValueError as e:
                        logger.debug("Date conversion failed for format: row_no:[%s] [%s]: %s. Trying older. format",
                                     no, elem, e, )

                    try:  # Jan 22 and older format - 1 Jan 2022 0:00:00
                        for k, v in months.items():
                            elem = re.sub(k, v, elem)
                        result.append(datetime.strptime(elem, "%d %b %Y %H:%M:%S"))
                    except ValueError as e:
                        logger.error("Date conversion failed: row_no:[%s] [%s]: %s", no, elem, e, )
                        raise e
                # raise e
                else:
                    try:
                        result.append(float(elem))
                    except Exception as e:
                        logger.error("Cannot convert line %s", line)
                        raise e
            return tuple(result)
        if '"' in line:  # This is old style format - "34,56","78,90"
            elements = re.split(r',(?=["n])', line)  # nan is without quotes
            elements = [re.sub(r'"?(\d+),(\d+)"?', r"\1.\2", e) for e in elements]  # commas to dots & strip quotes if needed
        else:
            elements = line.split(delimiter)
        converted_line = convert_types(elements)
        return converted_line

    result = []
    dtype = []
    with open(filename) as f:
        for row_no, row in enumerate(f):
            if headerline and row_no == 0:
                dtype = make_dtype(row)
            else:
                result.append(convert_line(row))
    return DataModel(result, dtype)


def to_pickle(filename: str, model: DataModel):
    """
    Save model to Pandas pickle.

    Args:
        filename: to save
        model: to save
    """
    dat = model.get_data_pd()
    with open(filename, "wb") as f:
        pickle.dump(dat, f)
