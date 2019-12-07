from Codes.Task.Utils.GlobalValues import MIN_COHERENCY


class Rewarder:
    @staticmethod
    def difficulty_reward(one_dir_prob):
        COEFF = -1 / (1 - MIN_COHERENCY)
        BIAS = 1 - MIN_COHERENCY

        coherency = abs(one_dir_prob - (1 - one_dir_prob))
        difficulty = COEFF * coherency + BIAS

        return difficulty

    @staticmethod
    def confidence_reward(user_confidence):

        MAX_CONFIDENCE = 6

        return user_confidence / MAX_CONFIDENCE

    @staticmethod
    def meta_reward(user_answer, correct_answer, user_confidence):

        MAX_CONFIDENCE = 6
        
        QSR = lambda accuracy, p_correct_: 1 - (accuracy - p_correct_) ** 2 

        p_correct = -1 / (MAX_CONFIDENCE - 1) + user_confidence / (MAX_CONFIDENCE - 1)

        if user_answer == correct_answer:
            return QSR(1, p_correct)
        
        return QSR(0, p_correct)
