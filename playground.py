# import numpy as np
# import matplotlib.pyplot as plt

# data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])
# num_bins = int(np.ceil(np.log2(len(data)) + 1))

# hist_values, bin_edges = np.histogram(data, bins=num_bins)
 
# plt.hist(data, bins=num_bins, edgecolor='k', alpha=0.7)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Continuous Frequency Distribution')
# plt.grid(True)
# plt.show()

# # import numpy as np
# # import plotly.express as px
# # import pandas as pd

# # # Sample data
# # data = np.array([10, 15, 20, 22, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 70])

# # # Determine the number of bins
# # num_bins = int(np.ceil(np.log2(len(data)) + 1))

# # # Create a histogram
# # hist_values, bin_edges = np.histogram(data, bins=num_bins)

# # # Create a DataFrame for Plotly
# # df = pd.DataFrame({'Value': bin_edges[:-1], 'Frequency': hist_values})

# # # Create an interactive histogram using Plotly
# # fig = px.bar(df, x='Value', y='Frequency', title='Interactive Continuous Frequency Distribution')

# # # Customize the appearance
# # fig.update_traces(marker_color='royalblue', opacity=0.7)
# # fig.update_xaxes(title_text='Value')
# # fig.update_yaxes(title_text='Frequency')
# # fig.update_layout(bargap=0.05)
# # fig.update_layout(showlegend=False)

# # # Show the interactive plot
# # fig.show()


# a = ['a', 'b', 'c']
# b = a
# b.remove('a')
# print(a)
# print(b)

ordered_ratios;
[34.858069832869404, 62.793969769849845, 72.27714071468431, 119.64796942633552, 139.43227933147762, 160.9809043190696, 186.39894184313323, 205.90580784997275, 210.80832708449591, 347.2137151979933, 571.2225637128277, 590.2633158365886, 632.4249812534877, 655.8481287073206, 1041.6411455939797, 1180.5266316731772, 1362.1461134690505, 1362.1461134690505, 4426.974868774414, 4426.974868774414, 5902.633158365886, 8853.949737548828, 17707.899475097656]
ordered concepts: 
[5.08, 2.82, 2.45, 1.48, 1.27, 1.1, 0.95, 0.86, 0.84, 0.51, 0.31, 0.3, 0.28, 0.27, 0.17, 0.15, 0.13, 0.13, 0.04, 0.04, 0.03, 0.02, 0.01]
['DOCN', 'CDAY', 'CRWD', 'BOX', 'BLKB', 'DT', 'CALX', 'ATEN', 'TDC', 'PRGS', 
 'CVLT', 'WDAY', 'PANW', 'PTC', 'AKAM', 'ORCL', 'QLYS', 'VMW', 'PLUS', 'FFIV', 'MSFT', 'ADBE', 'NOW']