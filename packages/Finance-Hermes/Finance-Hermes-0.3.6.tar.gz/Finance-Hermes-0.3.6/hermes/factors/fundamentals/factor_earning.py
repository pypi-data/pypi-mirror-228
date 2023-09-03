# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from alphakit.const import *
from alphakit.factor import *
from alphakit.portfolio import *
from alphakit.data import *

from hermes.factors.base import FactorBase, LongCallMixin, ShortCallMixin


class FactorEarning(FactorBase, LongCallMixin, ShortCallMixin):

    def __init__(self, data_format, **kwargs):
        __str__ = 'factor_earning'
        self.category = 'Earning'
        self.name = '盈利因子'
        self._data_format = data_format
        self._data = self.init_data(**kwargs) if 'end_date' in kwargs else None

    def _init_self(self, **kwargs):
        pass

    def factor_earning1(
            self,
            data=None,
            dependencies=[
                'dummy120_fst', 'sw1', 'fbqpub_mergeIncome_pnq0',
                'fbqpub_mergeIncome_pnq1', 'fbqpub_mergeIncome_pnq2',
                'fbqpub_mergeIncome_pnq3', 'fbqpub_mergeIncome_pnq4',
                'fbqpub_mergeIncome_pnq5', 'fbqpub_mergeIncome_pnq6',
                'fbqpub_mergeIncome_pnq7', 'isqpub_COGS_pnq0',
                'isqpub_COGS_pnq1', 'isqpub_COGS_pnq2', 'isqpub_COGS_pnq3',
                'isqpub_COGS_pnq4', 'isqpub_COGS_pnq5', 'isqpub_COGS_pnq6',
                'isqpub_COGS_pnq7'
            ],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        qmergeIncome0 = data['fbqpub_mergeIncome_pnq0']
        qmergeIncome1 = data['fbqpub_mergeIncome_pnq1']
        qmergeIncome2 = data['fbqpub_mergeIncome_pnq2']
        qmergeIncome3 = data['fbqpub_mergeIncome_pnq3']
        qmergeIncome4 = data['fbqpub_mergeIncome_pnq4']
        qmergeIncome5 = data['fbqpub_mergeIncome_pnq5']
        qmergeIncome6 = data['fbqpub_mergeIncome_pnq6']
        qmergeIncome7 = data['fbqpub_mergeIncome_pnq7']
        qcogs0 = data['isqpub_COGS_pnq0']
        qcogs1 = data['isqpub_COGS_pnq1']
        qcogs2 = data['isqpub_COGS_pnq2']
        qcogs3 = data['isqpub_COGS_pnq3']
        qcogs4 = data['isqpub_COGS_pnq4']
        qcogs5 = data['isqpub_COGS_pnq5']
        qcogs6 = data['isqpub_COGS_pnq6']
        qcogs7 = data['isqpub_COGS_pnq7']
        sw1 = data['sw1']
        tradingday = sw1.index
        ticker = sw1.columns
        dfall1 = pd.concat([
            qmergeIncome0.unstack(),
            qmergeIncome1.unstack(),
            qmergeIncome2.unstack(),
            qmergeIncome3.unstack(),
            qmergeIncome4.unstack(),
            qmergeIncome5.unstack(),
            qmergeIncome6.unstack(),
            qmergeIncome7.unstack()
        ],
                           axis=1)
        dfall2 = pd.concat([
            qcogs0.unstack(),
            qcogs1.unstack(),
            qcogs2.unstack(),
            qcogs3.unstack(),
            qcogs4.unstack(),
            qcogs5.unstack(),
            qcogs6.unstack(),
            qcogs7.unstack()
        ],
                           axis=1)

        v = dfall1.std(axis=1)
        v[v == 0] = np.nan
        df1 = dfall1.sub(dfall1.mean(axis=1), axis='rows').div(v, axis='rows')
        v = dfall2.std(axis=1)
        v[v == 0] = np.nan
        df2 = dfall2.sub(dfall2.mean(axis=1), axis='rows').div(v, axis='rows')
        df1.columns = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8']  # x
        df2.columns = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8']  # y
        b = (df1 * df2).sum(axis=1) / (df2 * df2).sum(axis=1)
        f = df1['q1'] - df2['q1'] * b
        f.name = 'factor'
        factor = pd.DataFrame(f).reset_index().pivot_table(index='trade_date',
                                                           columns='code',
                                                           values='factor')
        factor = factor.reindex(index=tradingday, columns=ticker)
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning1")

    def factor_earning2(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'marketValue',
                            'isqpub_tRevenue_pnq0', 'sw1'
                        ],
                        window=1):
        data = self._data if data is None else data
        qtRevenue0 = data['isqpub_tRevenue_pnq0']
        dummy = data['dummy120_fst']
        mktcap = data['marketValue']
        sw1 = data['sw1']
        f = factor_score(qtRevenue0 * dummy, 1).rank(pct=True, axis=1) - 0.5
        dfall = pd.DataFrame(mktcap.unstack(), columns=['mktcap'])
        out1 = alphaOpNeu(f, dfall)
        factor = standardize(factor_score(indLineNeu(out1, sw1), 3))
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning2")

    def factor_earning3(
            self,
            data=None,
            dependencies=[
                'dummy120_fst', 'sw1', 'fbqpub_mergeProfit_pnq0',
                'fbqpub_mergeProfit_pnq1', 'fbqpub_mergeProfit_pnq2',
                'fbqpub_mergeProfit_pnq3', 'fbqpub_mergeProfit_pnq4',
                'fbqpub_mergeProfit_pnq5', 'fbqpub_mergeProfit_pnq6',
                'fbqpub_mergeProfit_pnq7', 'fbqpub_mergeEbt_pnq0',
                'fbqpub_mergeEbt_pnq4', 'isqpub_tRevenue_pnq0',
                'isqpub_tRevenue_pnq4', 'cfqpub_cFRSaleGS_pnq0',
                'cfqpub_cFRSaleGS_pnq4', 'isqpub_finanExp_pnq0',
                'isqpub_finanExp_pnq4'
            ],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        qcFRSaleGS0 = data['cfqpub_cFRSaleGS_pnq0']
        qcFRSaleGS4 = data['cfqpub_cFRSaleGS_pnq4']
        qmergeEbt0 = data['fbqpub_mergeEbt_pnq0']
        qmergeEbt4 = data['fbqpub_mergeEbt_pnq4']
        qfinanExp0 = data['isqpub_finanExp_pnq0']
        qfinanExp4 = data['isqpub_finanExp_pnq4']
        qtRevenue0 = data['isqpub_tRevenue_pnq0']
        qtRevenue4 = data['isqpub_tRevenue_pnq4']
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        qmergeprofit1 = data['fbqpub_mergeProfit_pnq1']
        qmergeprofit2 = data['fbqpub_mergeProfit_pnq2']
        qmergeprofit3 = data['fbqpub_mergeProfit_pnq3']
        qmergeprofit4 = data['fbqpub_mergeProfit_pnq4']
        qmergeprofit5 = data['fbqpub_mergeProfit_pnq5']
        qmergeprofit6 = data['fbqpub_mergeProfit_pnq6']
        qmergeprofit7 = data['fbqpub_mergeProfit_pnq7']
        sw1 = data['sw1']
        tradingday = sw1.index
        ticker = sw1.columns

        alpha_np = qmergeprofit0 / abs(qmergeprofit4)
        alpha_np[np.isinf(alpha_np)] = np.nan
        alpha_np = alpha_np.rank(pct=True, axis=1)
        alpha_cash = qcFRSaleGS0 / abs(qcFRSaleGS4)
        alpha_cash[np.isinf(alpha_cash)] = np.nan
        alpha_cash = alpha_cash.rank(pct=True, axis=1)
        alpha_ebit = qmergeEbt0.add(qfinanExp0, fill_value=0) / qmergeEbt4.add(
            qfinanExp4, fill_value=0)
        alpha_ebit[np.isinf(alpha_ebit)] = np.nan
        alpha_ebit = alpha_ebit.rank(pct=True, axis=1)
        alpha_sales = qtRevenue0 / abs(qtRevenue4)
        alpha_sales[np.isinf(alpha_sales)] = np.nan
        alpha_sales = alpha_sales.rank(pct=True, axis=1)

        f1 = alpha_np.copy()
        f1[:] = np.nan
        f1[(alpha_np > 0.7) & (alpha_sales > 0.7) & (alpha_cash > 0.5)] = 4
        f1[(alpha_np > 0.7) & (alpha_sales > 0.7) & (~(alpha_cash > 0.5))] = 3
        f1[(alpha_np > 0.7) & (~(alpha_sales > 0.7))] = 2
        f1[(alpha_np <= 0.7) & (alpha_np > 0.5) & (alpha_sales > 0.7)] = 1
        f1[(alpha_np <= 0.5) & (alpha_np > 0.3) & (alpha_sales < 0.3)] = -1
        f1[(alpha_np <= 0.3) & (alpha_cash < 0.5) & (alpha_sales < 0.3)] = -4
        f1[(alpha_np <= 0.3) & (~(alpha_cash < 0.5)) &
           (alpha_sales < 0.3)] = -3
        f1[(alpha_np <= 0.3) & (alpha_ebit < 0.3) &
           (~(alpha_sales < 0.3))] = -2
        f1 = f1.rank(pct=True, axis=1) - 0.5

        dfall = pd.concat([
            qmergeprofit0.unstack(),
            qmergeprofit1.unstack(),
            qmergeprofit2.unstack(),
            qmergeprofit3.unstack(),
            qmergeprofit4.unstack(),
            qmergeprofit5.unstack(),
            qmergeprofit6.unstack(),
            qmergeprofit7.unstack(),
        ],
                          axis=1)
        std_value = dfall.std(axis=1).reset_index()
        std_value = std_value.pivot_table(index='trade_date',
                                          columns='code',
                                          values=0)
        std_value = std_value.reindex(index=tradingday, columns=ticker)
        std_value[std_value == 0] = np.nan
        f2 = (qmergeprofit0 - qmergeprofit4) / std_value
        f2 = f2.rank(pct=True, axis=1) - 0.5
        factor = f1.add(f2, fill_value=0)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning3")

    def factor_earning4(self,
                        data=None,
                        dependencies=[
                            'totalShares', 'closePrice', 'sw1', 'dummy120_fst',
                            'd'
                        ],
                        window=3 * 252):
        data = self._data if data is None else data
        d = data['d']
        dummy = data['dummy120_fst']
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        totalShares = data['totalShares']
        closePrice = data['closePrice']
        sw1 = data['sw1']
        dy_q_divout = d.rolling(3 * 252, min_periods=1).sum() / (
            qmergeprofit0.rolling(252 * 3, min_periods=1).sum() /
            totalShares.rolling(3 * 252, min_periods=1).mean())
        dy_q_divout[np.isinf(dy_q_divout)] = np.nan
        dy_q_pe_caldr = closePrice / (4 * qmergeprofit0 / totalShares)
        dy_q_pe_caldr[np.isinf(dy_q_pe_caldr)] = np.nan
        factor = dy_q_divout / dy_q_pe_caldr
        factor[np.isinf(factor)] = np.nan
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning4")

    def factor_earning5(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'marketValue',
                            'fbqpub_mergeProfit_pnq0', 'sw1',
                            'bspub_tEquityAttrP_pnq0'
                        ],
                        window=1):
        data = self._data if data is None else data
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        dummy = data['dummy120_fst']
        mktcap = data['marketValue']
        tEquityAttrP0 = data['bspub_tEquityAttrP_pnq0']
        sw1 = data['sw1']
        roe = qmergeprofit0 / abs(tEquityAttrP0) * dummy
        roe[np.isinf(roe)] = np.nan
        bp = tEquityAttrP0 / mktcap * dummy
        bp[np.isinf(bp)] = np.nan
        factor = roe.rank(pct=True, axis=1) * bp.rank(pct=True, axis=1)
        factor = factor.sub(factor.mean(axis=1), axis='rows')
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning5")

    def factor_earning6(
            self,
            data=None,
            dependencies=[
                'dummy120_fst', 'sw1', 'fbqpub_mergeProfit_pnq0',
                'fbqpub_mergeProfit_pnq1', 'fbqpub_mergeProfit_pnq2',
                'fbqpub_mergeProfit_pnq3', 'fbqpub_mergeProfit_pnq4',
                'fbqpub_mergeProfit_pnq5', 'fbqpub_mergeProfit_pnq6',
                'fbqpub_mergeProfit_pnq7', 'totalShares'
            ],
            window=240):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        totalShares = data['totalShares']
        tradingday = sw1.index
        ticker = sw1.columns
        f0 = data['fbqpub_mergeProfit_pnq0']
        f1 = data['fbqpub_mergeProfit_pnq1']
        f2 = data['fbqpub_mergeProfit_pnq2']
        f3 = data['fbqpub_mergeProfit_pnq3']
        f4 = data['fbqpub_mergeProfit_pnq4']
        f5 = data['fbqpub_mergeProfit_pnq5']
        f6 = data['fbqpub_mergeProfit_pnq6']
        f7 = data['fbqpub_mergeProfit_pnq7']
        dfall = pd.concat([
            f0.unstack(),
            f1.unstack(),
            f2.unstack(),
            f3.unstack(),
            f4.unstack(),
            f5.unstack(),
            f6.unstack(),
            f7.unstack()
        ],
                          axis=1)
        epsall = dfall.div(totalShares.unstack(), axis="rows")
        epsstd = epsall.std(axis=1).reset_index()
        epsstd = epsstd.pivot_table(index="trade_date",
                                    columns="code",
                                    values=0)
        epsstd = epsstd.reindex(index=tradingday, columns=ticker)
        epsstd[epsstd == 0] = np.nan
        epsmean = epsall.mean(axis=1).reset_index()
        epsmean = epsmean.pivot_table(index="trade_date",
                                      columns="code",
                                      values=0)
        epsmean = epsmean.reindex(index=tradingday, columns=ticker)
        eps0 = f0 / totalShares
        f1 = (eps0 - epsmean) / abs(epsstd)
        nistd = dfall.std(axis=1).reset_index()
        nistd = nistd.pivot_table(index="trade_date", columns="code", values=0)
        nistd = nistd.reindex(index=tradingday, columns=ticker)
        nistd[nistd == 0] = np.nan
        nimean = dfall.mean(axis=1).reset_index()
        nimean = nimean.pivot_table(index="trade_date",
                                    columns="code",
                                    values=0)
        nimean = nimean.reindex(index=tradingday, columns=ticker)
        f2 = (f0 - nimean) / abs(nistd)
        f3 = f0.rolling(240, min_periods=120).rank(pct=True)
        factor = factor_merge([f1, f2, f3])
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning6")

    def factor_earning7(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'marketValue',
                            'fbqpub_mergeIncome_pnq0', 'isqpub_COGS_pnq0',
                            'bspub_ltBorr_pnq0', 'sw1', 'marketValue',
                            'bspub_stBorr_pnq0', 'bspub_tradingFa_pnq0',
                            'bspub_cashCEquiv_pnq0'
                        ],
                        window=1):
        data = self._data if data is None else data
        qmergeIncome0 = data['fbqpub_mergeIncome_pnq0']
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        mktcap = data['marketValue']
        qcogs0 = data['isqpub_COGS_pnq0']
        LTBorr0 = data['bspub_ltBorr_pnq0']
        STBorr0 = data['bspub_stBorr_pnq0']
        cashCEquiv0 = data['bspub_cashCEquiv_pnq0']
        tradingFa0 = data['bspub_tradingFa_pnq0']
        gp_now = qmergeIncome0.sub(qcogs0, fill_value=0)
        denom = mktcap.add(STBorr0, fill_value=0).add(
            LTBorr0, fill_value=0).sub(cashCEquiv0,
                                       fill_value=0).sub(tradingFa0,
                                                         fill_value=0)
        denom[denom == 0] = np.nan
        factor = gp_now / denom
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning7")

    def factor_earning8(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst',
                            'marketValue',
                            'cfqpub_cPaidToForEmpl_pnq0',
                            'sw1',
                        ],
                        window=1):
        data = self._data if data is None else data
        qcPaidToForEmpl0 = data['cfqpub_cPaidToForEmpl_pnq0']
        dummy = data['dummy120_fst']
        mktcap = data['marketValue']
        sw1 = data['sw1']
        f = factor_score(qcPaidToForEmpl0 * dummy, 1).rank(pct=True,
                                                           axis=1) - 0.5
        dfall = pd.DataFrame(mktcap.unstack(), columns=['mktcap'])
        dfall.index.names = ['code', 'trade_date']
        out1 = alphaOpNeu(f, dfall)
        factor = standardize(factor_score(indLineNeu(out1, sw1), 3))
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning8")

    def factor_earning9(self,
                        data=None,
                        dependencies=[
                            'dummy120_fst', 'marketValue',
                            'isqpub_bizTaxSurchg_pnq0', 'sw1'
                        ],
                        window=1):
        data = self._data if data is None else data
        qbizTaxSurchg0 = data['isqpub_bizTaxSurchg_pnq0']
        dummy = data['dummy120_fst']
        mktcap = data['marketValue']
        sw1 = data['sw1']
        f = factor_score(qbizTaxSurchg0 * dummy, 1).rank(pct=True,
                                                         axis=1) - 0.5
        dfall = pd.DataFrame(mktcap.unstack(), columns=['mktcap'])
        dfall.index.names = ['code', 'trade_date']
        out1 = alphaOpNeu(f, dfall)
        factor = standardize(factor_score(indLineNeu(out1, sw1), 3))
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning9")

    def factor_earning10(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'isqpub_finanExp_pnq0',
                             'marketValue', 'fbqpub_mergeProfit_pnq0',
                             'fbqpub_mergeEbt_pnq0', 'bspub_tAssets_pnq0',
                             'bspub_tAssets_pnq1', 'bspub_tLiab_pnq0',
                             'bspub_tLiab_pnq1', 'isqpub_tRevenue_pnq0',
                             'isqpub_tRevenue_pnq4', 'isqpub_finanExp_pnq4',
                             'fbqpub_mergeEbt_pnq4', 'bspub_tAssets_pnq4',
                             'bspub_tAssets_pnq5', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        qmergeprofit0 = data['fbqpub_mergeProfit_pnq0']
        qmergeEbt0 = data['fbqpub_mergeEbt_pnq0']
        dummy = data['dummy120_fst']
        mktcap = data['marketValue']
        tAssets0 = data['bspub_tAssets_pnq0']
        tAssets1 = data['bspub_tAssets_pnq1']
        tAssets4 = data['bspub_tAssets_pnq4']
        tAssets5 = data['bspub_tAssets_pnq5']
        tLiab0 = data['bspub_tLiab_pnq0']
        tLiab1 = data['bspub_tLiab_pnq1']
        qfinanExp0 = data['isqpub_finanExp_pnq0']
        qfinanExp4 = data['isqpub_finanExp_pnq4']
        qtRevenue0 = data['isqpub_tRevenue_pnq0']
        qtRevenue4 = data['isqpub_tRevenue_pnq4']
        qmergeEbt4 = data['fbqpub_mergeEbt_pnq4']
        sw1 = data['sw1']
        tradingday = sw1.index
        ticker = sw1.columns
        tax_ratio_vector = qmergeprofit0 / qmergeEbt0
        tax_ratio_vector[np.isinf(tax_ratio_vector)] = np.nan
        eq = (tAssets0.sub(tLiab0,
                           fill_value=0)).add(tAssets1.sub(tLiab1,
                                                           fill_value=0),
                                              fill_value=0)
        roe_ratio_vector = qmergeprofit0 / eq
        roe_ratio_vector[np.isinf(roe_ratio_vector)] = np.nan
        interest_ratio_vector = qmergeEbt0 / (qmergeEbt0.add(qfinanExp0,
                                                             fill_value=0))
        interest_ratio_vector[np.isinf(interest_ratio_vector)] = np.nan
        alpha = tax_ratio_vector.copy()
        alpha[:] = np.nan
        alpha[tax_ratio_vector > 0.9] = roe_ratio_vector[
            tax_ratio_vector > 0.9] / tax_ratio_vector[tax_ratio_vector >
                                                       0.9] * 0.9
        alpha[tax_ratio_vector <= 0.9] = roe_ratio_vector[tax_ratio_vector <=
                                                          0.9]
        alpha[interest_ratio_vector > 0.8] = roe_ratio_vector[
            interest_ratio_vector > 0.8] / interest_ratio_vector[
                interest_ratio_vector > 0.8] * 0.8
        alpha[interest_ratio_vector <= 0.8] = roe_ratio_vector[
            interest_ratio_vector <= 0.8]
        alpha[np.isinf(alpha)] = np.nan
        alpha = alpha.rank(pct=True, axis=1)
        turnover_alpha = qtRevenue0 / tAssets0.add(
            tAssets1, fill_value=0) - qtRevenue4 / tAssets4.add(tAssets5,
                                                                fill_value=0)
        turnover_alpha[np.isinf(turnover_alpha)] = np.nan
        turnover_alpha = turnover_alpha.rank(pct=True, axis=1)
        profit_alpha = qmergeEbt0.add(
            qfinanExp0, fill_value=0) / qtRevenue0 - qmergeEbt4.add(
                qfinanExp4, fill_value=0) / qtRevenue4
        profit_alpha[np.isinf(profit_alpha)] = np.nan
        profit_alpha = profit_alpha.rank(pct=True, axis=1)
        leverage_alpha = tAssets0.add(tAssets1, fill_value=0) / eq
        leverage_alpha[np.isinf(leverage_alpha)] = np.nan

        dfall = pd.concat([leverage_alpha.unstack(), sw1.unstack()], axis=1)
        dfall.columns = ['leverage', 'sw1']
        dfall.reset_index(inplace=True)
        dfall['le'] = dfall.groupby(['trade_date',
                                     'sw1'])['leverage'].rank(pct=True)
        leverage_alpha = dfall.pivot_table(index='trade_date',
                                           columns='code',
                                           values='le')
        leverage_alpha = leverage_alpha.reindex(index=tradingday,
                                                columns=ticker)

        roe_vector = alpha.copy()
        roe_vector[(alpha > 0.5)
                   & ((turnover_alpha > 0.7)
                      | (profit_alpha > 0.7))] = roe_vector[(alpha > 0.5) & (
                          (turnover_alpha > 0.7) | (profit_alpha > 0.7))] + 0.5
        roe_vector[(alpha > 0.5)
                   & (~((turnover_alpha > 0.7) | (profit_alpha > 0.7))) &
                   (leverage_alpha > 0.35)] = np.nan
        roe_vector[(alpha <= 0.5)
                   & ((turnover_alpha < 0.3)
                      | (profit_alpha < 0.3))] = roe_vector[(alpha <= 0.5) & (
                          (turnover_alpha < 0.3) | (profit_alpha < 0.3))] - 0.5
        roe_vector[(alpha <= 0.5)
                   & (~((turnover_alpha < 0.3) | (profit_alpha < 0.3))) &
                   (leverage_alpha < -0.35)] = np.nan

        roe_vector = roe_vector.rank(pct=True, axis=1).unstack()
        asset_vector = mktcap.rank(pct=True, axis=1).unstack()

        dfall = pd.concat([roe_vector, asset_vector, sw1.unstack()], axis=1)
        dfall.columns = ['roe', 'asset', 'sw1']
        dfall.reset_index(inplace=True)
        group_corr1 = dfall.groupby(
            ['trade_date', 'sw1'])[['roe', 'asset']].apply(lambda x: x[
                'roe'].corr(x['asset']) * x['roe'].std() / x['asset'].std())
        group_corr1[np.isinf(group_corr1)] = np.nan
        group_corr1.name = 'group_corr1'
        dfall = dfall.merge(group_corr1.reset_index(),
                            on=['trade_date', 'sw1'],
                            how='left')

        dfall['inter'] = dfall['roe'] - dfall['group_corr1'] * dfall['asset']
        group_intercept1 = dfall.groupby(['trade_date', 'sw1'])['inter'].mean()
        group_intercept1.name = 'group_intercept1'
        dfall = dfall.merge(group_intercept1.reset_index(),
                            on=['trade_date', 'sw1'],
                            how='left')
        dfall['factor'] = dfall['roe'] - dfall['group_corr1'] * dfall[
            'asset'] - dfall['group_intercept1']
        factor = dfall.pivot_table(index='trade_date',
                                   columns='code',
                                   values='factor')
        factor = factor.reindex(index=tradingday, columns=ticker)
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning10")

    def factor_earning11(self,
                         data=None,
                         dependencies=['dummy120_fst', 'ffancy_aiSude', 'sw1'],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['ffancy_aiSude']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning11")

    def factor_earning12(self,
                         data=None,
                         dependencies=['dummy120_fst', 'ffancy_lpnpQ', 'sw1'],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['ffancy_lpnpQ']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning12")

    def factor_earning13(self,
                         data=None,
                         dependencies=['dummy120_fst', 'ffancy_rrocQ', 'sw1'],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['ffancy_rrocQ']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning13")

    def factor_earning14(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'bspub_tAssets_pnq0',
                             'ispub_rDExp_pnq0', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        f0 = data['ispub_rDExp_pnq0']
        tAssets0 = data['bspub_tAssets_pnq0']
        factor = f0 / tAssets0
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning14")

    def factor_earning15(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'bspub_tAssets_pnq0',
                             'fbqpub_mergeOprofit_pnq0', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        f0 = data['fbqpub_mergeOprofit_pnq0']
        tAssets0 = data['bspub_tAssets_pnq0']
        factor = f0 / tAssets0
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning15")

    def factor_earning16(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'bspub_tAssets_pnq0',
                             'fbqpub_mergeProfit_pnq0', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        f0 = data['fbqpub_mergeProfit_pnq0']
        tAssets0 = data['bspub_tAssets_pnq0']
        factor = f0 / tAssets0
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning16")

    def factor_earning17(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'bspub_tAssets_pnq0',
                             'isqpub_tComprIncome_pnq0', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        f0 = data['isqpub_tComprIncome_pnq0']
        tAssets0 = data['bspub_tAssets_pnq0']
        factor = f0 / tAssets0
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning17")

    def factor_earning18(self,
                         data=None,
                         dependencies=[
                             'dummy120_fst', 'totalShares',
                             'isqpub_tComprIncome_pnq0', 'sw1'
                         ],
                         window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        f0 = data['isqpub_tComprIncome_pnq0']
        totalShares = data['totalShares']
        factor = f0 / totalShares
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning18")

    def factor_earning19(
            self,
            data=None,
            dependencies=['dummy120_fst', 'isqpub_dilutedEps_pnq0', 'sw1'],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        factor = data['isqpub_dilutedEps_pnq0']
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning19")

    def factor_earning20(
            self,
            data=None,
            dependencies=[
                'dummy120_fst', 'sw1', 'fbpub_mergeProfit_pnq0',
                'fbpub_mergeProfit_pnq1', 'fbpub_mergeProfit_pnq2',
                'fbpub_mergeProfit_pnq3', 'fbpub_mergeProfit_pnq4',
                'fbpub_mergeProfit_pnq5', 'fbpub_mergeProfit_pnq6',
                'fbpub_mergeProfit_pnq7', 'fbpub_mergeProfit_pnq8',
                'fbpub_mergeProfit_pnq9', 'fbpub_mergeProfit_pnq10',
                'fbpub_mergeProfit_pnq11'
            ],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        tradingday = sw1.index
        ticker = sw1.columns
        f0 = data['fbpub_mergeProfit_pnq0']
        f1 = data['fbpub_mergeProfit_pnq1']
        f2 = data['fbpub_mergeProfit_pnq2']
        f3 = data['fbpub_mergeProfit_pnq3']
        f4 = data['fbpub_mergeProfit_pnq4']
        f5 = data['fbpub_mergeProfit_pnq5']
        f6 = data['fbpub_mergeProfit_pnq6']
        f7 = data['fbpub_mergeProfit_pnq7']
        f8 = data['fbpub_mergeProfit_pnq8']
        f9 = data['fbpub_mergeProfit_pnq9']
        f10 = data['fbpub_mergeProfit_pnq10']
        f11 = data['fbpub_mergeProfit_pnq11']
        dfall = pd.concat([
            f0.unstack(),
            f1.unstack(),
            f2.unstack(),
            f3.unstack(),
            f4.unstack(),
            f5.unstack(),
            f6.unstack(),
            f7.unstack(),
            f8.unstack(),
            f9.unstack(),
            f10.unstack(),
            f11.unstack()
        ],
                          axis=1)
        dfstd = dfall.std(axis=1).reset_index()
        dfstd = dfstd.pivot_table(index='trade_date', columns='code', values=0)
        dfstd = dfstd.reindex(index=tradingday, columns=ticker)
        dfstd[dfstd == 0] = np.nan
        factor = -f0 / dfstd
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning20")

    def factor_earning21(
            self,
            data=None,
            dependencies=[
                'dummy120_fst', 'sw1', 'fbqpub_mergeProfit_pnq0',
                'fbqpub_mergeProfit_pnq1', 'fbqpub_mergeProfit_pnq2',
                'fbqpub_mergeProfit_pnq3', 'fbqpub_mergeProfit_pnq4',
                'fbqpub_mergeProfit_pnq5', 'fbqpub_mergeProfit_pnq6',
                'fbqpub_mergeProfit_pnq7', 'fbqpub_mergeProfit_pnq8',
                'fbqpub_mergeProfit_pnq9', 'fbqpub_mergeProfit_pnq10',
                'fbqpub_mergeProfit_pnq11'
            ],
            window=1):
        data = self._data if data is None else data
        dummy = data['dummy120_fst']
        sw1 = data['sw1']
        tradingday = sw1.index
        ticker = sw1.columns
        f0 = data['fbqpub_mergeProfit_pnq0']
        f1 = data['fbqpub_mergeProfit_pnq1']
        f2 = data['fbqpub_mergeProfit_pnq2']
        f3 = data['fbqpub_mergeProfit_pnq3']
        f4 = data['fbqpub_mergeProfit_pnq4']
        f5 = data['fbqpub_mergeProfit_pnq5']
        f6 = data['fbqpub_mergeProfit_pnq6']
        f7 = data['fbqpub_mergeProfit_pnq7']
        f8 = data['fbqpub_mergeProfit_pnq8']
        f9 = data['fbqpub_mergeProfit_pnq9']
        f10 = data['fbqpub_mergeProfit_pnq10']
        f11 = data['fbqpub_mergeProfit_pnq11']
        dfall = pd.concat([
            f0.unstack(),
            f1.unstack(),
            f2.unstack(),
            f3.unstack(),
            f4.unstack(),
            f5.unstack(),
            f6.unstack(),
            f7.unstack(),
            f8.unstack(),
            f9.unstack(),
            f10.unstack(),
            f11.unstack()
        ],
                          axis=1)
        dfstd = dfall.std(axis=1).reset_index()
        dfstd = dfstd.pivot_table(index='trade_date', columns='code', values=0)
        dfstd = dfstd.reindex(index=tradingday, columns=ticker)
        dfstd[dfstd == 0] = np.nan
        factor = f0 / dfstd
        factor = indfill_median(factor * dummy, sw1)
        return self._format(factor, "factor_earning21")
