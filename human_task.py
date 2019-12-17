from Codes.Task.TaskLogic import TaskLogic
from Codes.Task.Display import Display
from Codes.Task.Utils.GlobalValues import BLACK, STAIR_STEP, RIGHT_PROB, \
    FIXATION_DELAY, STIMULUS_TIME, STARTING_DIR_PROB, \
    N_TEST_TRIALS, REWARD_DELAY, STIMULI_RADIUS, N_TRIALS

from psychopy import visual


win = visual.Window(fullscr=True, units="pix", color=BLACK)
circle = visual.Circle(win, lineColor='white', lineWidth=4., radius=STIMULI_RADIUS)


task_instance = TaskLogic(STARTING_DIR_PROB, N_TRIALS, N_TEST_TRIALS, circle, n_dots=400, move_diff=10)
display = Display()


def run_trial():
    task_instance.initial_dots()
    selected_dir, confidence = display.run_trial(task_instance)
    task_instance.send_to_tracker(selected_dir, confidence, task_instance.one_direction_prob)
    task_instance.tracker.staircase(STAIR_STEP, task_instance)


def test_phase():
    for _ in range(N_TEST_TRIALS):
        run_trial()


def train_phase():
    for i in range(N_TRIALS):
        run_trial()
        reward = task_instance.give_reward(N_TEST_TRIALS + i)
        display.give_reward(reward)


def run_task():

    user_info = display.user_info_page()
    task_instance.tracker.add_user_info(**user_info)

    display.initial_main_objects(win, circle)

    display.description_page("Press Space when you are ready")
    test_phase()
    task_instance.starting_dir_prob = task_instance.tracker.get_training_start_dir_prob()

    display.description_page("From now, you will receive rewards, Press space when you are ready to start this part")
    train_phase()

    display.description_page("Here is the last part. you won't receive rewards any more, Press space to start")
    test_phase()

    display.thanks_page()

    task_instance.tracker.save()

