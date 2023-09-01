"""A class to help with statistical tests"""
from ipywidgets import widgets
import pandas as pd
from scipy import stats

class Stattests:
    """A class to help with statistical tests (normal distribution/independence of variables)"""
    def __init__(self, bogui):
        """Class constructor."""

        self.dataset = pd.DataFrame()
        self.bogui = bogui
        self.explanatory = None
        self.dependent = None

    def check_numerical_data(self, dataframe):
        """Extract numerical data from pandas dataframe
        and checks properties of data(is normally distributed).
        args:
            dataframe: pandas dataframe
        returns:
            checked_indexes: dictionary
        """
        checked_indexes = {}
        num_data = {}
        num_indexes = dataframe.select_dtypes(include="number")
        str_indexes = dataframe.select_dtypes(include=["object", "string"])

        for index in num_indexes.columns:
            lst = list(num_indexes[index].dropna())
            num_data[index] = lst
        # loop through dtypes marked as strings or objects.
        for index in str_indexes.columns:
            lst = list(str_indexes[index].dropna())
            numerical = True
            # loop to check that all values are numerical.
            for idx, item in enumerate(lst):
                if item.lstrip('-').replace('.','',1).isdigit() is False:
                    numerical = False
                    break
                # change string value to float.
                lst[idx] = float(item)
            if numerical:
                num_data[index] = lst
        for item in num_data:
            # call for function(s) to check data property
            ndistributed = self._is_normally_distributed(num_data[item])
            checked_indexes[item] = ndistributed

        # self.chi_square_test()
        return checked_indexes

    def _is_normally_distributed(self, list_):
        """Check if values in the given list are normally distributed.
        args:
            values: list of values
        returns:
            boolean
        """
        result = stats.shapiro(list_)
        if len(result) >= 2:
            if result[1] > 0.05:
                return True

        return False

    def select_variables(self):
        """Creates dropdowns for selecting two variables from imported data."""

        categorical = self.dataset.select_dtypes(exclude='number')
        variables = categorical.columns.values
        style = {'description_width': 'initial'}
        if len(variables) >= 2:
            self.explanatory = widgets.Dropdown(
                options = variables,
                description = 'Explanatory variable',
                style = style
            )
            self.dependent = widgets.Dropdown(
                options = variables,
                description ='Dependent variable',
                style = style
            )
            variable_grid = widgets.AppLayout(
                header=self.bogui.create_message(
                    'Choose variables to test their independence:'
                ),
                center=widgets.VBox([
                    self.explanatory,
                    self.dependent
                ])
            )

            return variable_grid

        message = self.bogui.create_message(
            'There are not enough categorical variables to perform a chi-square test.')

        return message

    def check_variable_independence(self):
        """Performs a chi-square test of independence between selected variables.

        Returns:
            result_tuple (tuple): A tuple with explanatory variable (str),
            dependent variable (str), and True if variables are independent,
            False if they are not independent, and error message (str) if
            test could not be performed."""

        crosstab = pd.crosstab(
            self.dataset[self.explanatory.value],
            self.dataset[self.dependent.value]
        )

        result = 'Error: The test could not be performed'

        test_result = stats.chi2_contingency(crosstab)
        if len(test_result) >= 2:
            if test_result[1] < 0.05:
                result = False

            else:
                result = True

        return (self.explanatory.value, self.dependent.value, result)
    