from alphaVantageAPI.alphavantage import AlphaVantage

from unittest import TestCase
from unittest.mock import patch
from pandas import DataFrame

from .utils import Path
from .utils import Constant as C
from .utils import load_json, _mock_response

## Python 3.7 + Pandas DeprecationWarning
# /alphaVantageAPI/env/lib/python3.7/site-packages/pandas/core/frame.py:7476:
# DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working  elif isinstance(data[0], collections.Mapping):

class TestAlphaVantageAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_path = C.TEST_DATA_PATH
        # Set premium to True to avoid API throttling for testing
        av = AlphaVantage(api_key=C.API_KEY_TEST, premium=True)

        # Minimum parameters
        cls.batch_parameters = {'function':'BATCH_STOCK_QUOTES', 'symbols':C.API_BATCH_TEST}
        cls.fx_parameters = {'function':'CURRENCY_EXCHANGE_RATE', 'from_currency':'USD', 'to_currency':'JPY'}
        cls.sector_parameters = {'function':'SECTOR'}
        cls.data_parameters = {'function':'TIME_SERIES_DAILY_ADJUSTED', 'symbol':C.API_DATA_TEST}
        cls.intraday_parameters = {'function':'TIME_SERIES_INTRADAY', 'symbol':C.API_DATA_TEST}
        cls.indicator_parameters = {'function':'RSI', 'symbol':C.API_DATA_TEST, 'interval':'weekly', 'series_type':'open', 'time_period':10}
        cls.digital_parameters = {'function':'DIGITAL_CURRENCY_DAILY', 'symbol':C.API_DIGITAL_TEST, 'market':'CNY'}

        # json files of sample data
        cls.json_batch = load_json(cls.test_data_path / 'mock_batch.json')
        cls.json_fx = load_json(cls.test_data_path / 'mock_fx.json')
        cls.json_sectors = load_json(cls.test_data_path / 'mock_sectors.json')
        cls.json_data = load_json(cls.test_data_path / 'mock_data.json')
        cls.json_indicator = load_json(cls.test_data_path / 'mock_indicator.json')
        cls.json_digital = load_json(cls.test_data_path / 'mock_digital.json')

        # Pandas DataFrames of sample data
        cls.df_batch = av._to_dataframe('BATCH_STOCK_QUOTES', cls.json_batch)
        cls.df_fx = av._to_dataframe('CURRENCY_EXCHANGE_RATE', cls.json_fx)
        cls.df_sectors = av._to_dataframe('SECTOR', cls.json_sectors)
        cls.df_data = av._to_dataframe('TIME_SERIES_DAILY_ADJUSTED', cls.json_data)
        cls.df_indicator = av._to_dataframe('RSI', cls.json_indicator)
        cls.df_digital = av._to_dataframe('DIGITAL_CURRENCY_DAILY', cls.json_digital)


    @classmethod
    def tearDownClass(cls):
        del cls.test_data_path

        del cls.batch_parameters
        del cls.fx_parameters
        del cls.sector_parameters
        del cls.data_parameters
        del cls.intraday_parameters
        del cls.indicator_parameters
        del cls.digital_parameters

        del cls.json_batch
        del cls.json_fx
        del cls.json_sectors
        del cls.json_data
        del cls.json_indicator
        del cls.json_digital

        del cls.df_batch
        del cls.df_fx
        del cls.df_sectors
        del cls.df_data
        del cls.df_indicator
        del cls.df_digital


    def setUp(self):
        self.av = AlphaVantage(api_key=C.API_KEY_TEST)

    def tearDown(self):
        del self.av


    # tests of: batch, fx, sectors, data, intraday, and digital
    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_batch(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_batch, self.json_batch]
        self.assertIsNone(self.av.batch(C.API_BATCH_TEST))
        self.assertIsInstance(self.av.batch(C.API_BATCH_TEST), DataFrame)
        self.assertIsInstance(self.av.batch(C.API_BATCH_TEST), dict)

    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_fx(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_fx, self.json_fx]
        self.assertIsNone(self.av.fx(C.API_FX_TEST))
        self.assertIsInstance(self.av.fx(C.API_FX_TEST), DataFrame)
        self.assertIsInstance(self.av.fx(C.API_FX_TEST), dict)

    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_sectors(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_sectors, self.json_sectors]
        self.assertIsNone(self.av.sectors())
        self.assertIsInstance(self.av.sectors(), DataFrame)
        self.assertIsInstance(self.av.sectors(), dict)

    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_digital(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_digital, self.json_digital]
        self.assertIsNone(self.av.digital(C.API_DIGITAL_TEST))
        self.assertIsInstance(self.av.digital(C.API_DIGITAL_TEST), DataFrame)
        self.assertIsInstance(self.av.digital(C.API_DIGITAL_TEST), dict)
        
    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_intraday(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_sectors, self.json_sectors]
        self.assertIsNone(self.av.intraday(C.API_DATA_TEST))
        self.assertIsInstance(self.av.intraday(C.API_DATA_TEST), DataFrame)
        self.assertIsInstance(self.av.intraday(C.API_DATA_TEST), dict)

    @patch('alphaVantageAPI.alphavantage.AlphaVantage._av_api_call')
    def test_data(self, mock_av_api_call):
        mock_av_api_call.side_effect = [None, self.df_data, self.json_data]
        self.assertIsNone(self.av.data('D', C.API_DATA_TEST))
        self.assertIsInstance(self.av.data('D', C.API_DATA_TEST), DataFrame)
        self.assertIsInstance(self.av.data('D', C.API_DATA_TEST), dict)


    # av_api_call tests
    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_batch(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_batch)
        mock_to_dataframe.return_value = self.df_batch

        av_api_call = self.av._av_api_call(self.batch_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_batch_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_batch)

        av_api_call = self.av._av_api_call(self.batch_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_fx(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_fx)
        mock_to_dataframe.return_value = self.df_fx

        av_api_call = self.av._av_api_call(self.fx_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_fx_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_fx)

        av_api_call = self.av._av_api_call(self.fx_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_sectors(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_sectors)
        mock_to_dataframe.return_value = self.df_sectors

        av_api_call = self.av._av_api_call(self.sector_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_sectors_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_sectors)

        av_api_call = self.av._av_api_call(self.sector_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_data(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_data)
        mock_to_dataframe.return_value = self.df_data

        av_api_call = self.av._av_api_call(self.data_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_data_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'
        mock_requests_get.return_value = _mock_response(text_data=self.json_data)

        av_api_call = self.av._av_api_call(self.data_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_intraday(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_data)
        mock_to_dataframe.return_value = self.df_data

        av_api_call = self.av._av_api_call(self.intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_intraday_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_data)

        av_api_call = self.av._av_api_call(self.intraday_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_indicator(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_indicator)
        mock_to_dataframe.return_value = self.df_indicator

        av_api_call = self.av._av_api_call(self.indicator_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_indicator_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_indicator)

        av_api_call = self.av._av_api_call(self.indicator_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_digital(self, mock_requests_get, mock_to_dataframe):
        mock_requests_get.return_value = _mock_response(json_data=self.json_digital)
        mock_to_dataframe.return_value = self.df_digital

        av_api_call = self.av._av_api_call(self.digital_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 1)
        self.assertIsInstance(mock_to_dataframe(), DataFrame)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage._to_dataframe')
    @patch('alphaVantageAPI.alphavantage.requests.get')
    def test_av_api_call_digital_csv(self, mock_requests_get, mock_to_dataframe):
        self.av.datatype = 'csv'

        mock_requests_get.return_value = _mock_response(text_data=self.json_digital)

        av_api_call = self.av._av_api_call(self.digital_parameters)

        self.assertEqual(mock_requests_get.call_count, 1)
        self.assertEqual(mock_to_dataframe.call_count, 0)
        self.assertIsInstance(av_api_call(), dict)



    # save_df tests
    @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    @patch('alphaVantageAPI.alphavantage.DataFrame.to_csv')
    def test_save_df_to_csv(self, mock_to_csv, mock_last):
        self.av.output = 'csv'
        mock_last.return_value = self.sector_parameters
        mock_to_csv.return_result = True

        self.av._save_df(self.sector_parameters['function'], self.df_sectors)

        self.assertEqual(mock_last.call_count, 1)
        self.assertEqual(mock_to_csv.call_count, 1)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    @patch('alphaVantageAPI.alphavantage.DataFrame.to_json')
    def test_save_df_to_json(self, mock_to_json, mock_last):
        self.av.output = 'json'
        mock_last.return_value = self.sector_parameters
        mock_to_json.return_result = True

        self.av._save_df(self.sector_parameters['function'], self.df_sectors)

        self.assertEqual(mock_last.call_count, 1)
        self.assertEqual(mock_to_json.call_count, 1)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    @patch('alphaVantageAPI.alphavantage.DataFrame.to_pickle')
    def test_save_df_to_pickle(self, mock_to_pickle, mock_last):
        self.av.output = 'pkl'
        mock_last.return_value = self.sector_parameters
        mock_to_pickle.return_result = True

        self.av._save_df(self.sector_parameters['function'], self.df_sectors)

        self.assertEqual(mock_last.call_count, 1)
        self.assertEqual(mock_to_pickle.call_count, 1)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    @patch('alphaVantageAPI.alphavantage.DataFrame.to_html')
    def test_save_df_to_html(self, mock_to_html, mock_last):
        self.av.output = 'html'
        mock_last.return_value = self.sector_parameters
        mock_to_html.return_result = True

        self.av._save_df(self.sector_parameters['function'], self.df_sectors)

        self.assertEqual(mock_last.call_count, 1)
        self.assertEqual(mock_to_html.call_count, 1)


    @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    @patch('alphaVantageAPI.alphavantage.Path.write_text')
    def test_save_df_to_txt(self, mock_write_text, mock_last):
        self.av.output = 'txt'
        mock_last.return_value = self.sector_parameters
        mock_write_text.return_result = True

        self.av._save_df(self.sector_parameters['function'], self.df_sectors)

        self.assertEqual(mock_last.call_count, 1)
        self.assertEqual(mock_write_text.call_count, 1)


    # @patch('alphaVantageAPI.alphavantage.AlphaVantage.last')
    # @patch('alphaVantageAPI.alphavantage.DataFrame.to_excel')
    # def test_save_df_to_excel(self, mock_to_excel, mock_last):
    #     self.av.output = 'xlsx'
    #     mock_last.return_value = self.sector_parameters
    #     mock_to_excel.return_result = True

    #     self.av._save_df(self.sector_parameters['function'], self.df_sectors)

    #     self.assertEqual(mock_last.call_count, 1)
    #     self.assertEqual(mock_to_excel.call_count, 1)



if __name__ == '__main__':
    unittest.main(verbosity=2)