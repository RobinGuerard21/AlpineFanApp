import plotly.graph_objs as go
import plotly.io as pio
import os.path as path

custom_theme = go.layout.Template()

# Set background color
custom_theme.layout.paper_bgcolor = '#fffffa'
custom_theme.layout.plot_bgcolor = '#fffffa'

# Set font family and color
custom_theme.layout.font.family = 'Raleway Medium'
custom_theme.layout.font.color = '#2c3e50'

# Set background line color
custom_theme.layout.xaxis.gridcolor = '#ecf0f1'
custom_theme.layout.yaxis.gridcolor = '#ecf0f1'

base = path.dirname(path.abspath(__file__))

# Register the custom theme
pio.templates["alpine"] = custom_theme
pio.templates.default = "alpine"