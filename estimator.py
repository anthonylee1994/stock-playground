import pandas as pd
from sklearn import linear_model


class Estimator:
    fit_intercept: bool
    training_upto: str
    feature_names: [str]
    target_name: str
    data: pd.DataFrame

    def __init__(self, feature_names: [str], target_name: str, training_upto: str, data: pd.DataFrame, fit_intercept: bool = False):
        self.feature_names = feature_names
        self.target_name = target_name
        self.data = data
        self.training_upto = training_upto
        self.fit_intercept = fit_intercept

    def training_data(self):
        return self.data[self.data.index <= self.training_upto]

    def testing_data(self):
        return self.data[self.data.index > self.training_upto]

    def estimate(self) -> pd.Series:
        training_data = self.training_data()
        testing_data = self.testing_data()
        regression = linear_model.LinearRegression(fit_intercept=self.fit_intercept, n_jobs=10)
        regression.fit(training_data[self.feature_names], training_data[self.target_name])

        full_confidence = regression.score(self.data[self.feature_names], self.data[self.target_name])
        training_confidence = regression.score(training_data[self.feature_names], training_data[self.target_name])
        testing_confidence = regression.score(testing_data[self.feature_names], testing_data[self.target_name])

        prediction = regression.predict(self.data[self.feature_names])

        print('Coefficient', regression.coef_)
        print('Intercept', regression.intercept_)
        print('Full Confidence:', full_confidence)
        print('Training Confidence:', training_confidence)
        print('Testing Confidence:', testing_confidence)
        print('\n')

        return prediction
