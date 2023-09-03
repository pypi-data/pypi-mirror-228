# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorCom(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_com'
        self.category = 'Other'
        self.name = '综合因子'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_com1(self,
                    data=None,
                    dependencies=[
                        'dummy120_fst', 'buy_value_large_order_act',
                        'buy_value_exlarge_order_act', 'sw1',
                        's_mfd_inflow_open', 's_mfd_inflow_close'
                    ],
                    window=5):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        buy_value_large_order_act = data['buy_value_large_order_act']
        buy_value_exlarge_order_act = data['buy_value_exlarge_order_act']
        s_mfd_inflow_open = data['s_mfd_inflow_open']
        s_mfd_inflow_close = data['s_mfd_inflow_close']
        factor1 = -np.abs(
            buy_value_large_order_act.add(
                buy_value_exlarge_order_act, fill_value=0).sub(
                    buy_value_large_order_act.rolling(5, min_periods=1).mean(),
                    fill_value=0).sub(buy_value_exlarge_order_act.rolling(
                        5, min_periods=1).mean(),
                                      fill_value=0))
        factor2 = -s_mfd_inflow_open.rolling(5, min_periods=1).std().add(
            s_mfd_inflow_close.rolling(5, min_periods=1).std(), fill_value=0)
        factor = factor_merge([factor1, factor2])
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_mf1")