from Codes.Task.Display import Display
from Codes.Task.Utils.GlobalValues import RIGHT_PROB, N_TRIALS


if __name__ == "__main__":
    dot_stimuli = Display(n_dots=N_TRIALS, right_prob=RIGHT_PROB)
    dot_stimuli.run_task()
