from pandas import DataFrame

class DataFramePlus(DataFrame):
    """
    A pandas DataFrame subclass that warns when dropping a column that is 
    highly correlated to previously dropped columns.

    Attributes:
        __corr_graph (dict): Tracks column correlations above a given threshold.
        __corr_tol (float): Threshold for correlation strength (default 0.9).
    """
    __corr_graph = dict()
    __corr_tol = 0.9

    _metadata = ["_corr_graph", "_corr_tol"]

    @property
    def _constructor(self):
        return DataFramePlus

    @property
    def correlation_graph(self):
        """
        Return the current correlation graph
        """
        return self.__corr_graph

    @property
    def correlation_tolerance(self):
        """
        Return the current correlation threshold
        """
        return self.__corr_tol

    def set_correlation_tolerance(self, tol):
        """
        Set a new correlation threshold

        Parameters
        ----------
        tol (float): new correlation threshold
        """
        if tol > self.__corr_tol:
            self.__corr_graph = dict()
        self.__corr_tol = tol

    def drop(self, labels=None, axis=0, index=None, columns=None, level=None,inplace=False, errors="raise", raise_err=True):
        """
        Override the pandas drop method to include correlation-based warnings.
        """
        corr_table = super().corr(numeric_only=True).unstack().dropna()
        for (col1, col2), corr_val in corr_table.items():
            if col1 != col2 and abs(corr_val) > self.__corr_tol:
                self.__corr_graph.setdefault(col1, set()).add(col2)
                self.__corr_graph.setdefault(col2, set()).add(col1)

        if columns:
            for col in columns:
                for corr_col in self.__corr_graph.get(col, set()):
                    remaining_corr = self.__corr_graph.get(corr_col, set()).intersection(self.columns)
                    if corr_col not in self.columns and len(remaining_corr) <= 1:
                        warning = f"{col} is the last correlated column of previously dropped {corr_col}"
                        if raise_err:
                            raise ValueError(warning)
                        else:
                            print(f"Warning: {warning}")

        result = super().drop(labels=labels, axis=axis, index=index,
                              columns=columns, level=level, inplace=inplace,
                              errors=errors)
        if inplace:
            return None
        return self._constructor(result)
