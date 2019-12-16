from Codes.Task.Display import Display
from Codes.Task.Utils.GlobalValues import STARTING_DIR_PROB, N_TRIALS, N_TEST_TRIALS


if __name__ == "__main__":
    dot_stimuli = Display(n_dots=400, n_test_trials=N_TEST_TRIALS,
                          one_direction_prob=STARTING_DIR_PROB, n_trials=N_TRIALS)
    dot_stimuli.run_task()
