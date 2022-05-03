import bisect
import logging
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from numpy.lib import recfunctions

import da_datafix.fix as fix

logger = logging.getLogger(__file__)


class DataModel:
    """
     Digiaudit time series data model. Data is kept in numpy structured arrays.
    """

    def __init__(self, datalist: list, dtype: np.dtype):
        """
        Init model. Better to do it from fileimport

        Args:
            datalist: list to be converted to ndArray.
            dtype: datatype of the list.
        """
        self.data = np.array(datalist, dtype=dtype)

    def get_data_window(self, start_time: datetime, end_time: datetime,
                        time_field: Optional[str] = "timestamp") -> np.array:
        """
        Get slice data to only needed time window.

        Args:
            time_field: field name of timestamp values for slicing.
            start_time: starting time of the slice. Will be included in slice.
            end_time:  ending time of the slice. Will be included.

        Returns:
            `Structured numpy array`_.

        .. _Structured numpy array:
            https://numpy.org/doc/stable/user/basics.rec.html

        """
        def get_ndarr_index(value, ndarr):
            return np.ndarray.searchsorted(ndarr, value)

        def get_idx(val, arr):
            return bisect.bisect_right(arr[time_field], val)

        start_idx = max(get_idx(start_time, self.data) - 1, 0)
        end_idx = get_idx(end_time, self.data)
        return self.data[start_idx:end_idx]

    def get_data(self) -> np.array:
        """
        Get data as numpy structured array.

        Returns:
            `Structured numpy array`_


        """
        return self.data

    def get_data_pd(self) -> pd.DataFrame:
        """
        Copy data as Pandas Dataframe object.

        Returns:
             data as pd.DataFrame
        """
        return pd.DataFrame(self.data, index=self.data["timestamp"])

    def get_fields(self) -> list:
        """
        Get named fields of model's data structure.

        Returns:
            list of field names.

        """
        return self.data.dtype.names

    def _add_field(self, dat, kf_smooth):
        recfunctions.append_fields(dat, 'KF_Smooth', kf_smooth, fill_value=None, asrecarray=False)
        return NotImplementedError

    def adjust_baseline(self):
        """
        Adjust CO2 baseline on data of the model.
        """
        # TODO: Implement it.
        return NotImplementedError

    def fix_lastknown(self, *fields: str):
        """
        Fix missing data in specific fields by using last known good value.

        Args:
            *fields: list of field name strings. "*" can be used to apply to all fields.
        """
        logger.info(f"making lastknown for {fields=}")
        if "*" in fields:
            if len(fields) != 1:
                raise Exception("If * specified then no other fields can be specified.")
            fields = self.get_fields()
        for f in fields:
            fix.fix_lastknown(self.data[f])

# OK: Täita augud eelmise väärtusega vms (eeldatavasti on väiksed augud) - CO2, temperatuur
# test slicing
# write csv
# split to different fields.
# OK: test slicing
# TODO: CO2 baastaseme muutus
# TODO: Kumulatiivsete andmete aukude täitmine - elekter, soojus, vesi (see mis arutasime, Kalman filter ilmselt?)
# TODO: https://gitlab.com/gitlab-org/gitlab/-/issues/209301
# TODO: check SOC format, if it can be imported same? There is no csv? Only what we got from whoeverit was?
