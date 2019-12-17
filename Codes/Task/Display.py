import random
import sys
from copy import deepcopy
from psychopy import gui
from psychopy import visual, event, core
from Codes.Task.Objects.Dot import Dot
from Codes.Task.Utils.Directions import Dir
from Codes.Task.Tracker import Tracker
from Codes.Task.Rewarder import Rewarder
from Codes.Task.Utils.GlobalValues import IMAGE_PATH, \
    BLACK, WHITE, GREEN, STAIR_STEP, RIGHT_PROB, \
    FIXATION_DELAY, STIMULUS_TIME, STARTING_DIR_PROB, \
    N_TEST_TRIALS, REWARD_DELAY, STIMULI_RADIUS


class Display:
    def __init__(self):
        # self.n_trials = n_trials
        # self.n_test_trials = n_test_trials
        # self.n_dots = n_dots
        # self.move_diff = move_diff
        # self.one_direction_prob = one_direction_prob
        self.win = None
        # self.tracker = Tracker()
        # self.dots = []
        # self.starting_dir_prob = STARTING_DIR_PROB
        self.central_circle = None

    def initial_main_objects(self, win, circle):
        self.win = win
        self.central_circle = circle

    def thanks_page(self):
        # self.user_info_page()
        # self.win = visual.Window(fullscr=True, units="pix", color=BLACK)
        # self.central_circle = visual.Circle(self.win, lineColor='white', lineWidth=4., radius=STIMULI_RADIUS)
        # self.description_page("Press Space when you are ready")
        # self.testing_phase()
        # self.description_page("From now, you will receive rewards, Press space when you are ready to start this part")
        # self.training_phase()
        # self.description_page("Here is the last part. you won't receive rewards any more, Press space to start")
        # self.testing_phase()
        visual.TextStim(win=self.win, text="thanks :)", color=GREEN, pos=[495, 0]).draw()
        self.win.flip()
        # self.tracker.save()

    # def testing_phase(self, n_test_trials):
        # for _ in range(n_test_trials):
        #     self.run_trial()
        # self.starting_dir_prob = self.tracker.get_training_start_dir_prob()

    # def training_phase(self):
    #     for indx in range(self.n_trials):
    #         self.run_trial()
    #         self.give_reward(N_TEST_TRIALS+indx)

    def run_trial(self, task_instance):
        # self.initial_dots()
        self.fixation()
        self.random_dot_motion(task_instance)
        selected = self.select_direction()
        confidence = self.get_confidence()

        return selected[0], confidence[0]
        # self.send_to_tracker(selected[0], confidence[0], self.one_direction_prob)
        # self.tracker.staircase(STAIR_STEP, self)

    # def initial_dots(self):
    #     trial_direction = Dir.Right if random.random() < RIGHT_PROB else Dir.Left
    #     self.dots = []
    #     for _ in range(self.n_dots):
    #         x, y = self.renew_dot()
    #         self.dots.append(Dot([x, y], one_direction_prob=self.one_direction_prob, selected_dir=trial_direction))

    # def renew_dot(self):
    #     while True:
    #         x, y = random.uniform(-150, 150), random.uniform(-150, 150)
    #         if self.central_circle.contains(x, y):
    #             return [x, y]

    def give_reward(self, reward):
        # trial_info = self.tracker.get_trial_info(trial_index)
        # critic = self.tracker.get_critic()
        # reward = 0
        #
        # if critic == 'Performance':
        #     reward = Rewarder.difficulty_reward(trial_info.one_direction_prob)
        # elif critic == 'Meta':
        #     reward = Rewarder.meta_reward(
        #         trial_info.user_answer, trial_info.correct_answer, trial_info.user_confidence
        #     )
        # elif critic == 'Confidence':
        #     reward = Rewarder.confidence_reward(trial_info.user_confidence)

        visual.TextStim(win=self.win, text=str(int(reward*100)), color=GREEN, pos=[495, 0]).draw()
        self.win.flip()
        Display.delay(REWARD_DELAY)

    # def send_to_tracker(self, selected, confidence, one_direction_prob):
    #     answer = Tracker.majority_voting(self.dots, self.central_circle)
    #     selected = Dir.Right if selected == "right" else Dir.Left
    #     confidence = int(confidence)
    #     self.tracker.add_trial_info(answer, selected, confidence, one_direction_prob)

    def fixation(self):
        visual.TextStim(win=self.win, text="+", color=GREEN, pos=[495, 0]).draw()
        self.win.flip()
        Display.delay(FIXATION_DELAY)

    def description_page(self, txt):
        visual.TextStim(win=self.win, text=txt, color=GREEN, alignHoriz="center", alignVert="center").draw()
        self.win.flip()
        event.waitKeys(keyList=["space"])

    def random_dot_motion(self, task_instance):
        clock = core.Clock()
        while clock.getTime() < STIMULUS_TIME:
            self.central_circle.draw()
            dots = task_instance.update_dots()
            visual.ElementArrayStim(
                win=self.win,
                nElements=len(dots),
                elementTex=None,
                elementMask="gauss",
                xys=[dot.xy for dot in dots],
                sizes=15,
                colors=WHITE,
            ).draw()
            self.win.flip()
            task_instance.move_dots()

    # def move_dots(self):
    #     for dot in self.dots:
    #         if dot.move_direction == Dir.Right:
    #             dot.xy[0] += random.random() * self.move_diff
    #         else:
    #             dot.xy[0] -= random.random() * self.move_diff

    def select_direction(self):
        visual.TextStim(
            self.win,
            text="select the direction, which most of the dots are moving forward.",
            pos=(200, 200), color=WHITE
        ).draw()
        visual.ImageStim(
            self.win,
            image=IMAGE_PATH + 'arrow_key.png',
            size=100, ori=270.0, pos=[200, -100]
        ).draw()
        visual.ImageStim(
            self.win,
            image=IMAGE_PATH + 'arrow_key.png',
            size=100, ori=90.0, pos=[-200, -100]
        ).draw()
        self.win.flip()
        return event.waitKeys(keyList=["left", "right"])

    def get_confidence(self):
        visual.TextStim(
            self.win,
            text='rate your confidence on previous trial from 1 to 6',
            pos=[200, 200], color=WHITE).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '1.png', pos=[-280, -100], size=100).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '2.png', pos=[-170, -100], size=100).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '3.png', pos=[-60, -100], size=100).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '4.png', pos=[50, -100], size=100).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '5.png', pos=[160, -100], size=100).draw()
        visual.ImageStim(self.win, image=IMAGE_PATH + '6.png', pos=[270, -100], size=100).draw()
        self.win.flip()
        return event.waitKeys(keyList=["1", "2", "3", "4", "5", "6"])

    def user_info_page(self):
        user_page = gui.Dlg(title="please enter your info:")
        user_page.addText('Subject info')
        user_page.addField('First Name:')
        user_page.addField('Last Name:')
        user_page.addField('Age:')
        user_page.addField('Gender:', choices=['Male', 'Female', 'Other'])
        user_page.addField('Critic:', choices=['Performance', 'Meta', 'Confidence'])
        data = user_page.show()
        if user_page.OK:
            return data[0], data[1], data[2], data[3], data[4]
        else:
           sys.exit()

    # def change_dir_probability(self, diff):
    #     if diff < 0:
    #         self.one_direction_prob = max(self.one_direction_prob + diff, 0.54)
    #     else:
    #         self.one_direction_prob += diff

    @staticmethod
    def delay(ms):
        clock = core.Clock()
        while clock.getTime() < ms:
            pass


