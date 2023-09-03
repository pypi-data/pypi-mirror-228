# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
import pdb
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorConsensus(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_consensus'
        self.category = 'Consensus'
        self.name = '一致预期'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_con1(
            self,
            data=None,
            dependencies=['conheat_allReportCover1w', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conheat_allReportCover1w']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con1")

    def factor_con2(self,
                    data=None,
                    dependencies=['conpub_conPE_yr3', 'sw1', 'dummy120_fst'],
                    window=1):
        data = self._data if data is None else data
        conPe3 = data['conpub_conPE_yr3']
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = 1 / conPe3
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con2")

    def factor_con3(self,
                    data=None,
                    dependencies=[
                        'conpub_conProfitYoy_yr3', 'marketValue',
                        'dummy120_fst', 'f_MOMENTUM', 'sw1'
                    ],
                    window=1):
        data = self._data if data is None else data
        deri_conProfitYoy3 = data['conpub_conProfitYoy_yr3']
        mktcap = data['marketValue']
        dummy = data['dummy120_fst']
        MOMENTUM = data['f_MOMENTUM']
        sw1 = data['sw1']
        f = factor_score(deri_conProfitYoy3 * dummy, 1)
        dfall = pd.DataFrame(mktcap.unstack(), columns=['mktcap'])
        out1 = alphaOpNeu(f, dfall)
        dfall2 = pd.DataFrame(MOMENTUM.unstack(), columns=['MOMENTUM'])
        f1 = alphaOpNeu(out1, dfall2)
        f2 = indLineNeu(f1, sw1)
        factor = standardize(factor_score(f2, 3))
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con3")

    def factor_con4(self,
                    data=None,
                    dependencies=[
                        'bspub_tEquityAttrP_pnq0', 'fbqpub_mergeProfit_pnq0',
                        'conpub_conPeg1_yr0', 'dummy120_fst', 'sw1'
                    ],
                    window=1):
        data = self._data if data is None else data
        tEquityAttrP0 = data['bspub_tEquityAttrP_pnq0']
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        roe = qmergeprofit0 / abs(tEquityAttrP0)
        roe[np.isinf(roe)] = np.nan
        deri_conPeg10 = data['conpub_conPeg1_yr0']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        dfall = pd.DataFrame(deri_conPeg10.unstack(), columns=['peg'])
        factor = alphaOpNeu(roe * dummy, dfall)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con4")

    def factor_con5(self,
                    data=None,
                    dependencies=[
                        'bspub_tEquityAttrP_pnq0', 'fbqpub_mergeProfit_pnq0',
                        'conpub_conPeg1_yr0', 'conpub_conPeg1_yr1',
                        'conpub_conPeg1_yr2', 'conpub_conPeg1_yr3',
                        'conpub_conROE_yr0', 'conpub_conROE_yr1',
                        'conpub_conROE_yr2', 'conpub_conROE_yr3', 'sw1',
                        'dummy120_fst'
                    ],
                    window=1):
        data = self._data if data is None else data
        deri_conROE0 = data['conpub_conROE_yr0']
        deri_conROE1 = data['conpub_conROE_yr1']
        deri_conROE2 = data['conpub_conROE_yr2']
        deri_conROE3 = data['conpub_conROE_yr3']
        deri_conPeg10 = data['conpub_conPeg1_yr0']
        deri_conPeg11 = data['conpub_conPeg1_yr1']
        deri_conPeg12 = data['conpub_conPeg1_yr2']
        deri_conPeg13 = data['conpub_conPeg1_yr3']
        tEquityAttrP0 = data['bspub_tEquityAttrP_pnq0']
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        A = deri_conROE0.add(2 * deri_conROE1, fill_value=0).add(
            3 * deri_conROE2, fill_value=0).add(4 * deri_conROE3,
                                                fill_value=0) / 10
        B = deri_conPeg10.add(2 * deri_conPeg11, fill_value=0).add(
            3 * deri_conPeg12, fill_value=0).add(4 * deri_conPeg13,
                                                 fill_value=0) / 10
        ROE = qmergeprofit0 / abs(tEquityAttrP0)
        factor = -abs((A / ROE - 1) * (A / ROE - 1) * B) * dummy
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con5")

    def factor_con6(self,
                    data=None,
                    dependencies=[
                        'bspub_tEquityAttrP_pnq0', 'conpub_conProfit_yr0',
                        'conpub_conProfit_yr1', 'conpub_conProfit_yr2',
                        'conpub_conProfit_yr3', 'sw1', 'reportquart',
                        'dummy120_fst'
                    ],
                    window=300):
        data = self._data if data is None else data
        conProfit0 = data['conpub_conProfit_yr0']
        conProfit1 = data['conpub_conProfit_yr1']
        conProfit2 = data['conpub_conProfit_yr2']
        conProfit3 = data['conpub_conProfit_yr3']
        reportquart = data['reportquart']
        tEquityAttrP0 = data['bspub_tEquityAttrP_pnq0']
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        tradingday = conProfit0.index
        ticker = conProfit0.columns
        ni = pd.concat([
            conProfit0.unstack(),
            conProfit1.unstack(),
            conProfit2.unstack(),
            conProfit3.unstack()
        ],
                       axis=1).mean(axis=1)
        ni.name = 'ni'
        usequart = pd.concat(
            [reportquart.unstack(),
             reportquart.shift(-1).unstack()], axis=1)
        usequart.columns = ['quart', 'sftquart']
        equity = tEquityAttrP0.unstack()
        equity.name = 'equity'
        alldata = pd.concat([usequart, ni, equity], axis=1).reset_index()
        alldata.sort_values('trade_date', inplace=True)
        hisdata = alldata.loc[(~alldata.quart.isna()) &
                              (~alldata.sftquart.isna()) &
                              (alldata.quart != alldata.sftquart),
                              ['trade_date', 'code', 'ni', 'equity']]
        total = pd.merge_asof(alldata,
                              hisdata,
                              by='code',
                              on='trade_date',
                              direction='backward',
                              tolerance=pd.Timedelta("300days"))
        total['factor'] = (total['ni_x'] - total['ni_y']) / abs(
            total['equity_y'])
        factor = total.pivot_table(index='trade_date',
                                   columns='code',
                                   values='factor')
        factor = factor.reindex(index=tradingday, columns=ticker)
        factor.replace(np.inf, np.nan, inplace=True)
        factor.replace(-np.inf, np.nan, inplace=True)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con6")

    def factor_con7(self,
                    data=None,
                    dependencies=[
                        'conpub_conEPS_yr0', 'conpub_conEPS_yr1',
                        'conpub_conEPS_yr2', 'conpub_conEPS_yr3', 'sw1',
                        'dummy120_fst'
                    ],
                    window=120):
        data = self._data if data is None else data
        conEPS0 = data['conpub_conEPS_yr0']
        conEPS1 = data['conpub_conEPS_yr1']
        conEPS2 = data['conpub_conEPS_yr2']
        conEPS3 = data['conpub_conEPS_yr3']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        pdb.set_trace()
        value_now = 0.25 * conEPS0.add(conEPS1, fill_value=0).add(
            conEPS2, fill_value=0).add(conEPS3, fill_value=0)
        factor = value_now - value_now.shift(120)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con7")

    def factor_con8(self,
                    data=None,
                    dependencies=[
                        'conderi_conProfitRoll', 'marketValue', 'sw1',
                        'dummy120_fst'
                    ],
                    window=240):
        data = self._data if data is None else data
        conProfitRoll = data['conderi_conProfitRoll']
        mktcap = data['marketValue']
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        data = conProfitRoll / mktcap
        factor = (data - data.rolling(240, min_periods=5).mean()
                  ) / data.rolling(240, min_periods=5).std()
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con8")

    def factor_con9(self,
                    data=None,
                    dependencies=[
                        'conpub_conProfit_yr2', 'dummy120_fst', 'sw1',
                        'dummy120_fst'
                    ],
                    window=240):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        conProfit2 = data['conpub_conProfit_yr2']
        sw1 = data['sw1']
        factor = (conProfit2 - conProfit2.rolling(240, min_periods=3).mean()
                  ) / conProfit2.rolling(240, min_periods=3).std()
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con9")

    def factor_con10(self,
                     data=None,
                     dependencies=[
                         'conderi_conProfitrate2yRoll', 'sw1', 'dummy120_fst'
                     ],
                     window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conderi_conProfitrate2yRoll']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con10")

    def factor_con11(self,
                     data=None,
                     dependencies=[
                         'conpub_conIncomeChgpct1h_yr3', 'sw1', 'dummy120_fst'
                     ],
                     window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conpub_conIncomeChgpct1h_yr3']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con11")

    def factor_con12(
            self,
            data=None,
            dependencies=['conpub_conProfitYoy_yr0', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conpub_conProfitYoy_yr0']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con12")

    def factor_con13(
            self,
            data=None,
            dependencies=['conpub_conProfitYoy_yr2', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conpub_conProfitYoy_yr2']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con13")

    def factor_con14(
            self,
            data=None,
            dependencies=['conpub_conProfitType_yr2', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conpub_conProfitType_yr2']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con14")

    def factor_con15(
            self,
            data=None,
            dependencies=['conheat_stkOrgCover1m', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conheat_stkOrgCover1m']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con15")

    def factor_con16(
            self,
            data=None,
            dependencies=['conheat_stkReportCover1q', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conheat_stkReportCover1q']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con16")

    def factor_con17(
            self,
            data=None,
            dependencies=['conheat_stkReportCover1w', 'sw1', 'dummy120_fst'],
            window=1):
        data = self._data if data is None else data
        sw1 = data['sw1']
        dummy = data['dummy120_fst']
        factor = data['conheat_stkReportCover1w']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_con17")