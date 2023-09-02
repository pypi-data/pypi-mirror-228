# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorNorth(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_north'
        self.category = 'North'
        self.name = '北向资金'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def north_sub1(self, data, halflife):
        t = pd.DataFrame(data)
        return t.ewm(halflife=halflife, axis=0).mean().iloc[-1, :].values

    def north1(self,
               data=None,
               dependencies=['dummy120_fst', 'partyPct', 'sw1'],
               window=120):
        data = self._data if data is None else data
        holdpct = data['partyPct']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        f1 = holdpct.rolling(120, min_periods=40).rank(pct=True)
        factor = f1
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north1")

    def north2(self,
               data=None,
               dependencies=[
                   'dummy120_fst', 'closePrice', 'partyVol', 'sw1',
                   'negMarketValue'
               ]):
        data = self._data if data is None else data
        closePrice = data['closePrice']
        holdvol = data['partyVol']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        fcap = data['negMarketValue']
        hld_value = holdvol * closePrice
        hld_value[hld_value <= 0] = np.nan
        hld_value_ratio = hld_value / fcap
        factor = hld_value_ratio
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north2")

    def north3(self,
               data=None,
               dependencies=[
                   'dummy120_fst', 'closePrice', 'partyVol', 'sw1',
                   'negMarketValue'
               ],
               window=60):
        data = self._data if data is None else data
        closePrice = data['closePrice']
        holdvol = data['partyVol']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        fcap = data['negMarketValue']
        hld_value = holdvol * closePrice
        hld_value[hld_value <= 0] = np.nan
        hld_value_ratio = hld_value / fcap
        hld_value_ratio_chg_60d = hld_value_ratio - hld_value_ratio.shift(60)
        factor = hld_value_ratio_chg_60d
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north3")

    def north4(self,
               data=None,
               dependencies=[
                   'dummy120_fst', 'closePrice', 'partyVol', 'sw1',
                   'turnoverValue', 'turnoverVol', 'adjFactorVol'
               ],
               window=20):
        data = self._data if data is None else data
        closePrice = data['closePrice']
        holdvol = data['partyVol']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        val = data['turnoverValue']
        vol = data['turnoverVol']
        adjFactorVol = data['adjFactorVol']
        adjFactor = adjFactorVol / adjFactorVol.shift(1)
        vwap = val / vol
        hld_value = holdvol * closePrice
        hld_value[hld_value <= 0] = np.nan
        netinflowvol = holdvol - holdvol.shift(1) * adjFactor
        netinflowval = netinflowvol * vwap
        net_buy_m_to_net_buy_std_20d = netinflowval.rolling(
            20, min_periods=1).mean() / netinflowval.rolling(
                20, min_periods=1).std()
        factor = net_buy_m_to_net_buy_std_20d
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north4")

    def north5(self,
               data=None,
               dependencies=[
                   'dummy120_fst', 'closePrice', 'partyVol', 'sw1',
                   'turnoverValue', 'turnoverVol', 'adjFactorVol'
               ],
               window=60):
        data = self._data if data is None else data
        closePrice = data['closePrice']
        holdvol = data['partyVol']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        val = data['turnoverValue']
        vol = data['turnoverVol']
        adjFactorVol = data['adjFactorVol']
        adjFactor = adjFactorVol / adjFactorVol.shift(1)
        vwap = val / vol
        hld_value = holdvol * closePrice
        hld_value[hld_value <= 0] = np.nan
        netinflowvol = holdvol - holdvol.shift(1) * adjFactor
        netinflowval = netinflowvol * vwap
        net_buy_m_to_net_buy_std_60d = netinflowval.rolling(
            60, min_periods=1).mean() / netinflowval.rolling(
                60, min_periods=1).std()
        factor = net_buy_m_to_net_buy_std_60d
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north5")

    def hk_to_shsz_trim(self, data_to_trim, data_intersect, direction):
        data_t = data_to_trim.copy().pad() * direction[0]
        data_t.index = data_t.index.astype('datetime64[ns]')
        data_t_monthly = data_t.resample('M').last()
        temp1 = data_t_monthly.sub(data_t_monthly.quantile(1 / 3, axis=1),
                                   axis=0)
        data_intersect_t = data_intersect.copy().pad() * direction[1]
        data_intersect_t.index = data_intersect_t.index.astype(
            'datetime64[ns]')
        data_intersect_t_monthly = data_intersect_t.resample('M').last()
        temp2 = data_intersect_t_monthly.sub(data_intersect_t_monthly.quantile(
            1 / 3, axis=1),
                                             axis=0)

        drop_dummy = pd.DataFrame(index=data_t_monthly.index,
                                  columns=data_t_monthly.columns)
        drop_dummy[(temp1 < 0) & (temp2 < 0)] = 1
        drop_dummy = drop_dummy.resample('D').ffill().shift(1)
        data_trimd = data_to_trim.copy()
        data_trimd[drop_dummy == 1] = np.nan

        return data_trimd

    def north6(self,
               data=None,
               dependencies=[
                   'dummy120_fst', 'closePrice', 'partyVol', 'sw1',
                   'turnoverValue', 'turnoverVol', 'adjFactorVol',
                   'negMarketValue'
               ],
               window=60):
        data = self._data if data is None else data
        closePrice = data['closePrice']
        holdvol = data['partyVol']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        val = data['turnoverValue']
        vol = data['turnoverVol']
        adjFactorVol = data['adjFactorVol']
        fcap = data['negMarketValue']
        adjFactor = adjFactorVol / adjFactorVol.shift(1)
        vwap = val / vol
        hld_value = holdvol * closePrice
        hld_value[hld_value <= 0] = np.nan
        hld_value_ratio = hld_value / fcap
        # 动态因子计算
        hld_value_ratio_chg_20d = hld_value_ratio - hld_value_ratio.shift(20)
        hld_value_ratio_chg_60d = hld_value_ratio - hld_value_ratio.shift(60)
        netinflowvol = holdvol - holdvol.shift(1) * adjFactor
        netinflowval = netinflowvol * vwap
        net_buy_to_hld_m_20d = netinflowval.rolling(
            20, min_periods=1).mean() / hld_value.rolling(
                20, min_periods=1).mean()
        # 非线性修正
        hld_value_ratio_chg_20d_trimd = self.hk_to_shsz_trim(
            hld_value_ratio_chg_20d, hld_value_ratio, [1, -1])
        hld_value_ratio_chg_60d_trimd = self.hk_to_shsz_trim(
            hld_value_ratio_chg_60d, hld_value_ratio, [1, -1])
        net_buy_to_hld_m_20d_trimd = self.hk_to_shsz_trim(
            net_buy_to_hld_m_20d, hld_value, [-1, 1])
        # 复合因子
        hk_to_shsz = hld_value_ratio_chg_20d_trimd * 0.5 + hld_value_ratio_chg_60d_trimd * 0.5 + net_buy_to_hld_m_20d_trimd
        factor = hk_to_shsz
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north6")

    def north7(self,
               data=None,
               dependencies=['dummy120_fst', 'sw1', 'ffancy_hkHoldRatioAll']):
        data = self._data if data is None else data
        factor = data['ffancy_hkHoldRatioAll']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north7")

    def north8(self,
               data=None,
               dependencies=['dummy120_fst', 'sw1', 'ffancy_hkHoldRatioB']):
        data = self._data if data is None else data
        factor = data['ffancy_hkHoldRatioB']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north8")

    def north9(self,
               data=None,
               dependencies=['dummy120_fst', 'sw1',
                             'ffancy_hkHoldVolChgB120']):
        data = self._data if data is None else data
        factor = data['ffancy_hkHoldVolChgB120']
        vardummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = indfill_median(factor * vardummy, sw1)
        factor.fillna(method='pad', inplace=True)
        return self._format(factor, "north9")
