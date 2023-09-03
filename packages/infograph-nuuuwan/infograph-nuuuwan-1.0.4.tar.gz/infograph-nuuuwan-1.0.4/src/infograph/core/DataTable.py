from utils import File, JSONFile, String, TSVFile


class DataTable:
    @staticmethod
    def clean_data_cell(cell):
        cell = str(cell)
        if cell.isnumeric():
            return String(cell).int
        s = String(cell).float
        if s is not None:
            return s
        return cell

    @staticmethod
    def clean_data_row(row):
        return {k: DataTable.clean_data_cell(v) for k, v in row.items()}

    @staticmethod
    def clean_data_list(data_list):
        return [DataTable.clean_data_row(row) for row in data_list]

    def __init__(self, data_list):
        self.data_list = data_list

    @staticmethod
    def from_file(file_path):
        data_list = None
        if File(file_path).ext == 'tsv':
            data_list = TSVFile(file_path).read()
        if File(file_path).ext == 'json':
            data_list = JSONFile(file_path).read()

        if data_list:
            return DataTable(DataTable.clean_data_list(data_list))

        raise Exception(f'Unsupported file type: {file_path}')

    def get_column(self, column_name):
        return [row[column_name] for row in self.data_list]

    def __getitem__(self, field_or_index):
        if isinstance(field_or_index, int):
            return self.data_list[field_or_index]
        if isinstance(field_or_index, str):
            return self.get_column(field_or_index)

    def sort(self, field, reverse=False):
        self.data_list = sorted(
            self.data_list, key=lambda x: x[field], reverse=reverse
        )
