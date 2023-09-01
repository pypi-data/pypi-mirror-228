# my_module.py

import unittest
from element_python_package import plotPrecisionRecallCurve_multiclass
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class TestPlotPrecisionRecallCurve(unittest.TestCase):

    def setUp(self):
        X, y = make_classification(n_samples=1000, n_classes=3, n_informative=3, n_redundant=0, random_state=42)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(self.x_train, self.y_train)

    def test_return_type(self):
        fig = plotPrecisionRecallCurve_multiclass(self.model, self.x_test, pd.Series(self.y_test), return_plot=True)
        self.assertTrue(isinstance(fig, type(plt.figure())))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            plotPrecisionRecallCurve_multiclass(None, self.x_test, self.y_test)

    # Add more tests

if __name__ == '__main__':
    unittest.main()