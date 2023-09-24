import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(data, ratio_name): 
    # num_bins = int(1 + np.log2(len(data))) #sturges
    # print("number of bins:", num_bins)
    # num_bins = int((max(data) - min(data)) / bin_width) #scott
    # num_bins = int(np.sqrt(len(data))) #square root
    num_bins = 100 
    # num_bins = int(np.max(data)-np.min(data))

    # Create a histogram
    plt.hist(data, bins=num_bins, edgecolor='k')  # Adjust the number of bins as needed
    plt.xlabel(f"{ratio_name}")
    plt.ylabel('Frequency')
    plt.title('Histogram of a Continuous Variable')
    plt.grid(True)

    # Show the histogram
    plt.show()

def plot_xy(data): 
    indices = np.arange(len(data))
    plt.plot(indices, data, marker='o', linestyle='-')
    plt.xlabel('ticker index')
    plt.ylabel('reward')
    plt.title('oooooo')
    plt.show()

