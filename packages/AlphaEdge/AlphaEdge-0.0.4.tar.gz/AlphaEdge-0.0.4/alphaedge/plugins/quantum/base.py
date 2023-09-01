import os
import pandas as pd
from ultron.factor.data.processing import factor_processing
from ultron.factor.data.winsorize import winsorize_normal
from ultron.factor.data.standardize import standardize


class Base(object):

    def __init__(self, directory, policy_id, is_groups=1):
        self.policy_id = policy_id
        self.directory = os.path.join(directory, self.policy_id)
        self.is_groups = is_groups
        self.category_directory = os.path.join(
            self.directory, "groups") if is_groups == 1 else os.path.join(
                self.directory, "main")

    def normal(self, total_data, columns):
        diff_columns = [
            col for col in total_data.columns if col not in columns
        ]
        diff_data = total_data[diff_columns]
        new_factors = factor_processing(
            total_data[columns].values,
            pre_process=[winsorize_normal, standardize],
            groups=total_data['trade_date'].values)

        factors_data = pd.DataFrame(new_factors,
                                    columns=columns,
                                    index=total_data.set_index(
                                        ['trade_date', 'code']).index)
        factors_data = factors_data.reset_index()
        factors_data = factors_data.merge(
            diff_data, on=['trade_date',
                           'code']).sort_values(by=['trade_date', 'code'])
        return factors_data