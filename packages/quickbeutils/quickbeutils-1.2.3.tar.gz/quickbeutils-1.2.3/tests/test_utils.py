import os
import uuid
import unittest
from quickbelog import Log
from quickbeutils import get_env_var_as_int, get_env_var_as_list, cast_mongo_types


class SendEmailTestCase(unittest.TestCase):

    def test_get_env_var_as_int(self):
        test_cases = {
            '123': 123,
            '12.3': 12,
            '12': 12,
            '111   ': 111,
            'Not relevant': 42
        }
        for k, v in test_cases.items():
            var_name = f'VAR_{uuid.uuid4()}'
            os.environ[var_name] = k
            value = get_env_var_as_int(var_name, default=42)
            Log.debug(f'Var: {var_name}, Value: {value}, Original value: {os.getenv(var_name)}')
            self.assertEqual(v, value)

    def test_get_env_var_as_list(self):
        test_cases = {
            '1 2 3': ['1', '2', '3'],
            '   1 2 3   ': ['1', '2', '3'],
            '   1, 2, 3   ': ['1', '2', '3'],
            '   ,1, 2, 3   ': ['', '1', '2', '3'],
            '   1, 2, 3,   ': ['1', '2', '3', ''],
        }
        for k, v in test_cases.items():
            var_name = f'VAR_{uuid.uuid4()}'
            os.environ[var_name] = k
            delimiter = ',' if ',' in k else ' '
            value = get_env_var_as_list(var_name, default=[42], delimiter=delimiter)
            Log.debug(f'Var: {var_name}, Value: {value}, Original value: {os.getenv(var_name)}')
            self.assertEqual(v, value)

    def test_cast_mongo_types(self):
        test_case = {
            'a1': {
                'a1a': {
                    '$numberInt': '1'
                },
                'a1b': {
                    '$numberDouble': '355.22388059701495'
                },
                'a1c': {
                    '$numberDouble': '0.3941176470588235'
                }
            },
            'b1': {
                'b1a': {
                    '$numberInt': '1'
                },
                'b1b': {
                    '$numberDouble': '355.22388059701495'
                }
            },
            'c1': {
                '$numberDouble': '204.78260869565216'
            },
            'd1': {
                '$numberInt': '200'
            },
            'e1': {
                'e2': {
                    'e3': {
                        'e4a': {
                            '$numberInt': '123'
                        },
                        'e4b': {
                            '$numberDouble': '123.456'
                        }
                    }
                }
            }
        }
        d1 = cast_mongo_types(test_case)
        Log.info(f'Converted dict: {d1}')
        self.assertEqual('$numberInt' in d1, False)


if __name__ == '__main__':
    unittest.main()
