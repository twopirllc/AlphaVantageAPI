from alphaVantageAPI.alphavantage import AlphaVantage

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from .utils import Path
from .utils import Constant as C

class TestAlphaVantageAPIProperties(TestCase):
    def setUp(self):
        self.API_KEY_TEST = C.API_KEY_TEST
        self.av = AlphaVantage(api_key = self.API_KEY_TEST)


    @patch('os.getenv')
    @patch('sys.exit')
    def test_apikey(self, mock_sys_exit, mock_os_getenv):
        self.assertEqual(self.API_KEY_TEST, 'demo')

        mock_os_getenv.return_value = None
        self.av.api_key = None
        self.assertIsNone(self.av.api_key)

        mock_sys_exit.return_value = True
        self.av.api_key = 13
        self.assertIsNone(self.av.api_key)
        self.assertTrue(mock_sys_exit)
        self.assertEqual(mock_sys_exit.call_count, 1)

        # How to mock the print())?


    def test_export_property(self):
        self.av.export = True
        self.assertTrue(self.av.export)

        self.av.export = False
        self.assertFalse(self.av.export)


    def test_export_path_property(self):
        self.av.export_path = None
        self.assertIsInstance(self.av.export_path, Path)

        self.av.export_path = ''
        self.assertIsInstance(self.av.export_path, Path)

        subdir = 'av_test'
        self.av.export_path = '~/{}'.format(subdir)
        self.assertIsInstance(self.av.export_path, Path)
        self.assertEqual(str(self.av.export_path), str(Path().home() / subdir))

        self.av.export_path = '/tmp/av_test'
        self.assertIsInstance(self.av.export_path, Path)


    def test_output_size_property(self):
        full = 'full'
        self.av.output_size = full
        self.assertEqual(self.av.output_size, full)

        compact = 'compact'
        self.av.output_size = compact
        self.assertEqual(self.av.output_size, compact)

        compact = 'compacT'
        self.av.output_size = compact
        self.assertEqual(self.av.output_size, compact.lower())

        other = None
        self.av.output_size = other
        self.assertEqual(self.av.output_size, 'compact')


    def test_output_property(self):
        json = 'json'
        self.av.output = json
        self.assertEqual(self.av.output, json)

        csv = 'csv'
        self.av.output = csv
        self.assertEqual(self.av.output, csv)

        other = 'other'
        self.av.output = other
        self.assertNotEqual(self.av.output, other)
        self.assertEqual(self.av.output, csv)


    def test_datatype_property(self):
        csv = 'csv'
        self.av.datatype = csv
        self.assertEqual(self.av.datatype, csv)

        json = 'json'
        self.av.datatype = json
        self.assertEqual(self.av.datatype, json)

        other = 'other'
        self.av.datatype = other
        self.assertEqual(self.av.datatype, json)


    def test_proxy_property(self):
        self.assertIsInstance(self.av.proxy, dict)

        self.av.proxy = None
        self.assertIsNotNone(self.av.proxy)
        self.assertIsInstance(self.av.proxy, dict)


    def test_clean_property(self):
        self.av.clean = True
        self.assertTrue(self.av.clean)

        self.av.clean = False
        self.assertFalse(self.av.clean)


    def test_api_initial_parameters(self):
        self.assertIsInstance(self.av.api_key, str)
        self.assertEqual(self.av.api_key, self.API_KEY_TEST)

        self.assertIsInstance(self.av.output_size, str)
        self.assertEqual(self.av.output_size, 'compact')

        self.assertIsInstance(self.av.datatype, str)
        self.assertEqual(self.av.datatype, 'json')

        self.assertIsInstance(self.av.export, bool)
        self.assertEqual(self.av.export, False)

        self.assertIsInstance(self.av.export_path, Path)
        self.assertEqual(self.av.export_path, Path().home() / 'av_data')

        self.assertIsInstance(self.av.output, str)
        self.assertEqual(self.av.output, 'csv')


    @patch('alphaVantageAPI.alphavantage.AlphaVantage.export_path')
    def test_init_export_path_method(self, mock_export_path):
        mock_export_path.side_effect = [OSError, PermissionError]

        self.assertRaises(OSError, mock_export_path)
        self.assertRaises(PermissionError, mock_export_path)
        

    def test_parameters_method(self):
        self.assertIsInstance(self.av._parameters('TIME_SERIES_INTRADAY', 'required'), list)
        self.assertIsInstance(self.av._parameters('TIME_SERIES_INTRADAY', 'optional'), list)

        self.assertIsInstance(self.av._parameters('SMA', 'required'), list)
        self.assertIsInstance(self.av._parameters('SMA', 'optional'), list)


    def test_function_alias_method(self):
        self.assertEqual(self.av._function_alias('TIME_SERIES_INTRADAY'), 'I')

        self.assertEqual(self.av._function_alias('TIME_SERIES_DAILY'), 'D')
        self.assertEqual(self.av._function_alias('TIME_SERIES_DAILY_ADJUSTED'), 'DA')

        self.assertEqual(self.av._function_alias('TIME_SERIES_WEEKLY'), 'W')
        self.assertEqual(self.av._function_alias('TIME_SERIES_WEEKLY_ADJUSTED'), 'WA')

        self.assertEqual(self.av._function_alias('TIME_SERIES_MONTHLY'), 'M')
        self.assertEqual(self.av._function_alias('TIME_SERIES_MONTHLY_ADJUSTED'), 'MA')

        self.assertEqual(self.av._function_alias('DIGITAL_CURRENCY_INTRADAY'), 'CI')
        self.assertEqual(self.av._function_alias('DIGITAL_CURRENCY_DAILY'), 'CD')
        self.assertEqual(self.av._function_alias('DIGITAL_CURRENCY_WEEKLY'), 'CW')
        self.assertEqual(self.av._function_alias('DIGITAL_CURRENCY_MONTHLY'), 'CM')

        self.assertEqual(self.av._function_alias('BATCH_STOCK_QUOTES'), 'B')

        self.assertEqual(self.av._function_alias('CURRENCY_EXCHANGE_RATE'), 'FX')

        self.assertEqual(self.av._function_alias('SECTOR'), 'S')

        self.assertEqual(self.av._function_alias('SMA'), 'SMA')
        self.assertEqual(self.av._function_alias('DEMA'), 'DEMA')
        ### and more indicators ...

        self.assertEqual(self.av._function_alias('Qwerty'), 'Qwerty')


    def test_configure_mock(self):
        mock = Mock(foo='bar')
        self.assertEqual(mock.foo, 'bar')

        mock = MagicMock(foo='bar')
        self.assertEqual(mock.foo, 'bar')

        kwargs = {'side_effect': KeyError, 'foo.bar.return_value': 33,
            'foo': MagicMock()}
        mock = Mock(**kwargs)
        self.assertRaises(KeyError, mock)
        self.assertEqual(mock.foo.bar(), 33)
        self.assertIsInstance(mock.foo, MagicMock)

        mock = Mock()
        mock.configure_mock(**kwargs)
        self.assertRaises(KeyError, mock)
        self.assertEqual(mock.foo.bar(), 33)
        self.assertIsInstance(mock.foo, MagicMock)

if __name__ == '__main__':
    unittest.main(verbosity=2)