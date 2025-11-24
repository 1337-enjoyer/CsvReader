import argparse
import csv
import tabulate


# Комментарий к ТЗ: В проекте есть readme, примеры запуска, .gitignore, файл с зависимостями. 
# В проекте нет линтера или форматтера. Используется контекстный менеджер, что верно. 
# Аннотации не используются. Используется try/except или исключения. Для валидации названия отчетов можно
#  было использовать choices в argparse. Есть валидация путей к файлам. Используется ООП. Не используются 
#  абстрактные классы или протоколы, можно было с их помощью описать отчёты. God Object. Не используется 
#  dataclasses, можно было использовать как DTO, раз читаем весь файл в память, если по проще, то можно 
#  было взять TypedDict. Не используется @pytest.fixture. Не используется @pytest.mark.parametrize.




class CsvReader:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--files', type=str, nargs='+',
                                 help='Files for report')
        self.parser.add_argument('--report', type=str, help='Type of report')
        self.__get_args()
        self.report_type = self.parser_args.report

    def __get_args(self):
        """Загрузка аргументов и директорий и отчёта."""
        self.parser_args = self.parser.parse_args()
        self.run_files = self.parser_args.files
        self.run_report = self.parser_args.report

    def __load_report_info(self, data_for_load, report):
        """"Получаем все position и performance."""
        try:
            for arg in self.parser_args.files:
                with open(arg, 'r') as file:
                    if not file.name.endswith('.csv'):
                        raise ValueError('some file is not cvs')
                    reader = csv.DictReader(file)
                    for employee in reader:
                        data_for_load.append([
                            employee['position'],
                            employee[report]
                        ])
            return data_for_load
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден в директории!')

    def __calculate_arithmetic(self, data_for_calculate):
        """Подсчитываем среднее арифметическое."""
        result = {}
        for position, report_value in data_for_calculate:
            try:
                value = float(report_value)
                if position not in result:
                    result[position] = []
                result[position].append(value)
            except ValueError:
                print('Невозможно преобразовать в float.')

        for position, values in result.items():
            result[position] = sum(values) / len(values)

        return result

    def __sort_arithmetic(self, data_for_sort, reverse=True):
        """"Сортировка по убыванию."""
        return dict(sorted(
            data_for_sort.items(),
            key=lambda item: item[1],
            reverse=reverse))

    def __enumerate_data(self, data_for_enumerate):
        """"Нумерация для отчёта."""
        enumerated_data = []
        for i, (position, performance) in enumerate(
                    data_for_enumerate.items(), 1):
            enumerated_data.append([
                i,
                position,
                f"{performance:.2f}",
            ])
        return enumerated_data

    def performance_report(self):
        """"Получените отчёта."""
        data_for_report = []
        headers = ['#', 'position', self.report_type]
        data_for_report = self.__load_report_info(
            data_for_report, self.report_type)
        calculate_arithmetic = self.__calculate_arithmetic(data_for_report)
        sorted_arithmetic = self.__sort_arithmetic(calculate_arithmetic)
        enumerated_data = self.__enumerate_data(sorted_arithmetic)
        print(tabulate.tabulate(enumerated_data, headers=headers))
