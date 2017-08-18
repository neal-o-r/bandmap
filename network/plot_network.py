from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Div, BoxZoomTool, ResetTool, Title
from bokeh.embed import file_html
from bokeh.palettes import Category10 as palette
import json
import pandas as pd

def make_full_map(df):

    output_file("map.html", title="Band Map")

    desc = Div(text=open("../description.html", 'r').read(), width=1000)

    source = ColumnDataSource(data=dict(x=[], y=[], artist=[]))

    cs = lambda x: palette[10][x]
    df['Colour'] = df.Class.apply(cs)

    source.data = dict(
        x = df['X'],
        y = df['Y'],
        artist = df.Artist,
	colour = df.Colour,
    )

    hover = HoverTool(tooltips=[
        ("Artist", "@artist"),
    ])

    p = figure(plot_width=1000, plot_height=700,
        title='Band Map', toolbar_location="below",
        tools=[hover, BoxZoomTool(),ResetTool()])

    p.circle(x='x', y='y', size=7, alpha=0.6, color='colour',
        source=source, line_color=None)

    p.axis.visible = False

    show(p)


if __name__ == '__main__':

	df = pd.read_csv('top_points.csv')
	make_full_map(df)
