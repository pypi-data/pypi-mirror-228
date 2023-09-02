# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorRiskStock(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_risk_stock'
        self.category = 'Risk'
        self.name = '股票风险因子'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_risk1(self,
                     data=None,
                     dependencies=[
                         'dummy120_fst', 'fuqer_GainLossVarianceRatio20', 'sw1'
                     ],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['fuqer_GainLossVarianceRatio20']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_risk1")

    def factor_risk2(self,
                     data=None,
                     dependencies=[
                         'dummy120_fst', 'fuqer_GainLossVarianceRatio60', 'sw1'
                     ],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        fuqer_GainLossVarianceRatio60 = data['fuqer_GainLossVarianceRatio60']
        factor = -fuqer_GainLossVarianceRatio60
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_risk2")

    def factor_risk3(self,
                     data=None,
                     dependencies=[
                         'dummy120_fst', 'fuqer_GainLossVarianceRatio120',
                         'sw1'
                     ],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        fuqer_GainLossVarianceRatio120 = data['fuqer_GainLossVarianceRatio120']
        factor = -fuqer_GainLossVarianceRatio120
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_risk3")

    # def factor_risk4(self,
    #                  data=None,
    #                  dependencies=['dummy120_fst', 'SRISK', 'sw1'],
    #                  window=1):
    #     data = self._data if data is None else data
    #     dummy = data['dummy120_fst']
    #     sw1 = data['sw1']
    #     factor = data['SRISK']
    #     factor = indfill_median(factor * dummy, sw1)
    #     return self._format(factor, "factor_risk4")

    def factor_risk4(
            self,
            data=None,
            dependencies=['dummy120_fst', 'fuqer_GainVariance20', 'sw1'],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['fuqer_GainVariance20']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_risk4")