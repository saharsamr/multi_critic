from Codes.Analysis.AnalyseData import AnalyseData
from Codes.Analysis.Plots import plot_series, plot_series_in_same_plot, compare_pre_post_scatter

import matplotlib.pyplot as plt


if __name__ == "__main__":

    analyser = AnalyseData('Data/khers_sharifi.txt')

    plt.figure("accuracy")
    accuracy = analyser.accuracy(bin_size=10)
    plot_series(accuracy, f'subject accuracy')

    plt.figure("difficulty")
    difficulty = analyser.difficulties(bin_size=10)
    plot_series(difficulty, "subject difficulty")

    plt.figure("confidence")
    confidence = analyser.confidences(bin_size=10)
    plot_series(confidence, "subject difficulty")

    plt.figure("pre-post phase difficulty")
    avg_difficulty, min_difficulty, max_difficulty = analyser.pre_post_training_difficulty()
    compare_pre_post_scatter(
        avg_difficulty, [[avg_difficulty[0] - min_difficulty[0], avg_difficulty[1] - min_difficulty[1]],
                         [max_difficulty[0] - avg_difficulty[0], max_difficulty[1] - avg_difficulty[1]]]
    )

    plt.figure("pre-post phase confidence")
    avg_confidence, min_confidence, max_confidence = analyser.pre_post_training_avg_confidence()
    compare_pre_post_scatter(
        avg_confidence, [[avg_confidence[0] - min_confidence[0], avg_confidence[1] - min_confidence[1]],
                         [max_confidence[0] - avg_confidence[0], max_confidence[1] - avg_confidence[1]]]
    )

    plt.figure("pre-post phase meta")
    avg_meta, min_meta, max_meta = analyser.pre_post_training_meta()
    compare_pre_post_scatter(
        avg_meta, [[avg_meta[0] - min_meta[0], avg_meta[1] - min_meta[1]],
                   [max_meta[0] - avg_meta[0], max_meta[1] - avg_meta[1]]]
    )

    performance_reward = analyser.rewards("Performance", bin_size=10)
    meta_reward = analyser.rewards("Meta", bin_size=10)
    confidence_reward = analyser.rewards("Confidence", bin_size=10)
    plt.figure('meta subject')
    plot_series_in_same_plot(
        [performance_reward, meta_reward, confidence_reward],
        ["performance", "meta", "confidence"],
        ['r-', 'b-', 'g-']
    )

    plt.show()
