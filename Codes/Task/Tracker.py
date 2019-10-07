from Codes.Task.Utils.Directions import Dir
from Codes.Task.Utils.Genders import Gender
from Codes.Task.Logger import Logger

class Ttrial_info:
    def __init__(self, correct_answer, user_answer, user_confidence):
        self.correct_answer = correct_answer
        self.user_answer = user_answer
        self.user_confidence = user_confidence

class User_info:
    def __init__(self, first_name, last_name, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

class Tracker:
    def __init__(self, n_trials):
        self.user_info = None
        self.n_trials = n_trials
        self.trials_info = []

    def add_user_info(self, first_name, last_name, age, gender):
        if gender == "Male":
            gender = Gender.Male
        elif gender == "Female":
            gender = Gender.Female
        else:
            gender = Gender.Other
        self.user_info = User_info(first_name, last_name, age, gender)

    def add_trial_info(self, correct_answer, user_answer, user_confidence):
        self.trials_info.append(Ttrial_info(correct_answer, user_answer, user_confidence))

    def save(self):
        Logger.write_per_user_data(self)

    @staticmethod
    def majority_voting(dots):
        n_right, n_left = 0, 0
        for dot in dots:
            if dot.move_direction == Dir.Right:
                n_right += 1
            else:
                n_left += 1
        return Dir.Right if n_right > n_left else Dir.Left
