from unittest.mock import mock_open, patch
from src.CsvReader import CsvReader

test_csv = """position,performance
Backend Developer,4.85
Frontend Developer,4.72
"""


def test_load_report_info():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
            'file1.csv',
                '--report',
                'performance']
        ):
            reader = CsvReader()
            data = []
            result = reader._CsvReader__load_report_info(data)

            assert len(result) == 2
            assert ['Backend Developer', '4.85'] in result
            assert ['Frontend Developer', '4.72'] in result


def test_calculate_arithmetic():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
            'file1.csv',
                '--report',
                'performance']
        ):
            reader = CsvReader()
            data = [
                ('Backend Developer', '4.85'),
                ('Backend Developer', '4.85'),
                ('Backend Developer', '4.85'),
                ('Data Scientist', '4'),
                ('Data Scientist', '7'),
                ('Data Scientist', '4')
            ]

            result = reader._CsvReader__calculate_arithmetic(data)

            assert result['Backend Developer'] == 4.85
            assert result['Data Scientist'] == 5


def test_sort_arithmetic():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
            'file1.csv',
                '--report',
                'performance']
        ):
            reader = CsvReader()
            data = {
                'Backend Developer': 7,
                'Frontend Developer': 10
            }

            result = reader._CsvReader__sort_arithmetic(data)

            values = list(result.values())
            assert values == sorted(values, reverse=True)


def test_enumerate_data():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
            'file1.csv',
                '--report',
                'performance']
        ):
            reader = CsvReader()
            data = {
                'Backend Developer': 10,
                'Frontend Developer': 7
            }

            result = reader._CsvReader__enumerate_data(data)
            assert result[0][0] == 1


def test_wrong_args():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
            'file1.txt',
                '--report',
                'performance']
        ):

            data = []
            try:
                reader = CsvReader()
                reader._CsvReader__load_report_info(data)
            except ValueError as e:
                assert 'some file is not cvs' in str(e)


def test_value_error():
    with patch('builtins.open', mock_open(read_data=test_csv)):
        with patch('sys.argv', [
            ' main.py',
            '--files',
                'file1.csv',
            '--report',
            'performance']
        ):

            data = [
                ('Backend Developer', 'string'),
                ('Backend Developer', '4.85'),
                ('Backend Developer', '4.85'),
                ('Data Scientist', '4'),
                ('Data Scientist', '7'),
                ('Data Scientist', '4')
            ]
            try:
                reader = CsvReader()
                reader._CsvReader__calculate_arithmetic(data)
            except ValueError as e:
                assert 'Невозможно преобразовать в float.' in str(e)
