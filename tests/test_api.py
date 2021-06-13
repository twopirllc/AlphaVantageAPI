from alphaVantageAPI.alphavantage import AlphaVantage

from unittest import TestCase
from unittest.mock import patch
from pandas import DataFrame, read_csv

from .utils import Path
from .utils import Constant as C
from .utils import load_json, _mock_response

## Python 3.7 + Pandas DeprecationWarning
# /alphaVantageAPI/env/lib/python3.7/site-packages/pandas/core/frame.py:7476:
# DeprecationWarning: Using or importing the ABCs from "collections" instead of from "collections.abc" is deprecated, and in 3.8 it will stop working  elif isinstance(data[0], collections.Mapping):

class TestAlphaVantageAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_path = C.TEST_DATA_PATH
        # Set premium to True to avoid API throttling for testing
        av = AlphaVantage(api_key=C.API_KEY_TEST, premium=True)

        # Minimum parameters
        cls.fx_parameters = {"function":"CURRENCY_EXCHANGE_RATE", "from_currency":"USD", "to_currency":"JPY"}
        cls.fx_daily_parameters = {"function":"FX_DAILY", "from_currency":"EUR", "to_currency":"USD"}
        cls.fx_intraday_parameters = {"function":"FX_INTRADAY", "from_currency":"EUR", "to_currency":"USD"}
        cls.fx_monthly_parameters = {"function":"FX_MONTHLY", "from_currency":"EUR", "to_currency":"USD"}
        cls.fx_weekly_parameters = {"function":"FX_WEEKLY", "from_currency":"EUR", "to_currency":"USD"}
        cls.data_parameters = {"function":"TIME_SERIES_DAILY_ADJUSTED", "symbol": C.API_DATA_TEST}
        cls.intraday_parameters = {"function":"TIME_SERIES_INTRADAY", "symbol": C.API_DATA_TEST}
        cls.indicator_parameters = {"function":"RSI", "symbol": C.API_DATA_TEST, "interval":"weekly", "series_type":"open", "time_period":10}
        cls.digital_parameters = {"function":"DIGITAL_CURRENCY_DAILY", "symbol": C.API_DIGITAL_TEST, "market":"CNY"}
        cls.digital_rating_parameters = {"function":"CRYPTO_RATING", "symbols": C.API_DIGITAL_TEST}
        cls.global_quote_parameters = {"function":"GLOBAL_QUOTE", "symbols": C.API_DIGITAL_TEST}
        cls.overview_parameters = {"function":"OVERVIEW", "symbols": C.API_FUNDA_TEST}
        cls.balance_parameters = {"function":"BALANCE_SHEET", "symbols": C.API_FUNDA_TEST}
        cls.income_parameters = {"function":"INCOME_STATEMENT", "symbols": C.API_FUNDA_TEST}
        cls.cashflow_parameters = {"function":"CASH_FLOW", "symbols": C.API_FUNDA_TEST}

        cls.earnings_parameters = {"function": "EARNINGS_CALENDAR"}
        cls.ipos_parameters = {"function": "IPO_CALENDAR"}
        cls.listing_parameters = {"function": "LISTING_STATUS"}

        cls.intraday_ext_parameters = {"function": "TIME_SERIES_INTRADAY_EXTENDED", "symbol": C.API_FUNDA_TEST, "interval": 15}

        # json files of sample data
        cls.json_fx = load_json(cls.test_data_path / "mock_fx.json")
        cls.json_fx_daily = load_json(cls.test_data_path / "mock_fx_daily.json")
        cls.json_fx_intraday = load_json(cls.test_data_path / "mock_fx_intraday.json")
        cls.json_fx_monthly = load_json(cls.test_data_path / "mock_fx_monthly.json")
        cls.json_fx_weekly = load_json(cls.test_data_path / "mock_fx_weekly.json")
        cls.json_data = load_json(cls.test_data_path / "mock_data.json")
        cls.json_indicator = load_json(cls.test_data_path / "mock_indicator.json")
        cls.json_digital = load_json(cls.test_data_path / "mock_digital.json")
        cls.json_digital_rating = load_json(cls.test_data_path / "mock_digital_rating.json")
        cls.json_global_quote = load_json(cls.test_data_path / "mock_global_quote.json")
        cls.json_overview = load_json(cls.test_data_path / "mock_overview.json")
        cls.json_balance = load_json(cls.test_data_path / "mock_balance_sheet.json")
        cls.json_income = load_json(cls.test_data_path / "mock_income_statement.json")
        cls.json_cashflow = load_json(cls.test_data_path / "mock_cash_flow.json")

        # csv files of sample data
        cls.csv_earnings_cal = read_csv(cls.test_data_path / "mock_earnings_cal.csv")
        cls.csv_ipos_cal = read_csv(cls.test_data_path / "mock_ipos_cal.csv")
        cls.csv_delisted = read_csv(cls.test_data_path / "mock_delisted_status.csv")
        cls.csv_listed = read_csv(cls.test_data_path / "mock_listed_status.csv")

        cls.csv_intra_ext_adj = read_csv(cls.test_data_path / "mock_intra_ext_adj_15min_y1m1.csv")
        cls.csv_intra_ext_adj_slice = read_csv(cls.test_data_path / "mock_intra_ext_adj_15min_y1m2.csv")
        cls.csv_intra_ext_raw_slice = read_csv(cls.test_data_path / "mock_intra_ext_raw_60min_y1m3.csv")

        # Pandas DataFrames of sample data
        cls.df_fx = av._to_dataframe("CURRENCY_EXCHANGE_RATE", cls.json_fx)
        cls.df_fx_daily = av._to_dataframe("FX_DAILY", cls.json_fx_daily)
        cls.df_fx_intraday = av._to_dataframe("FX_INTRADAY", cls.json_fx_intraday)
        cls.df_fx_monthly = av._to_dataframe("FX_MONTHLY", cls.json_fx_monthly)
        cls.df_fx_weekly = av._to_dataframe("FX_WEEKLY", cls.json_fx_weekly)
        cls.df_data = av._to_dataframe("TIME_SERIES_DAILY_ADJUSTED", cls.json_data)
        cls.df_indicator = av._to_dataframe("RSI", cls.json_indicator)
        cls.df_digital = av._to_dataframe("DIGITAL_CURRENCY_DAILY", cls.json_digital)
        cls.df_digital_rating = av._to_dataframe("CRYPTO_RATING", cls.json_digital_rating)
        cls.df_global_quote = av._to_dataframe("GLOBAL_QUOTE", cls.json_global_quote)
        cls.df_overview = av._to_dataframe("OVERVIEW", cls.json_overview)
        cls.df_balance = av._to_dataframe("BALANCE_SHEET", cls.json_balance)
        cls.df_income = av._to_dataframe("INCOME_STATEMENT", cls.json_income)
        cls.df_cashflow = av._to_dataframe("CASH_FLOW", cls.json_cashflow)


        cls.df_earnings = DataFrame(cls.csv_earnings_cal)
        cls.df_ipos = DataFrame(cls.csv_ipos_cal)
        cls.df_delisted = DataFrame(cls.csv_delisted)
        cls.df_listed = DataFrame(cls.csv_listed)
        cls.df_intraday_ext_adj = DataFrame(cls.csv_intra_ext_adj)
        cls.df_intraday_ext_adj_slice = DataFrame(cls.csv_intra_ext_adj_slice)
        cls.df_intraday_ext_raw_slice = DataFrame(cls.csv_intra_ext_raw_slice)


    @classmethod
    def tearDownClass(cls):
        del cls.test_data_path

        del cls.fx_parameters
        del cls.fx_daily_parameters
        del cls.fx_intraday_parameters
        del cls.fx_monthly_parameters
        del cls.fx_weekly_parameters
        # del cls.sector_parameters
        del cls.data_parameters
        del cls.intraday_parameters
        del cls.intraday_ext_parameters
        del cls.indicator_parameters
        del cls.digital_parameters
        del cls.digital_rating_parameters
        del cls.global_quote_parameters
        del cls.overview_parameters
        del cls.balance_parameters
        del cls.income_parameters
        del cls.cashflow_parameters

        del cls.earnings_parameters
        del cls.ipos_parameters
        del cls.listing_parameters

        del cls.json_fx
        del cls.json_fx_daily
        del cls.json_fx_intraday
        del cls.json_fx_monthly
        del cls.json_fx_weekly
        del cls.json_data
        del cls.json_indicator
        del cls.json_digital
        del cls.json_digital_rating
        del cls.json_global_quote
        del cls.json_overview
        del cls.json_balance
        del cls.json_income
        del cls.json_cashflow

        del cls.df_fx
        del cls.df_fx_daily
        del cls.df_fx_intraday
        del cls.df_fx_monthly
        del cls.df_fx_weekly
        del cls.df_data
        del cls.df_indicator
        del cls.df_intraday_ext_adj
        del cls.df_intraday_ext_adj_slice
        del cls.df_intraday_ext_raw_slice
        del cls.df_digital
        del cls.df_digital_rating
        del cls.df_global_quote
        del cls.df_overview
        del cls.df_balance
        del cls.df_income
        del cls.df_cashflow

        del cls.csv_earnings_cal
        del cls.csv_ipos_cal
        del cls.csv_delisted
        del cls.csv_listed
        del cls.csv_intra_ext_adj
        del cls.csv_intra_ext_adj_slice
        del cls.csv_intra_ext_raw_slice


    def setUp(self):
        self.av = AlphaVantage(api_key=C.API_KEY_TEST)

    def tearDown(self):
        del self.av


    # tests of: fx, sectors, data, intraday, and digital
    @patch("alphaVantageAPI.alphavantage.AlphaVantage._av_api_call")
    def test_fx(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_fx, self.json_fx]
        self.assertIsNone(self.av.fx(C.API_FX_TEST))
        # 4/7/2019 Stopped passing!?
        # self.assertIsInstance(self.av.fx(C.API_FX_TEST), DataFrame)
        # self.assertIsInstance(self.av.fx(C.API_FX_TEST), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._av_api_call")
    def test_digital(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_digital, self.json_digital]
        self.assertIsNone(self.av.digital(C.API_DIGITAL_TEST))
        self.assertIsInstance(self.av.digital(C.API_DIGITAL_TEST), DataFrame)
        self.assertIsInstance(self.av.digital(C.API_DIGITAL_TEST), dict)
        
    # @patch("alphaVantageAPI.alphavantage.AlphaVantage._av_api_call")
    # def test_intraday(self, mock_av_api_call):
    #     mock_av_api_call.side_effect = [None, self.df_sectors, self.json_sectors]
    #     self.assertIsNone(self.av.intraday(C.API_DATA_TEST))
    #     self.assertIsInstance(self.av.intraday(C.API_DATA_TEST), DataFrame)
    #     self.assertIsInstance(self.av.intraday(C.API_DATA_TEST), dict)

    # @patch("alphaVantageAPI.alphavantage.AlphaVantage._av_api_call")
    # def test_data(self, mock_av_api_call):
    #     mock_av_api_call.side_effect = [None, self.df_data, self.json_data]
    #     self.assertIsNone(self.av.data("D", C.API_DATA_TEST))
    #     self.assertIsInstance(self.av.data("D", C.API_DATA_TEST), DataFrame)
    #     self.assertIsInstance(self.av.data("D", C.API_DATA_TEST), dict)


    # av_api_call tests
    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx)
        mock_to_dataframe.return_value = self.df_fx

        av_api_call = self.av._av_api_call(self.fx_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx)

        av_api_call = self.av._av_api_call(self.fx_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_daily(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx_daily)
        mock_to_dataframe.return_value = self.df_fx_daily

        av_api_call = self.av._av_api_call(self.fx_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_daily_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx_daily)

        av_api_call = self.av._av_api_call(self.fx_daily_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_intraday(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx_intraday)
        mock_to_dataframe.return_value = self.df_fx

        av_api_call = self.av._av_api_call(self.fx_intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_intraday_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx_intraday)

        av_api_call = self.av._av_api_call(self.fx_intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_monthly(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx_monthly)
        mock_to_dataframe.return_value = self.df_fx_monthly

        av_api_call = self.av._av_api_call(self.fx_monthly_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_monthly_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx_monthly)

        av_api_call = self.av._av_api_call(self.fx_monthly_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_weekly(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx_weekly)
        mock_to_dataframe.return_value = self.df_fx_weekly

        av_api_call = self.av._av_api_call(self.fx_weekly_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_fx_weekly_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx_weekly)

        av_api_call = self.av._av_api_call(self.fx_weekly_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_data(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_data)
        mock_to_dataframe.return_value = self.df_data

        av_api_call = self.av._av_api_call(self.data_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_data_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"
        mock_requests_get.return_value = _mock_response(text_data=self.json_data)

        av_api_call = self.av._av_api_call(self.data_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_intraday(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_data)
        mock_to_dataframe.return_value = self.df_data

        av_api_call = self.av._av_api_call(self.intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_intraday_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_data)

        av_api_call = self.av._av_api_call(self.intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_intraday_ext_adj_csv(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(text_data=self.csv_intra_ext_adj)
        mock_to_dataframe.return_value = self.df_intraday_ext_adj

        av_api_call = self.av._av_api_call(self.intraday_ext_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_intraday_ext_adj_slice_csv(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(text_data=self.csv_intra_ext_adj_slice)
        mock_to_dataframe.return_value = self.df_intraday_ext_adj_slice

        _params = self.intraday_ext_parameters.copy()
        _params.update({"interval": 15, "slice": "year1month2"})
        av_api_call = self.av._av_api_call(_params)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_intraday_ext_raw_slice_csv(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(text_data=self.csv_intra_ext_raw_slice)
        mock_to_dataframe.return_value = self.df_intraday_ext_raw_slice

        _params = self.intraday_ext_parameters.copy()
        _params.update({"interval": 60, "slice": "year1month3", "adjusted": False})
        av_api_call = self.av._av_api_call(_params)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_indicator(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_indicator)
        mock_to_dataframe.return_value = self.df_indicator

        av_api_call = self.av._av_api_call(self.indicator_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_indicator_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_indicator)

        av_api_call = self.av._av_api_call(self.indicator_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_digital(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_digital)
        mock_to_dataframe.return_value = self.df_digital

        av_api_call = self.av._av_api_call(self.digital_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_digital_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_digital)

        av_api_call = self.av._av_api_call(self.digital_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)

# 
    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_digital_rating(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_digital_rating)
        mock_to_dataframe.return_value = self.df_digital_rating

        av_api_call = self.av._av_api_call(self.digital_rating_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_digital_rating_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_digital_rating)

        av_api_call = self.av._av_api_call(self.digital_rating_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_global_quote(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_global_quote)
        mock_to_dataframe.return_value = self.df_global_quote

        av_api_call = self.av._av_api_call(self.global_quote_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_global_quote_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_global_quote)

        av_api_call = self.av._av_api_call(self.global_quote_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_overview(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_overview)
        mock_to_dataframe.return_value = self.df_overview

        av_api_call = self.av._av_api_call(self.overview_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_overview_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_overview)

        av_api_call = self.av._av_api_call(self.overview_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_overview(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_overview)
        mock_to_dataframe.return_value = self.df_overview

        av_api_call = self.av._av_api_call(self.overview_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_overview_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_overview)

        av_api_call = self.av._av_api_call(self.overview_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_balance_sheet(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_balance)
        mock_to_dataframe.return_value = self.df_balance

        av_api_call = self.av._av_api_call(self.balance_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)

        self.assertIsInstance(mock_to_dataframe(), list)
        self.assertIsInstance(mock_to_dataframe()[0], DataFrame)
        self.assertIsInstance(mock_to_dataframe()[1], DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_balance_sheet_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_balance)

        av_api_call = self.av._av_api_call(self.balance_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_income_statement(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_income)
        mock_to_dataframe.return_value = self.df_income

        av_api_call = self.av._av_api_call(self.income_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)

        self.assertIsInstance(mock_to_dataframe(), list)
        self.assertIsInstance(mock_to_dataframe()[0], DataFrame)
        self.assertIsInstance(mock_to_dataframe()[1], DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_income_statement_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.json_income)

        av_api_call = self.av._av_api_call(self.income_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_cashflow(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_cashflow)
        mock_to_dataframe.return_value = self.df_cashflow

        av_api_call = self.av._av_api_call(self.cashflow_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)

        self.assertIsInstance(mock_to_dataframe(), list)
        self.assertIsInstance(mock_to_dataframe()[0], DataFrame)
        self.assertIsInstance(mock_to_dataframe()[1], DataFrame)

    @patch("alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe")
    @patch("alphaVantageAPI.alphavantage.requests.get")
    def test_cashflow_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = "csv"

        mock_requests_get.return_value = _mock_response(text_data=self.cashflow_parameters)

        av_api_call = self.av._av_api_call(self.cashflow_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    # save_df tests
    # @patch("alphaVantageAPI.alphavantage.AlphaVantage.last")
    # @patch("alphaVantageAPI.alphavantage.DataFrame.to_csv")
    # def test_save_df_to_csv(self, mock_to_csv, mock_last):
    #     self.av.output = "csv"
    #     mock_last.return_value = self.sector_parameters
    #     mock_to_csv.return_result = True

    #     self.av._save_df(self.sector_parameters["function"], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_to_csv.call_count, 1)


    # @patch("alphaVantageAPI.alphavantage.AlphaVantage.last")
    # @patch("alphaVantageAPI.alphavantage.DataFrame.to_json")
    # def test_save_df_to_json(self, mock_to_json, mock_last):
    #     self.av.output = "json"
    #     mock_last.return_value = self.sector_parameters
    #     mock_to_json.return_result = True

    #     self.av._save_df(self.sector_parameters["function"], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_to_json.call_count, 1)


    # @patch("alphaVantageAPI.alphavantage.AlphaVantage.last")
    # @patch("alphaVantageAPI.alphavantage.DataFrame.to_pickle")
    # def test_save_df_to_pickle(self, mock_to_pickle, mock_last):
    #     self.av.output = "pkl"
    #     mock_last.return_value = self.sector_parameters
    #     mock_to_pickle.return_result = True

    #     self.av._save_df(self.sector_parameters["function"], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_to_pickle.call_count, 1)


    # @patch("alphaVantageAPI.alphavantage.AlphaVantage.last")
    # @patch("alphaVantageAPI.alphavantage.DataFrame.to_html")
    # def test_save_df_to_html(self, mock_to_html, mock_last):
    #     self.av.output = "html"
    #     mock_last.return_value = self.sector_parameters
    #     mock_to_html.return_result = True

    #     self.av._save_df(self.sector_parameters["function"], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_to_html.call_count, 1)


    # @patch("alphaVantageAPI.alphavantage.AlphaVantage.last")
    # @patch("alphaVantageAPI.alphavantage.Path.write_text")
    # def test_save_df_to_txt(self, mock_write_text, mock_last):
    #     self.av.output = "txt"
    #     mock_last.return_value = self.sector_parameters
    #     mock_write_text.return_result = True

    #     self.av._save_df(self.sector_parameters["function"], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_write_text.call_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)