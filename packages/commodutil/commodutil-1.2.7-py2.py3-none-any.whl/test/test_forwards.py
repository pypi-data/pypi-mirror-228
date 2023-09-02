import os
import unittest

import pandas as pd

from commodutil import forwards


class TestForwards(unittest.TestCase):
    def test_convert_columns_to_date(self):
        df = pd.DataFrame([], columns=["2020J", "2020M", "Test"])
        res = forwards.convert_columns_to_date(df)
        self.assertIn(pd.to_datetime("2020-04-1"), res.columns)

    def test_conv_factor(self):
        res = forwards.convert_contract_to_date("2020F")
        self.assertEqual(res, "2020-1-1")

    def test_quarterly_contracts(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl

        res = forwards.quarterly_contracts(contracts)
        self.assertAlmostEqual(
            res["Q2 2019"].loc[pd.to_datetime("2019-03-20")], 60.18, 2
        )
        self.assertAlmostEqual(
            res["Q3 2019"].loc[pd.to_datetime("2019-06-20")], 56.95, 2
        )
        self.assertAlmostEqual(
            res["Q4 2019"].loc[pd.to_datetime("2019-09-20")], 58.01, 2
        )
        self.assertAlmostEqual(
            res["Q1 2020"].loc[pd.to_datetime("2019-12-19")], 61.09, 2
        )

        self.assertAlmostEqual(
            res["Q2 2020"].loc[pd.to_datetime("2020-03-20")], 23.14, 2
        )

        res_qs = forwards.quarterly_spreads(res)
        self.assertAlmostEqual(
            res_qs["Q1Q2 2020"].loc[pd.to_datetime("2019-12-19")], 1.14, 2
        )
        self.assertAlmostEqual(
            res_qs["Q2Q3 2019"].loc[pd.to_datetime("2019-03-20")], -0.73, 2
        )
        self.assertAlmostEqual(
            res_qs["Q3Q4 2019"].loc[pd.to_datetime("2019-06-20")], 0.07, 2
        )
        self.assertAlmostEqual(
            res_qs["Q4Q1 2020"].loc[pd.to_datetime("2019-09-20")], 0.61, 2
        )

        res_qf = forwards.quarterly_flys(res)
        self.assertAlmostEqual(
            res_qf["Q1Q2Q3 2020"].loc[pd.to_datetime("2019-12-19")], -0.53, 2
        )
        self.assertAlmostEqual(
            res_qf["Q2Q3Q4 2019"].loc[pd.to_datetime("2019-03-20")], -0.66, 2
        )
        self.assertAlmostEqual(
            res_qf["Q3Q4Q1 2019"].loc[pd.to_datetime("2019-06-20")], -0.58, 2
        )
        self.assertAlmostEqual(
            res_qf["Q4Q1Q2 2020"].loc[pd.to_datetime("2019-09-20")], 0.21, 2
        )

    def test_cal_contracts(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl

        res = forwards.cal_contracts(contracts)
        self.assertAlmostEqual(
            res["CAL 2020"].loc[pd.to_datetime("2019-03-20")], 59.53, 2
        )
        self.assertAlmostEqual(
            res["CAL 2021"].loc[pd.to_datetime("2019-03-20")], 57.19, 2
        )

        res = forwards.cal_spreads(res)
        self.assertAlmostEqual(
            res["CAL 2020-2021"].loc[pd.to_datetime("2019-12-19")], 4.77, 2
        )
        self.assertAlmostEqual(
            res["CAL 2021-2022"].loc[pd.to_datetime("2019-03-20")], 1.77, 2
        )

    def test_half_year_contracts(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl

        res = forwards.half_year_contracts(contracts)
        self.assertAlmostEqual(
            res["H1 2019"].loc[pd.to_datetime("2018-03-20")], 58.82, 2
        )
        self.assertAlmostEqual(
            res["H2 2019"].loc[pd.to_datetime("2018-06-20")], 61.21, 2
        )

        self.assertAlmostEqual(
            res["Summer 2019"].loc[pd.to_datetime("2018-03-20")], 57.666, 2
        )
        self.assertAlmostEqual(
            res["Winter 2019"].loc[pd.to_datetime("2018-06-20")], 60.43, 2
        )

        res_hs = forwards.half_year_spreads(res)
        self.assertAlmostEqual(
            res_hs["H1H2 2020"].loc[pd.to_datetime("2018-12-19")], -0.215, 2
        )
        self.assertAlmostEqual(
            res_hs["H2H1 2019"].loc[pd.to_datetime("2018-03-20")], 1.58, 2
        )
        res_hs = forwards.half_year_spreads(res)
        self.assertAlmostEqual(
            res_hs["SummerWinter 2020"].loc[pd.to_datetime("2018-12-19")], -0.2249, 2
        )
        self.assertAlmostEqual(
            res_hs["WinterSummer 2019"].loc[pd.to_datetime("2018-03-20")], 1.505, 2
        )

    def test_timespreads(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl

        res = forwards.time_spreads(contracts, m1=6, m2=12)
        self.assertAlmostEqual(res[2019].loc[pd.to_datetime("2019-01-02")], -1.51, 2)
        self.assertAlmostEqual(res[2019].loc[pd.to_datetime("2019-05-21")], 0.37, 2)

        res = forwards.time_spreads(contracts, m1=12, m2=12)
        self.assertAlmostEqual(res[2019].loc[pd.to_datetime("2019-11-20")], 3.56, 2)
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-03-20")], 2.11, 2)

    def test_timespreads2(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.time_spreads(cl, m1="Q1", m2="Q2")
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-01-02")], -0.33, 2)
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-05-21")], 1.05, 2)

        res = forwards.time_spreads(cl, m1="Q4", m2="Q1")
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-01-02")], -0.25, 2)
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-05-21")], 0.91, 2)

    def test_fly(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.fly(cl, m1=1, m2=2, m3=3)
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-01-03")], -0.02, 2)
        self.assertAlmostEqual(res[2021].loc[pd.to_datetime("2019-05-21")], 0.02, 2)

    def test_fly2(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.fly(cl, m1=12, m2=1, m3=3)
        self.assertAlmostEqual(res[2020].loc[pd.to_datetime("2019-01-03")], 0.06, 2)
        self.assertAlmostEqual(res[2021].loc[pd.to_datetime("2019-05-21")], -0.14, 2)

    def test_fly_quarterly(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl
        contracts = forwards.quarterly_contracts(contracts)
        res = forwards.fly_quarterly(contracts, x=1, y=2, z=3)
        self.assertAlmostEqual(
            res["Q1Q2Q3 2020"].loc[pd.to_datetime("2019-01-03")], -0.073, 3
        )
        self.assertAlmostEqual(
            res["Q1Q2Q3 2021"].loc[pd.to_datetime("2019-05-21")], 0.11, 2
        )

    def test_spread_combinations(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combinations(cl)
        self.assertIn("Q1", res)
        self.assertIn("Q1Q2", res)
        self.assertIn("Calendar", res)
        self.assertIn("JanFeb", res)
        self.assertIn("JanFebMar", res)

    def test_spread_combination_calendar(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "calendar")
        self.assertIsNotNone(res)
        self.assertAlmostEqual(res[2020]["2020-01-02"], 59.174, 3)

    def test_spread_combination_calendar_spread(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "calendar spread")
        self.assertAlmostEqual(res["CAL 2020-2021"]["2020-01-02"], 4.35, 2)

    def test_spread_combination_half_year(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "half year")
        self.assertAlmostEqual(res["H1 2020"]["2019-01-02"], 50.04, 2)

    def test_spread_combination_half_year_spread(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "half year spread")
        self.assertAlmostEqual(res["H1H2 2020"]["2019-01-02"], -0.578, 2)

    def test_spread_combination_quarter(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )
        contracts = cl

        res = forwards.spread_combination(contracts, "q1")
        self.assertAlmostEqual(res["Q1 2020"]["2019-01-02"], 49.88, 2)

    def test_spread_combination_quarter_spread(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "q1q2")
        self.assertAlmostEqual(res["Q1Q2 2020"]["2019-01-02"], -0.33, 2)

        res = forwards.spread_combination(cl, "q1q3")
        self.assertAlmostEqual(res["Q1Q3 2020"]["2019-01-02"], -0.58, 2)

    def test_spread_combination_month(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "jan")
        self.assertAlmostEqual(res["Jan 2020"]["2019-01-02"], 49.77, 2)

    def test_spread_combination_month_spread_janfeb(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "janfeb")
        self.assertAlmostEqual(res["JanFeb 2020"]["2019-01-02"], -0.11, 2)

    def test_spread_combination_month_spread_decjan(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "decjan")
        self.assertAlmostEqual(res["DecJan 2020"]["2019-01-02"], -0.06, 2)

    def test_spread_combination_month_fly(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "janfebmar")
        self.assertAlmostEqual(res["JanFebMar 2020"]["2019-01-02"], 0.0, 2)

    def test_spread_combination_quarter_fly(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(
            os.path.join(dirname, "test_cl.csv"),
            index_col=0,
            parse_dates=True,
            dayfirst=True,
        )

        res = forwards.spread_combination(cl, "q4q1q2")
        self.assertAlmostEqual(res["Q4Q1Q2 2020"]["2019-01-02"], -0.023, 3)


if __name__ == "__main__":
    unittest.main()
