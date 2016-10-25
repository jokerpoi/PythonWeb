
class Page(object):
    def __init__(self,counts,offset):
        self._counts = counts
        self._pageNo = offset
        self._limit = 10

    @property
    def pageNo(self):
        return self._pageNo

    @pageNo.setter
    def offset(self,value):
        self._pageNo = value

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self,value):
        self._limit = value