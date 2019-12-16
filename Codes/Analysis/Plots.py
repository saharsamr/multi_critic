import matplotlib.pyplot as plt


def plot_series(list_, label):
    plt.ylabel(label)
    plt.xlim(0, len(list_)-1)
    plt.plot(list_, '-bo')


def plot_series_in_same_plot(xs, labels, line_styles):
    for i, x in enumerate(xs):
        plt.plot(x, line_styles[i], label=labels[i])

    plt.legend(loc='best')


def compare_pre_post_scatter(x, yerr):
    plt.errorbar(x, range(1, len(x) + 1), yerr=yerr, fmt='o')
