# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorFormulaStock(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_formula_stock'
        self.category = 'Formula'
        self.name = '股票公式因子'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_formula1(self,
                        data=None,
                        dependencies=['dummy120_fst', 'vwap', 'sw1', 'ret'],
                        window=30):
        data = self._data if data is None else data
        vol = data['turnoverVol']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        ret = data['ret']
        vwap = data['vwap']
        factor = clear_by_cond(dfabs(ts_rank(dfabs(ts_rank(ret, 7)), 6)),
                               ts_max(vol, 4),
                               vdelta(rank(decay_linear(vwap, 3)), 4))
        factor = factor.where(factor != 0, factor + 0.1)
        factor = -factor.rolling(20, min_periods=10).mean()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_formula1")

    def factor_formula2(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'highestPrice', 'sw1',
                            'turnoverVol'
                        ],
                        window=30):
        data = self._data if data is None else data
        vol = data['turnoverVol']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        highestPrice = data['highestPrice']
        factor = ts_max(corr(highestPrice, vol, 6), 5)
        factor = -factor.rolling(20, min_periods=10).mean()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_formula2")

    def factor_formula3(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'turnoverVol', 'sw1', 'closePrice',
                            'vwap'
                        ],
                        window=10):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        vol = data['turnoverVol']
        closePrice = data['closePrice']
        vwap = data['vwap']
        factor = vsub(ts_argmin(vdiv(closePrice, vwap), 10), ts_stdev(vol, 10))
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_formula3")