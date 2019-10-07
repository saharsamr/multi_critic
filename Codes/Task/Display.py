import random
import sys
from psychopy import gui
from psychopy import visual, event, core
from Codes.Task.Objects.Dot import Dot
from Codes.Task.Utils.Directions import Dir
from Codes.Task.Tracker import Tracker
from Codes.Task.Utils.GlobalValues import PATH


BLACK = [-1, -1, -1]
WHITE = [1, 1, 1]


class Display:
    def __init__(self, n_trials=100 ,scr_size=(800, 800), n_dots=200, max_step_size=10):
        self.n_trials = n_trials
        self.n_dots = n_dots
        self.max_step_size = max_step_size
        self.win = visual.Window(size=scr_size, units="pix", fullscr=False, color=WHITE)
        self.tracker = Tracker(n_trials)

    def run_task(self):
        self.user_info_page()
        for _ in range(self.n_trials):
            self.dots = [Dot([random.uniform(-400, 400), random.uniform(-400, 400)])
                         for _ in range(self.n_dots)]
            self.fixation()
            self.random_dot_motion()
            selected = self.select_direction()
            confidence = self.get_confidence()
            self.send_to_tracker(selected[0], confidence[0])
        self.tracker.save()

    def send_to_tracker(self, selected, confidence):
        answer = Tracker.majority_voting(self.dots)
        selected = Dir.Right if selected == "right" else Dir.Left
        confidence = int(confidence)
        self.tracker.add_trial_info(answer, selected, confidence)

    def fixation(self):
        visual.TextStim(win=self.win, text="+", color=[0, 1, 0], pos=[500, 0]).draw()
        self.win.flip()
        Display.delay(0.5)

    def random_dot_motion(self):
        clock = core.Clock()
        while clock.getTime() < 2.0:
            visual.ElementArrayStim(
                win=self.win,
                nElements=self.n_dots,
                elementTex=None,
                elementMask="gauss",
                xys=[dot.xy for dot in self.dots],
                sizes=10,
                colors=BLACK
            ).draw()
            self.win.flip()
            self.move_dots()

    def move_dots(self):
        for dot in self.dots:
            if dot.move_direction == Dir.Right:
                dot.xy[0] += random.random() * self.max_step_size
            else:
                dot.xy[0] -= random.random() * self.max_step_size

    def select_direction(self):
        visual.TextStim(
            self.win,
            text="select the direction, which most of the dots are moving forward.",
            pos=(200,200), color=BLACK
        ).draw()
        visual.ImageStim(
            self.win,
            image=PATH + 'images/arrow_key.png',
            size=100, ori=270.0, pos=[200, -100]
        ).draw()
        visual.ImageStim(
            self.win,
            image=PATH + 'images/arrow_key.png',
            size=100, ori=90.0, pos=[-200, -100]
        ).draw()
        self.win.flip()
        return event.waitKeys(keyList=["left", "right"])

    def get_confidence(self):
        visual.TextStim(
            self.win,
            text='rate your confidence on previous trial from 1 to 6',
            pos=[200, 200], color=BLACK).draw()
        visual.ImageStim(self.win, image=PATH + 'images/1.png', pos=[-280, -100], size=100).draw()
        visual.ImageStim(self.win, image=PATH + 'images/2.png', pos=[-170, -100], size=100).draw()
        visual.ImageStim(self.win, image=PATH + 'images/3.png', pos=[-60, -100], size=100).draw()
        visual.ImageStim(self.win, image=PATH + 'images/4.png', pos=[50, -100], size=100).draw()
        visual.ImageStim(self.win, image=PATH + 'images/5.png', pos=[160, -100], size=100).draw()
        visual.ImageStim(self.win, image=PATH + 'images/6.png', pos=[270, -100], size=100).draw()
        self.win.flip()
        return event.waitKeys(keyList=["1", "2", "3", "4", "5", "6"])

    def user_info_page(self):
        user_page = gui.Dlg(title="please enter your info:")
        user_page.addText('Subject info')
        user_page.addField('First Name:')
        user_page.addField('Last Name:')
        user_page.addField('Age:')
        user_page.addField('Gender:', choices=['Male', 'Female', 'Other'])
        data = user_page.show()
        if user_page.OK:
            self.tracker.add_user_info(data[0], data[1], data[2], data[3])
        else:
           sys.exit()

    @staticmethod
    def delay(ms):
        clock = core.Clock()
        while clock.getTime() < ms:
            pass


