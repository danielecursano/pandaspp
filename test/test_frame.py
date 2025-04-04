import unittest
from pandas.testing import assert_frame_equal
from pandas import DataFrame
from src.frame import DataFramePlus  # Replace with your actual module path

class TestDataFramePlus(unittest.TestCase):

    def setUp(self):
        self.df = DataFramePlus({
            "A": [1, 2, 3, 4, 5],
            "B": [2, 4, 6, 8, 10],  # Perfectly correlated with A
            "C": [5, 10, 15, 20, 25]  # Also correlated
        })

    def test_drop_warns_on_last_correlated_column(self):
        df1 = self.df.drop(columns=["A", "C"], inplace=False)
        with self.assertRaises(ValueError) as context:
            df1.drop(columns=["B"], raise_err=True)
        self.assertIn("is the last correlated column of previously dropped", str(context.exception))

    def test_drop_warns_without_raising_error(self):
        df1 = self.df.drop(columns=["A"], inplace=False)
        try:
            df2 = df1.drop(columns=["B"], raise_err=False)
            expected_df = DataFramePlus({
                "C": [5, 10, 15, 20, 25]
            })
            assert_frame_equal(df2, expected_df)
        except Exception as e:
            self.fail(f"drop() raised an exception unexpectedly: {e}")

    def test_set_correlation_tolerance_resets_graph(self):
        df = DataFramePlus({
            "A": [1, 2, 3],
            "B": [1, 2, 3],
            "C": [3, 2, 1]
        })
        df._corr_graph = {"A": {"B"}}
        df.set_correlation_tolerance(0.95)

        self.assertEqual(df.correlation_graph, {})
        self.assertEqual(df.correlation_tolerance, 0.95)

if __name__ == "__main__":
    unittest.main()
