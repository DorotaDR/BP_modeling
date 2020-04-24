import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram

from collections import OrderedDict
import numpy as np
import pandas as pd


from BP_mining.log_wrapper import LogWrapper
from BP_mining.base_miner import BaseMiner


class HeuristicMiner(BaseMiner):
    def __init__(self, log_file_xes_path):
        super(HeuristicMiner, self).__init__(log_file_xes_path)
        self.log = LogWrapper(log_file_xes_path)
        self.TL = self.log.get_all_tasks()
        self.TI = self.log.get_first_tasks()
        self.TO = self.log.get_last_tasks()

        self.relation_frequency_df: pd.DataFrame = None
        self.rel_2loop_frequency_df: pd.DataFrame = None
        self.norm_relation_frequency_df: pd.DataFrame = None
        self.norm_rel_2loop_frequency_df: pd.DataFrame = None

        _relations = dict()
        for task in self.TL:
            _relations[task] = dict()
        self._dict_relations_frequency = OrderedDict(sorted(_relations.copy().items()))

        _relations = dict()
        for task in self.TL:
            _relations[task] = dict()
        self._dict_rel_2loop_frequency = OrderedDict(sorted(_relations.copy().items()))

        self._direct_successor_pairs: list = None


    def execute_algorithm(self):

        self.set_relation_frequency_matrix()
        self.set_2loop_frequency_matrix()

        self.normalize_relation_frequency_matrix()
        self.normalize_2loop_frequency_matrix()

        # print(f"Relation matrix \n {self.get_relation_frequency_matrix()}\n")
        #
        # print(f"Loop  matrix \n {self.get_2loop_frequency_matrix()}\n")

    def get_relation_frequency_matrix(self, normalized: bool = True):
        return self.norm_relation_frequency_df if normalized else self.relation_frequency_df

    def get_2loop_frequency_matrix(self, normalized: bool = True):
        freq_df = self.norm_rel_2loop_frequency_df.copy(deep=True) if normalized \
            else self.rel_2loop_frequency_df.copy(deep=True)
        freq_df.index = [f"{i}_{i}" for i in freq_df.index]
        return freq_df

    def set_relation_frequency_matrix(self):
        if not self._direct_successor_pairs:
            self._set_direct_successors()

        for pair in set(self._direct_successor_pairs):
            self._dict_relations_frequency[pair[1]][pair[0]] =self._direct_successor_pairs.count(pair)

        self.relation_frequency_df = pd.DataFrame.from_dict(self._dict_relations_frequency)
        self.relation_frequency_df = self._fill_freq_matrix_with_nan(self.relation_frequency_df)

    def set_2loop_frequency_matrix(self):

        # find 2-loop patterns in logs:
        two_loop_list = []
        for case in self.log.log:
            tasks_names_list = [task['concept:name'] for task in case]
            for i in range(0, len(tasks_names_list) - 3):
                # miss patterns as: "aaa" (all the same)
                if tasks_names_list[i] == tasks_names_list[i + 2] and tasks_names_list[i] != tasks_names_list[i+1]:
                    two_loop_list.append(tuple(tasks_names_list[i:i + 3]))

        #count frequencies of each 2-loop pattern and safe
        for (a_1, b, a_2) in set(two_loop_list):
            self._dict_rel_2loop_frequency[b][a_1] = two_loop_list.count((a_1, b, a_2))

        self.rel_2loop_frequency_df = pd.DataFrame.from_dict(self._dict_rel_2loop_frequency)
        self.rel_2loop_frequency_df = self._fill_freq_matrix_with_nan(self.rel_2loop_frequency_df)

    def normalize_relation_frequency_matrix(self):
        if self.relation_frequency_df.empty:
            print("Empty relation matrix")

        relation_df = self.relation_frequency_df.copy(deep=True)
        for i in relation_df.index:
            for col in relation_df.columns:
                if i == col:
                    relation_df.loc[i, col] = self.calculate_self_loop_normalization(i, self.relation_frequency_df)
                else:
                    relation_df.loc[i, col] = self.calculate_causality_normalization(i, col, self.relation_frequency_df)

        self.norm_relation_frequency_df = relation_df
        pass

    def normalize_2loop_frequency_matrix(self):
        if self.rel_2loop_frequency_df.empty:
            print("Empty two-loop matrix")

        two_loop_df = self.rel_2loop_frequency_df.copy(deep=True)
        for i in two_loop_df.index:
            for col in two_loop_df.columns:
                two_loop_df.loc[i, col] = self.calculate_two_loop_normalization(i, col, self.rel_2loop_frequency_df)

        self.norm_rel_2loop_frequency_df = two_loop_df

    @staticmethod
    def calculate_causality_normalization(t1: str, t2: str, relation_df: pd.DataFrame):
        """T1->T2"""
        if np.isnan(relation_df.loc[t1, t2]):
            return np.nan
        else:
            reverse_count = 0 if np.isnan(relation_df.loc[t2, t1]) else relation_df.loc[t2, t1]
            return (relation_df.loc[t1, t2] - reverse_count)/(relation_df.loc[t1, t2] + reverse_count+1)

    @staticmethod
    def calculate_self_loop_normalization(t1: str, relation_df: pd.DataFrame):
        """T1->T1"""
        if np.isnan(relation_df.loc[t1, t1]):
            return np.nan
        else:
            return relation_df.loc[t1, t1]/(relation_df.loc[t1, t1]+1)

    @staticmethod
    def calculate_two_loop_normalization(t1: str, t2: str, relation_df: pd.DataFrame):
        """T1->^2 T2"""
        if np.isnan(relation_df.loc[t1, t2]):
            return np.nan
        else:
            reverse_loop_count = 0 if np.isnan(relation_df.loc[t2, t1]) else relation_df.loc[t2, t1]
            return (relation_df.loc[t1, t2] + reverse_loop_count)/(relation_df.loc[t1, t2] + reverse_loop_count+1)

    def _set_direct_successors(self):
        self._direct_successor_pairs = []
        for case in self.log.log:
            prev_task_name = None
            for task in case:
                if prev_task_name:
                    self._direct_successor_pairs.append((prev_task_name, task['concept:name']))
                prev_task_name = task['concept:name']

    def _fill_freq_matrix_with_nan(self, relation_df):
        missing_columns = set(self.TL).difference(set(relation_df.columns))
        missing_rows = set(self.TL).difference(set(relation_df.index))

        for m_col in missing_columns:
            relation_df[m_col] = [np.NaN] * len(relation_df)

        relation_df = relation_df.T
        for m_row in missing_rows:
            relation_df[m_row] = [np.NaN] * len(relation_df)
        relation_df = relation_df.T

        relation_df = relation_df.reindex(sorted(relation_df.index), axis=0)
        return relation_df.reindex(sorted(relation_df.columns), axis=1)


