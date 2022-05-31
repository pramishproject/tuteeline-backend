class StringToJson():
    def __init__(self,data):
        self._data = data

    def execute(self):
        return self._factory()

    def _factory(self):
        listId = list(self._data.split(","))
        return listId