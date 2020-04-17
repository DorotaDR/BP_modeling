
from log_wrapper import LogWrapper
from alpha_miner import AlphaMiner



if __name__ == "__main__":
    # execute only if run as a script
    log_file_path = "./../my-example_short.xes"
    log_wrapped = LogWrapper(log_file_path)
    log_wrapped.to_list()

    alpha = AlphaMiner(log_file_path)
    alpha.execute_algorithm()

    filename = "./../results/alpha_result"
    alpha.save_to_png(filename)

    print(alpha.get_relation_df())



