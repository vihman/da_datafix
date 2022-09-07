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
     Digiaudit time series data model. Data is kept in `Structured numpy array`_.
    """

    def __init__(self, datalist: list, dtype: np.dtype):
        """
        Init model. In practice better to do from files.from_csv.

        Args:
            datalist: list to be converted to ndArray.
            dtype: datatype of the list.
        """
        self.data = np.array(datalist, dtype=dtype)

    def get_data_window(self, start_time: datetime, end_time: datetime,
                        time_field: Optional[str] = "timestamp") -> np.array:
        """
        Get sliced data to only needed time window. Doesn't affect model.

        Args:
            start_time: starting time of the slice. Will be included in slice.
            end_time:  ending time of the slice. Will be included.
            time_field: [Optional] field name of timestamp values for slicing.

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

    def set_data_window(self, start_time: datetime, end_time: datetime):
        """
        Set model's data to only specified time window.

        :param start_time: of window
        :param end_time:  of window
        """
        self.data = self.get_data_window(start_time, end_time)

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

    def fix_baseline(self, field: str):
        """
        Adjust CO2 baseline on data of the model.

        Args:
            field: field name of the data to fix.
        """
        fix.fix_baseline(self.data[field])

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

    def get_occupation_from_co2(self, smoothing_kernel_size: int = 7,
                                timestamp_field_name: str ="timestamp",
                                co2_field_name: str= "240_value",
                                gradient_boundary: float=0.01) -> np.array:
        """
        Get occupation of room using CO2 values gradient. This method 1) smoothes the data to reduce false positives 2) calculates gradient of the data
        3) returns vector of room occupation where gradient is greater of given boundary.
        Args:
            timestamp_field_name: data field name for timestamp.
            co2_field_name: data field name for the co2 values vector.
            gradient_boundary: boundary counstant of gradient up from where room is considered occupied.
            smoothing_kernel_size: data convolution kernel size.

        Returns:
            vector of room occupation: (1==occupied, 0==not occupied)
        """

        def smooth_data(dta, kernel_size=7):
            kernel = np.ones(kernel_size) / kernel_size
            return np.convolve(dta, kernel, mode='same')

        def get_gradient(tsa, smoothed_data):
            timediff = tsa - tsa[0]
            gda = np.gradient(smoothed_data, timediff, edge_order=1)
            return gda
        smoothed = smooth_data(self.data[co2_field_name], smoothing_kernel_size)
        grad = get_gradient(self.data[timestamp_field_name], smoothed)
        occ = np.greater(grad, gradient_boundary)
        return occ

# TODO: Kumulatiivsete andmete aukude täitmine - elekter, soojus, vesi (see mis arutasime, Kalman filter ilmselt?)
