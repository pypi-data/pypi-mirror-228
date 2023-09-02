# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorSize(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_size'
        self.category = 'Size'
        self.name = '规模因子'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_size1(self,
                     data=None,
                     dependencies=['dummy120_fst', 'fuqer_NLSIZE', 'sw1'],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['fuqer_NLSIZE']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_size1")

    def factor_size2(self,
                     data=None,
                     dependencies=['dummy120_fst', 'fuqer_LCAP', 'sw1'],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['fuqer_LCAP']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_size2")

    def factor_size3(self,
                     data=None,
                     dependencies=['dummy120_fst', 'f_SIZENL', 'sw1'],
                     window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['f_SIZENL']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_size3")