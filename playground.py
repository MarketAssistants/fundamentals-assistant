import numpy as np
import matplotlib.pyplot as plt

data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])
num_bins = int(np.ceil(np.log2(len(data)) + 1))

hist_values, bin_edges = np.histogram(data, bins=num_bins)
 
plt.hist(data, bins=num_bins, edgecolor='k', alpha=0.7)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Continuous Frequency Distribution')
plt.grid(True)
plt.show()

# import numpy as np
# import plotly.express as px
# import pandas as pd

# # Sample data
# data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])

# # Determine the number of bins
# num_bins = int(np.ceil(np.log2(len(data)) + 1))

# # Create a histogram
# hist_values, bin_edges = np.histogram(data, bins=num_bins)

# # Create a DataFrame for Plotly
# df = pd.DataFrame({'Value': bin_edges[:-1], 'Frequency': hist_values})

# # Create an interactive histogram using Plotly
# fig = px.bar(df, x='Value', y='Frequency', title='Interactive Continuous Frequency Distribution')

# # Customize the appearance
# fig.update_traces(marker_color='royalblue', opacity=0.7)
# fig.update_xaxes(title_text='Value')
# fig.update_yaxes(title_text='Frequency')
# fig.update_layout(bargap=0.05)
# fig.update_layout(showlegend=False)

# # Show the interactive plot
# fig.show()



