from unittest import TestCase

from infograph import DataTable

TEST_DATA_LIST = [
    {'name': 'John', 'age': 20},
    {'name': 'Jane', 'age': 21},
    {'name': 'Jack', 'age': 22},
    {'name': 'Jill', 'age': 23},
    {'name': 'Jenny', 'age': 24},
]

TEST_DATA_TABLE = DataTable(TEST_DATA_LIST)


class TestDataTable(TestCase):
    def test_clean_data_cell(self):
        for [cell, expected_cleaned_cell] in [
            ['john', 'john'],
            ['20', 20],
            ['20.0', 20.0],
            ['20.1', 20.1],
            ['20.1.1', '20.1.1'],
            ['0', 0],
        ]:
            self.assertEqual(
                DataTable.clean_data_cell(cell), expected_cleaned_cell
            )

    def test_clean_data_row(self):
        self.assertEqual(
            DataTable.clean_data_row({'name': 'john', 'age': '20'}),
            {'name': 'john', 'age': 20},
        )

    def test_clean_data_list(self):
        self.assertEqual(
            DataTable.clean_data_list(TEST_DATA_LIST),
            TEST_DATA_LIST,
        )

    def test_init(self):
        self.assertEqual(TEST_DATA_TABLE.data_list, TEST_DATA_LIST)

    def test_get_column(self):
        self.assertEqual(
            TEST_DATA_TABLE.get_column('name'),
            ['John', 'Jane', 'Jack', 'Jill', 'Jenny'],
        )
        self.assertEqual(
            TEST_DATA_TABLE.get_column('age'), [20, 21, 22, 23, 24]
        )

    def test_getitem(self):
        self.assertEqual(
            TEST_DATA_TABLE['name'], ['John', 'Jane', 'Jack', 'Jill', 'Jenny']
        )
        self.assertEqual(TEST_DATA_TABLE['age'], [20, 21, 22, 23, 24])
        self.assertEqual(TEST_DATA_TABLE[0], {'name': 'John', 'age': 20})
        self.assertEqual(TEST_DATA_TABLE[1], {'name': 'Jane', 'age': 21})
        self.assertEqual(TEST_DATA_TABLE[2], {'name': 'Jack', 'age': 22})
        self.assertEqual(TEST_DATA_TABLE[3], {'name': 'Jill', 'age': 23})
        self.assertEqual(TEST_DATA_TABLE[4], {'name': 'Jenny', 'age': 24})

    def test_from_file(self):
        self.assertEqual(
            DataTable.from_file('tests/test_data_table.tsv').data_list,
            TEST_DATA_LIST,
        )
        self.assertEqual(
            DataTable.from_file('tests/test_data_table.json').data_list,
            TEST_DATA_LIST,
        )
