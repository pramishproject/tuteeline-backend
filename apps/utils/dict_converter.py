from django.db import connection


class QueryDataSerializer():
    def __init__(self, query_data):
        self._query = query_data

    def execute(self):
        self._factory()
        return self.resp_data
    def _factory(self):
        self._query_factory()
        self._data_factory()

    def _query_factory(self):
        self.cursor = connection.cursor()
        self.cursor.execute(self._query)
        self._data=self.cursor.fetchall()

    def _data_factory(self):
        col_names = [desc[0] for desc in self.cursor.description]
        data_type=type(self._data) == list
        self.resp_data=None
        if  len(self._data)>0:
            if data_type :
                data_dict = []
                for row in self._data:
                    row_dict = dict(zip(col_names, row))
                    data_dict.append(row_dict)
            else:
                row_dict = dict(zip(col_names, self._data))
                data_dict= row_dict
            self.resp_data=data_dict

        return self.resp_data
        # print(self._data)
