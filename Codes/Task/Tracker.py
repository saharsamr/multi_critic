from Codes.Task.Utils.Directions import Dir
from Codes.Task.Utils.Genders import Gender
from Codes.Task.Logger import Logger
from Codes.Task.Utils.GlobalValues import N_TRIALS, \
    BLOCK_SIZE, N_TEST_TRIALS, MIN_COHERENCY


class TrialInfo:
    def __init__(self, correct_answer, user_answer, user_confidence, one_direction_prob):
        self.correct_answer = correct_answer
        self.user_answer = user_answer
        self.user_confidence = user_confidence
        self.one_direction_prob = one_direction_prob


class UserInfo:
    def __init__(self, first_name, last_name, age, gender, critic):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.critic = critic


class Tracker:
    def __init__(self):
        self.user_info = None
        self.n_trials = N_TRIALS
        self.block_size = BLOCK_SIZE
        self.trials_info = []

    def add_user_info(self, first_name, last_name, age, gender, critic):
        if gender == "Male":
            gender = Gender.Male
        elif gender == "Female":
            gender = Gender.Female
        else:
            gender = Gender.Other
        self.user_info = UserInfo(first_name, last_name, age, gender, critic)

    def add_trial_info(self, correct_answer, user_answer, user_confidence, one_direction_prob):
        self.trials_info.append(TrialInfo(correct_answer, user_answer, user_confidence, one_direction_prob))

    def staircase(self, step, display):
        n_trial = len(self.trials_info)
        if len(self.trials_info) > 1:
            last_trial, pre_last_trial = \
                self.trials_info[n_trial-1], self.trials_info[n_trial-2]
            if last_trial.correct_answer == last_trial.user_answer and \
                    pre_last_trial.correct_answer == pre_last_trial.user_answer:
                display.change_dir_probability(-1 * 4 * step)
            elif last_trial.correct_answer != last_trial.user_answer:
                display.change_dir_probability(2 * step)

    def save(self):
        Logger.write_per_user_data(self)

    def get_trial_info(self, trial_index):
        return self.trials_info[trial_index]

    def get_training_start_dir_prob(self):
        return self.trials_info[N_TEST_TRIALS-1].one_direction_prob

    def get_trial_difficulty(self, trial_index):
        trial = self.trials_info[trial_index]

        COEFF = -1 / (1 - MIN_COHERENCY)
        BIAS = 1 - MIN_COHERENCY

        coherency = abs(trial.one_direction_prob - (1 - trial.one_direction_prob))
        difficulty = COEFF * coherency + BIAS

        return difficulty

    def get_critic(self):
        return self.user_info.critic

    @staticmethod
    def majority_voting(dots, central_circle):
        n_right, n_left = 0, 0
        for dot in [dot for dot in dots if central_circle.contains(dot.xy[0], dot.xy[1])]:
            if dot.move_direction == Dir.Right:
                n_right += 1
            else:
                n_left += 1
        return Dir.Right if n_right > n_left else Dir.Left
