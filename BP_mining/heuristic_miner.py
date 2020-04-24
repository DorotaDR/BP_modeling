import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram

from collections import OrderedDict
import numpy as np
import pandas as pd


from log_wrapper import LogWrapper
from base_miner import BaseMiner


class HeuristicMiner(BaseMiner):
    def __init__(self, log_file_xes_path):
        super(HeuristicMiner, self).__init__(log_file_xes_path)
        self.log = LogWrapper(log_file_xes_path)
        self.TL = self.log.get_all_tasks()
        self.TI = self.log.get_first_tasks()
        self.TO = self.log.get_last_tasks()

        self.relation_frequency_df = pd.DataFrame()

        _relations = dict()
        for task in self.TL:
            _relations[task] = dict()
        self._dict_relations_frequency = OrderedDict(sorted(_relations.items()))

        self._direct_successor_pairs: list = None


    def execute_algorithm(self):
        pass

    def _set_direct_successors(self):

        self._direct_successor_pairs = []
        for case in self.log.log:
            prev_task_name = None
            for task in case:
                if prev_task_name:
                    self._direct_successor_pairs.append((prev_task_name, task['concept:name']))
                prev_task_name = task['concept:name']

    def set_relation_frequency_df(self):
        if not self._direct_successor_pairs:
            self._set_direct_successors()

        for pair in set(self._direct_successor_pairs):
            self._dict_relations_frequency[pair[0]][pair[1]] =self._direct_successor_pairs.count(pair)

        self.relation_frequency_df = pd.DataFrame.from_dict(self._dict_relations_frequency).T
        self.relation_frequency_df = self._fill_freq_matrix_with_nan(self.relation_frequency_df)


    def _fill_freq_matrix_with_nan(self, relation_df):
        missing_columns = set(self.TL).difference(set(relation_df.columns))

        for m_col in missing_columns:
            relation_df[m_col] = [np.NaN] * len(relation_df)

        return relation_df.reindex(sorted(relation_df.columns), axis=1)


