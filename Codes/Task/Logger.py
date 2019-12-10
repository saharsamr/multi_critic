PATH = "/Users/sadegh/Desktop/multi_critic/Data/"


class Logger:
    @staticmethod
    def write_per_user_data(tracker):
        file = open(PATH + tracker.user_info.first_name + "_" + tracker.user_info.last_name + ".txt", "a+")
        file.write(
            "age: " + tracker.user_info.age + ", gender: " + tracker.user_info.gender.name
            + ", critic: " + tracker.user_info.critic + "\n")
        for i, trial in enumerate(tracker.trials_info):
            file.write(
                "trial#" + str(i+1) + ": " + trial.correct_answer.name
                + ", " + trial.user_answer.name + ", " + str(trial.user_confidence) +
                ", " + str(trial.one_direction_prob) + "\n"
            )
        file.close()
