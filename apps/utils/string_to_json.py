class StringToJson():
    def __init__(self,data):
        self._data = data

    def execute(self):
        return self._factory()

    def _factory(self):
        print("**********hhjgkjh",self._data)
        if len(self._data) >3:

            listId = list(self._data.split(","))
            return listId
        else:
            return []

