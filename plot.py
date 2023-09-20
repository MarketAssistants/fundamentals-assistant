import plotly.express as px
import pandas as pd

# Sample data (you can replace this with your own data)
data = pd.DataFrame({'Names': ['yacine', 'boussad', 'salim', 'nadji', 'tahar', 'nacer', 'anis', 'yanis', 'kamel', 'hani', 'ahcene', 'ouchen', 'ahmad', 'ikram', 'amir'], 
                     'Scores':[450, 350, 330, 370, 200, 250, 270, 290, 300, 300, 30, 100, 120, 130,110]})
df_sorted = data.sort_values(by='Scores')
length = len(data['Names'])
print("length is: ", length)

# Create an interactive histogram using Plotly Express
# help(px.histogram)
fig = px.histogram(df_sorted, x='Names', y='Scores', nbins=5, title='Interactive Histogram')

np.histogram(Scores, bins=5)
# Show the plot (in a Jupyter notebook, it will be displayed inline)
fig.show()