# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorVolatilityStock(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_volatility_stock'
        self.category = 'Volatility'
        self.name = '股票波动率'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def bollbais(self, invar, n, m):
        ma = invar.rolling(n, min_periods=1).mean()
        ma[ma <= 0] = np.nan
        std = invar.rolling(n, min_periods=3).std()
        std[std == 0] = np.nan
        boll_cls2up = invar / (ma + 2 * std) - 1
        boll_cls2dow = invar / (ma - 2 * std) - 1
        boll_cls2up[np.isinf(boll_cls2up)] = np.nan
        boll_cls2dow[np.isinf(boll_cls2dow)] = np.nan
        boll_cls2up_pnd = boll_cls2up.rolling(m, min_periods=1).sum()
        boll_cls2dow_pnd = boll_cls2dow.rolling(m, min_periods=1).sum()
        return boll_cls2up_pnd, boll_cls2dow_pnd

    def dma(self, invar, n, m):
        ma = invar.rolling(n, min_periods=1).mean()
        ma[ma <= 0] = np.nan
        testvar_dma = (invar - ma) / ma
        testvar_dma_pnd = testvar_dma.rolling(m, min_periods=1).sum()
        return testvar_dma_pnd

    def factor_vol1(self,
                    data=None,
                    dependencies=['dummy120_fst', 'fuqer_ACD20', 'sw1'],
                    window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['fuqer_ACD20']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol1")

    def factor_vol2(self,
                    data=None,
                    dependencies=['dummy120_fst', 'closePrice', 'sw1'],
                    window=120):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        closePrice = data['closePrice']
        factor, _ = self.bollbais(closePrice, 120, 1)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol2")

    def factor_vol3(self,
                    data=None,
                    dependencies=['dummy120_fst', 'ffancy_upp01M20D', 'sw1'],
                    window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['ffancy_upp01M20D']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol3")

    def factor_vol4(self,
                    data=None,
                    dependencies=[
                        'dummy120_fst', 'highestPrice', 'lowestPrice', 'sw1'
                    ],
                    window=60):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        highp = data['highestPrice']
        lowp = data['lowestPrice']
        price_range = highp / lowp
        pnd = price_range.rolling(60, min_periods=1).sum() / 60
        my_std = price_range.rolling(60, min_periods=20).std()
        factor = -pnd / my_std
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol4")

    def factor_vol5(self,
                    data=None,
                    dependencies=['dummy120_fst', 'turnoverVol', 'sw1'],
                    window=120):
        data = self._data if data is None else data
        vol = data['turnoverVol']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -vol.rolling(20, min_periods=10).std() / vol.rolling(
            120, min_periods=30).std()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol5")

    def factor_vol6(self,
                    data=None,
                    dependencies=['dummy120_fst', 'fuqer_VSTD10', 'sw1'],
                    window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = -data['fuqer_VSTD10']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol6")

    def factor_vol7(self,
                    data=None,
                    dependencies=['dummy120_fst', 'turnoverRate', 'sw1'],
                    window=10):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        turnoverRate = data['turnoverRate']
        factor = -turnoverRate.rolling(10, min_periods=5).std()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol7")

    def factor_vol8(self,
                    data=None,
                    dependencies=['dummy120_fst', 'turnoverRate', 'sw1'],
                    window=60):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        turnoverRate = data['turnoverRate']
        factor = -turnoverRate.rolling(60, min_periods=20).std()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol8")

    def factor_vol9(self,
                    data=None,
                    dependencies=['dummy120_fst', 'turnoverRate', 'sw1'],
                    window=90):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        turnoverRate = data['turnoverRate']
        pnd = turnoverRate.rolling(90, min_periods=1).sum() / 90
        my_std = turnoverRate.rolling(90, min_periods=30).std()
        factor = -pnd / my_std
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_vol9")