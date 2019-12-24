import sys
from psychopy import gui
from psychopy import visual, event, core
from Codes.Task.Utils.GlobalValues import IMAGE_PATH, \
    WHITE, GREEN, FIXATION_DELAY, STIMULUS_TIME, REWARD_DELAY


class Display:
    def __init__(self):
        self.win = None
        self.central_circle = None

    def initial_main_objects(self, win, circle):
        self.win = win
        self.central_circle = circle

    def thanks_page(self):
        visual.TextStim(win=self.win, text="thanks :)", color=GREEN, pos=[495, 0]).draw()
        self.win.flip()

    def run_trial(self, task_instance):
        self.fixation()
        self.random_dot_motion(task_instance)
        selected = self.select_direction()
        confidence = self.get_confidence()
        return selected[0], confidence[0]

    def give_reward(self, reward):
        visual.TextStim(win=self.win, text=str(int(reward*100)), color=GREEN, pos=[495, 0]).draw()
        self.win.flip()
        Display.delay(REWARD_DELAY)

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

    @staticmethod
    def delay(ms):
        clock = core.Clock()
        while clock.getTime() < ms:
            pass


