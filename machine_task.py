from Codes.Task.TaskLogic import TaskLogic
from Codes.Task.Utils.GlobalValues import BLACK, STAIR_STEP, \
    STARTING_DIR_PROB, N_TEST_TRIALS, STIMULI_RADIUS, N_TRIALS

from psychopy import visual


win = visual.Window(fullscr=True, units="pix", color=BLACK)
circle = visual.Circle(win, lineColor='white', lineWidth=4., radius=STIMULI_RADIUS)

task_instance = TaskLogic(STARTING_DIR_PROB, N_TRIALS, N_TEST_TRIALS, circle, n_dots=400, move_diff=10)


def run_trial():
    task_instance.initial_dots()
    # selected_dir, confidence = display.run_trial(task_instance)
    task_instance.send_to_tracker(selected_dir, confidence, task_instance.one_direction_prob)
    task_instance.tracker.staircase(STAIR_STEP, task_instance)


def test_phase():
    for _ in range(N_TEST_TRIALS):
        run_trial()


def train_phase():
    for i in range(N_TRIALS):
        run_trial()
        reward = task_instance.give_reward(N_TEST_TRIALS + i)
        # display.give_reward(reward)


def run_task(critic, test_num):

    task_instance.tracker.add_user_info('machine', test_num, 0, 'Other', critic)
