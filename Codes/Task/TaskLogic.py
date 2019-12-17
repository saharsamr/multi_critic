from Codes.Task.Tracker import Tracker
from Codes.Task.Display import Display
from Codes.Task.Utils.Directions import Dir
from Codes.Task.Objects.Dot import Dot
from Codes.Task.Rewarder import Rewarder
from Codes.Task.Utils.GlobalValues import IMAGE_PATH, \
    BLACK, WHITE, GREEN, STAIR_STEP, RIGHT_PROB, \
    FIXATION_DELAY, STIMULUS_TIME, STARTING_DIR_PROB, \
    N_TEST_TRIALS, REWARD_DELAY, STIMULI_RADIUS

import random


class TaskLogic:
    def __init__(self, one_direction_prob, n_trials, n_test_trials, circle, n_dots=400, move_diff=10):
        self.n_trials = n_trials
        self.n_test_trials = n_test_trials
        self.n_dots = n_dots
        self.move_diff = move_diff
        self.one_direction_prob = one_direction_prob
        self.tracker = Tracker()
        self.dots = []
        self.starting_dir_prob = STARTING_DIR_PROB
        self.display = Display()
        self.central_circle = circle

    def initial_dots(self):
        trial_direction = Dir.Right if random.random() < RIGHT_PROB else Dir.Left
        self.dots = []
        for _ in range(self.n_dots):
            x, y = self.renew_dot()
            self.dots.append(Dot([x, y], one_direction_prob=self.one_direction_prob, selected_dir=trial_direction))

    def renew_dot(self):
        while True:
            x, y = random.uniform(-150, 150), random.uniform(-150, 150)
            if self.central_circle.contains(x, y):
                return [x, y]

    def give_reward(self, trial_index):

        trial_info = self.tracker.get_trial_info(trial_index)
        critic = self.tracker.get_critic()
        reward = 0

        if critic == 'Performance':
            reward = Rewarder.difficulty_reward(trial_info.one_direction_prob)
        elif critic == 'Meta':
            reward = Rewarder.meta_reward(
                trial_info.user_answer, trial_info.correct_answer, trial_info.user_confidence
            )
        elif critic == 'Confidence':
            reward = Rewarder.confidence_reward(trial_info.user_confidence)

        return reward

    def send_to_tracker(self, selected, confidence, one_direction_prob):
        answer = Tracker.majority_voting(self.dots, self.central_circle)
        selected = Dir.Right if selected == "right" else Dir.Left
        confidence = int(confidence)
        self.tracker.add_trial_info(answer, selected, confidence, one_direction_prob)

    def update_dots(self):
        for i, dot in enumerate(self.dots):
            # TODO: what to do? what not to do?
            dot.xy = dot.xy if self.central_circle.contains(dot.xy[0], dot.xy[1]) else self.renew_dot()
        return self.dots

    def move_dots(self):
        for dot in self.dots:
            if dot.move_direction == Dir.Right:
                dot.xy[0] += random.random() * self.move_diff
            else:
                dot.xy[0] -= random.random() * self.move_diff

    def change_dir_probability(self, diff):
        if diff < 0:
            self.one_direction_prob = max(self.one_direction_prob + diff, 0.54)
        else:
            self.one_direction_prob += diff

