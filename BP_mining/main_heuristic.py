
from log_wrapper import LogWrapper
from heuristic_miner import HeuristicMiner

import pandas as pd


if __name__ == "__main__":
    # execute only if run as a script
    log_file_path = "./../sample_logs/heuristic_log.xes"
    log_wrapped = LogWrapper(log_file_path)
    log_wrapped.to_list()

    heuristic = HeuristicMiner(log_file_path)
    heuristic.execute_algorithm()

    # filename = "./../results/heuristic_result"
    # heuristic.save_to_png(filename)
    #
    # print(heuristic.get_relation_df())

    # heuristic.set_relation_frequency_matrix()
    # heuristic.set_2loop_frequency_matrix()

    # print(f"heuristic._direct_successor_pairs= {heuristic._direct_successor_pairs}")

    print(f"heuristic.relation_frequency_df=\n\n{heuristic.get_relation_frequency_matrix(normalized=False)}")
    print("\n\n")

    print(f"heuristic.rel_2loop_frequency_df=\n\n{heuristic.get_2loop_frequency_matrix(normalized=False)}")