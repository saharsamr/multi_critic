from Codes.Task.Tracker import TrialInfo
from statistics import mean
from Codes.Task.Utils.GlobalValues import MIN_COHERENCY, N_TEST_TRIALS, N_TRIALS
from Codes.Task.Rewarder import Rewarder


class AnalyseData:

    def __init__(self, path):
        self.trials = []
        self.critic = None

        self.extract_user_data(path)

    def extract_user_data(self, data_path):
        with open(data_path, 'r') as file:
            line = file.readline()
            start_pos = line.find('critic:') + 8
            self.critic = line[start_pos:-1]

            trial = file.readline()
            while trial:
                trial_info = trial[trial.find(':')+2:]
                correct_answer, user_answer, user_confidence, one_direction_prob = trial_info.split(sep=', ')
                self.trials.append(TrialInfo(correct_answer, user_answer, user_confidence, one_direction_prob))
                trial = file.readline()

    def answers(self, start_inx=None, end_inx=None):
        start_inx, end_inx = self.set_inx(start_inx, end_inx)

        return [1 if trial.correct_answer == trial.user_answer else 0 for trial in self.trials[start_inx:end_inx]]

    def confidences(self, bin_size, start_inx=None, end_inx=None):
        start_inx, end_inx = self.set_inx(start_inx, end_inx)

        confidences = [int(trial.user_confidence) for trial in self.trials[start_inx:end_inx]]

        return [mean(confidences[i*bin_size:(i+1)*bin_size]) for i in range(int(len(confidences)/bin_size))]

    def accuracy(self, bin_size, start_inx=None, end_inx=None):
        start_inx, end_inx = self.set_inx(start_inx, end_inx)
        answers = self.answers(start_inx=start_inx, end_inx=end_inx)

        return [mean(answers[i*bin_size:(i+1)*bin_size]) for i in range(int(len(answers)/bin_size))]

    def difficulties(self, bin_size=1, start_inx=None, end_inx=None):
        start_inx, end_inx = self.set_inx(start_inx, end_inx)

        def difficulty(one_dir_prob):
            COEFF = -1 / (1 - MIN_COHERENCY)
            BIAS = 1 - MIN_COHERENCY

            coherency = abs(one_dir_prob - (1 - one_dir_prob))
            return COEFF * coherency + BIAS
        diffs = [difficulty(float(trial.one_direction_prob)) for trial in self.trials[start_inx:end_inx]]
        return [mean(diffs[i * bin_size:(i + 1) * bin_size]) for i in range(int(len(diffs) / bin_size))]

    def meta(self, bin_size, start_inx=None, end_inx=None):
        start_inx, end_inx = self.set_inx(start_inx, end_inx)

        answers = self.answers(start_inx=start_inx, end_inx=end_inx)
        confidences = self.confidences(bin_size=1, start_inx=start_inx, end_inx=end_inx)

        MAX_CONFIDENCE = 6
        QSR = lambda accuracy, p_correct_: 1 - (accuracy - p_correct_) ** 2
        p_correct = lambda user_confidence: -1 / (MAX_CONFIDENCE - 1) + user_confidence / (MAX_CONFIDENCE - 1)

        meta_ability = [QSR(answers[i], p_correct(confidences[i])) for i in range(len(answers))]

        return [mean(meta_ability[i*bin_size:(i+1)*bin_size]) for i in range(int(len(meta_ability)/bin_size))]

    def rewards(self, critic, bin_size=1, start_inx=N_TEST_TRIALS, end_inx=N_TRIALS+N_TEST_TRIALS):
        rewards = None

        if critic == 'Meta':
            rewards = [Rewarder.meta_reward(trial.user_answer, trial.correct_answer, int(trial.user_confidence))
                       for trial in self.trials[start_inx:end_inx]]

        elif critic == 'Confidence':
            rewards = [Rewarder.confidence_reward(int(trial.user_confidence))
                       for trial in self.trials[start_inx:end_inx]]

        elif critic == 'Performance':
            rewards = [Rewarder.difficulty_reward(float(trial.one_direction_prob))
                       for trial in self.trials[start_inx:end_inx]]

        return [mean(rewards[i*bin_size:(i+1)*bin_size]) for i in range(int(len(rewards)/bin_size))]

    def pre_post_training_difficulty(self):
        pre_difficulty = self.difficulties(end_inx=N_TEST_TRIALS-1)
        post_difficulty = self.difficulties(start_inx=N_TEST_TRIALS+N_TRIALS-1)

        return [mean(pre_difficulty), mean(post_difficulty)], \
               [min(pre_difficulty), min(post_difficulty)], \
               [max(pre_difficulty), max(post_difficulty)]

    def pre_post_training_meta(self):
        pre_meta = self.meta(bin_size=1, end_inx=N_TEST_TRIALS-1)
        post_meta = self.meta(bin_size=1, start_inx=N_TEST_TRIALS+N_TRIALS-1)

        return [mean(pre_meta), mean(post_meta)], \
               [min(pre_meta), min(post_meta)], \
               [max(pre_meta), max(post_meta)]

    def pre_post_training_avg_confidence(self):
        pre_confidence = self.confidences(bin_size=1, end_inx=N_TEST_TRIALS-1)
        post_confidence = self.confidences(bin_size=1, start_inx=N_TEST_TRIALS+N_TRIALS-1)

        return [mean(pre_confidence), mean(post_confidence)], \
               [min(pre_confidence), min(post_confidence)], \
               [max(pre_confidence), max(post_confidence)]

    def set_inx(self, start_inx, end_inx):
        s_inx = 0 if not start_inx else start_inx
        e_inx = len(self.trials) if not end_inx else end_inx

        return s_inx, e_inx





