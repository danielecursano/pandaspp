from pandas import DataFrame

class DataFramePlus(DataFrame):

    __corr_graph = dict()
    __corr_tol = 0.9
    _metadata = [""]

    @property
    def _constructor(self):
        return DataFramePlus

    @property
    def correlation_graph(self):
        return self.__corr_graph

    @property
    def correlation_tolerance(self):
        return self.__corr_tol

    def set_correlation_tolerance(self, tol):
        if tol > self.__corr_tol:
            self.__corr_graph = {}
        self.__corr_tol = tol

    def drop(self, labels=None, axis=0, index=None, columns=None, level=None,inplace=False, errors="raise", raise_err=True):
        result = super().drop(labels=labels, axis=axis, index=index,
                              columns=columns, level=level, inplace=inplace,
                              errors=errors)
        if inplace:
            return None
        return self._constructor(result)
