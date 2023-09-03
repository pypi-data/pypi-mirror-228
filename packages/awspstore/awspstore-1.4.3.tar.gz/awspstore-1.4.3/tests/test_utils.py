import os
import uuid
import unittest
from awspstore import get_env_as_list, get_parameters, is_secret


class UtilsTestCase(unittest.TestCase):

    def test_is_secret(self):
        test_cases = {
            'ABC_DEF_KEY': True,
            'ABC_DEF-KEY': True,
            'ABC_DEF_KEYS': True,
            'ABC_ACCESS_KEY_123': True,
            'ABC_123_TOKEN': True,
            'ABC_123-TOKEN': True,
            'ABC_123_PWD': True,
            'ABC_PWD_123': True,
            'ABC_PASSWORD_123': True,
            'ABC_SECRET_KEY_123': True,
            'ABC_KEY_PWD123': False,
            'ABC_KEY_123': False,
            'ABC_KEYS_123': False,
            'ABC_SECRET_123': False,
        }
        for key, expected_value in test_cases.items():
            self.assertEqual(True, is_secret(key) == expected_value, msg=f'{key}')

    def test_get_env_as_list(self):
        var_name = f'var_{uuid.uuid4()}'
        value = '   a ,B,1,  2  '
        os.environ[var_name] = value
        valid_result = ['a', 'B', '1', '2']
        self.assertEqual(valid_result, get_env_as_list(key=var_name))
        self.assertEqual(valid_result, get_env_as_list(key=f'{uuid.uuid4()}', default=valid_result.copy()))

    def test_get_parameters(self):
        results = get_parameters(path='dev')
        self.assertIsNotNone(results)
        self.assertIsInstance(results, dict)


if __name__ == '__main__':
    unittest.main()
