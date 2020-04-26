import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram

from collections import OrderedDict
import numpy as np
import pandas as pd
import copy


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


    def execute_algorithm(self, threshold):

        self.set_relation_frequency_matrix()
        self.set_2loop_frequency_matrix()

        self.normalize_relation_frequency_matrix()
        self.normalize_2loop_frequency_matrix()
        self.recognize_patterns_to_graph(threshold)

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
        if np.isnan(relation_df.loc[t1, t2]) and np.isnan(relation_df.loc[t2, t1]):
            return np.nan
        elif np.isnan(relation_df.loc[t1, t2]):
            return (-relation_df.loc[t2, t1]) / (relation_df.loc[t2, t1] + 1)
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

    @staticmethod
    def negative_in_row(array, start):
        for i, x in enumerate(array):
            if x < 0 and i != start:
                return i

    @staticmethod
    def positive_in_row(array, start):
        for i, x in enumerate(array):
            if x > 0 and i != start:
                return i

    @staticmethod
    def next_no_nan_index(array, start):
        next_items = array[start + 1:]
        for i, x in enumerate(next_items):
            if not np.isnan(x):
                # print(y)
                return 1 + start + i

    def recognize_patterns_to_graph(self, threshold):
        Xl_a = []
        Xl_b = []
        Xl_c = []
        P_d = []
        P_e = []
        L_1 = []
        L_2 = []

        #TODO: cleanup
        T_0 = list(self.norm_relation_frequency_df.columns)

        # list(logs.task.unique())

        relations = np.array(self.get_relation_frequency_matrix())
        loops = np.array(self.get_2loop_frequency_matrix())

        for task in range(len(T_0)):

            x = task

            # that's L_1
            if relations[x, x] > threshold:
                aa = self.negative_in_row(relations[x], x)  # a->bb (minus w rzędzie b)
                cc = self.positive_in_row(relations[x], x)  # bb->c (plus w b)
                if not aa + 1:
                    print('todo_a')  # L_1.append(())
                elif not cc + 1:
                    print('todo_c')  # L_1.append(())
                else:
                    L_1.append((T_0[aa], T_0[x], T_0[cc]))

                    # y = 1
            y = self.next_no_nan_index(relations[x], 0)
            if not y:
                continue
                # print(y)

            for i in range(len(T_0) - x):
                a = x + i
                # print(x,a)

                # that's L_2
                if loops[x, a] > 0:
                    # print('got it')
                    aba = self.negative_in_row(relations[x], x)  # a->bcb (minus w rzędzie b)
                    cbc = self.positive_in_row(relations[x], x)  # bcb->d (plus w b)
                    L_2.append((T_0[aba], (T_0[x], T_0[a], T_0[x]), T_0[cbc]))

                # that's A
                if relations[x, a] > threshold and relations[a, x] < -threshold:
                    Xl_a.append((T_0[x], T_0[a]))  # A is ok

            for i in range(len(T_0) - y):
                a = y + i
                z = self.next_no_nan_index(relations[x], a)
                # print(x,a,z)
                if not (a and z):
                    continue

                    # that's B,C
                if np.all(relations[x, a] > threshold and relations[x, z] > threshold and np.isnan(relations[a, z])):
                    Xl_b.append((T_0[x], (T_0[a], T_0[z])))
                if np.all(relations[x, a] < -threshold and relations[x, z] < -threshold and np.isnan(relations[a, z])):
                    Xl_c.append(((T_0[a], T_0[z]), T_0[x]))  # C is ok

                # that's D,E
                if np.all(
                        relations[x, a] > -threshold and relations[x, z] > -threshold and relations[a, z] < threshold):
                    P_d.append((T_0[x], (T_0[a], T_0[z])))  # k
                if np.all(relations[x, a] < threshold and relations[x, z] < threshold and relations[a, z] < threshold):
                    P_e.append(((T_0[a], T_0[z]), T_0[x]))

        Yl = copy.deepcopy(Xl_a)
        # print(Yl)

        for bit in Xl_b:
            if ((bit[0], bit[1][0])) in Yl:
                Yl.remove((bit[0], bit[1][0]))
            if ((bit[0], bit[1][1])) in Yl:
                Yl.remove((bit[0], bit[1][1]))
            # Yl.append(bit)

        for bit in Xl_c:
            if ((bit[0][0], bit[1])) in Yl:
                Yl.remove((bit[0][0], bit[1]))
            if ((bit[0][1], bit[1])) in Yl:
                Yl.remove((bit[0][1], bit[1]))
            # Yl.append(bit)

        for bit in P_d:
            if ((bit[0], bit[1][0])) in Yl:
                Yl.remove((bit[0], bit[1][0]))
            if ((bit[0], bit[1][1])) in Yl:
                Yl.remove((bit[0], bit[1][1]))
                # Yl.append(bit)

        for bit in P_e:
            if ((bit[0][0], bit[1])) in Yl:
                Yl.remove((bit[0][0], bit[1]))
            if ((bit[0][1], bit[1])) in Yl:
                Yl.remove((bit[0][1], bit[1]))
            # Yl.append(bit)

        # TODO: if bit in L1/L2 remove from b/c/d/e ?
        for bit in L_1:
            if ((bit[0], bit[1])) in Yl:
                Yl.remove((bit[0], bit[1]))
            if ((bit[1], bit[2])) in Yl:
                Yl.remove((bit[1], bit[2]))
            # Yl.append(bit)

        for bit in L_2:
            if ((bit[0], bit[1][0])) in Yl:
                Yl.remove((bit[0], bit[1][0]))
            if ((bit[0], bit[1][1])) in Yl:
                Yl.remove((bit[0], bit[1][1]))
            if ((bit[1][0], bit[2])) in Yl:
                Yl.remove((bit[1][0], bit[2]))

            # Yl.append(bit)

        # print(Yl)
        # print(Xl_b)
        # print(Xl_c)
        # print(P_d)
        # print(P_e)
        # print(L_1)
        # print(L_2)

        self.bpmn_graph = diagram.BpmnDiagramGraph()
        self.bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        process_id = self.bpmn_graph.add_process_to_diagram()

        [start_id, _] = self.bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event", )

        xors_fork = []
        for n in Xl_b:
            xors_fork.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_fork"))[0])
        xors_fork_l1 = []
        for n in L_1:
            xors_fork_l1.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_fork"))[0])
        xors_fork_l2 = []
        for n in L_2:
            xors_fork_l2.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_fork"))[0])

        ands_fork = []
        for t in P_d:
            ands_fork.append((self.bpmn_graph.add_parallel_gateway_to_diagram(process_id, gateway_name="and_fork"))[0])

        all_tasks = []
        for task in T_0:
            all_tasks.append((self.bpmn_graph.add_task_to_diagram(process_id, task_name=str(task)))[0])
            # print(all_tasks)

        xors_join = []
        for i in Xl_c:
            xors_join.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_join"))[0])
        xors_join_l1 = []
        for n in L_1:
            xors_join_l1.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_join"))[0])
        xors_join_l2 = []
        for n in L_2:
            xors_join_l2.append((self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_join"))[0])

        ands_join = []
        for k in P_e:
            ands_join.append((self.bpmn_graph.add_parallel_gateway_to_diagram(process_id, gateway_name="and_join"))[0])

        [end_id, _] = self.bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="end_event", )

        if len(self.TI) > 1:
            [first_xor, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(process_id, gateway_name="xor_fork")
            # start_id -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=start_id, target_ref_id=first_xor)
            for elem in self.TI:
                self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=first_xor,
                                                             target_ref_id=all_tasks[T_0.index(elem)])
                # XOR -> bit
        else:
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=start_id,
                                                         target_ref_id=all_tasks[T_0.index(list(self.TI)[0])])  # start_event -> self.TI[0]

        for bits in self.TO:
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(bits)],
                                                         target_ref_id=end_id)  # bit -> end_event

        for num, B in enumerate(Xl_b):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(B[0])],
                                                         target_ref_id=xors_fork[num])  # B[0] -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork[num],
                                                         target_ref_id=all_tasks[T_0.index(B[1][0])])  # XOR -> B[1][0]
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork[num],
                                                         target_ref_id=all_tasks[T_0.index(B[1][1])])  # XOR -> B[1][1]

        for num, C in enumerate(Xl_c):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(C[0][0])],
                                                         target_ref_id=xors_join[num])  # C[0][0] -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(C[0][1])],
                                                         target_ref_id=xors_join[num])  # C[0][1] -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_join[num],
                                                         target_ref_id=all_tasks[T_0.index(C[1])])  # XOR -> C[1]

        for num, D in enumerate(P_d):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(D[0])],
                                                         target_ref_id=ands_fork[num])  # D[0] -> AND
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=ands_fork[num],
                                                         target_ref_id=all_tasks[T_0.index(D[1][0])])  # AND -> D[1][0]
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=ands_fork[num],
                                                         target_ref_id=all_tasks[T_0.index(D[1][1])])  # AND -> D[1][1]

        for num, E in enumerate(P_e):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(E[0][0])],
                                                         target_ref_id=ands_join[num])  # E[0][0] -> AND
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(E[0][1])],
                                                         target_ref_id=ands_join[num])  # E[0][1] -> AND
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=ands_join[num],
                                                         target_ref_id=all_tasks[T_0.index(E[1])])  # AND -> E[1]

        for A in Yl:
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(A[0])],
                                                         target_ref_id=all_tasks[T_0.index(A[1])])  # A[0] -> A[1]

        for num, L in enumerate(L_1):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(L[0])],
                                                         target_ref_id=xors_join_l1[num])  # A -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(L[1])],
                                                         target_ref_id=xors_fork_l1[num])  # L -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_join_l1[num],
                                                         target_ref_id=all_tasks[T_0.index(L[1])])  # XOR -> L
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork_l1[num],
                                                         target_ref_id=xors_join_l1[num])  # XOR -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork_l1[num],
                                                         target_ref_id=all_tasks[T_0.index(L[2])])  # XOR -> C

        for num, L in enumerate(L_2):
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(L[0])],
                                                         target_ref_id=xors_join_l2[num])  # A -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(L[1][0])],
                                                         target_ref_id=xors_fork_l2[num])  # B -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_join_l2[num],
                                                         target_ref_id=all_tasks[T_0.index(L[1][0])])  # XOR -> B
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork_l2[num],
                                                         target_ref_id=all_tasks[T_0.index(L[1][1])])  # XOR -> C
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=all_tasks[T_0.index(L[1][1])],
                                                         target_ref_id=xors_join_l2[num])  # C -> XOR
            self.bpmn_graph.add_sequence_flow_to_diagram(process_id, source_ref_id=xors_fork_l2[num],
                                                         target_ref_id=all_tasks[T_0.index(L[2])])  # XOR -> D

    def save_to_png(self, filename="bpmn_heuristic_graph.png"):
        return super().save_to_png(filename)