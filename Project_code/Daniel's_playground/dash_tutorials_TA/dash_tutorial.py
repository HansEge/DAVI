# import standard dash components.
# we use the dcc module for the slider widgets, and html to give us a basic <div> container to
# put our layout into.
import dash
import dash_core_components as dcc
import dash_html_components as html

# these imports are for piping data from the widget into the visualization using the callback
# function whenever we drag around the slider.
from dash.dependencies import Input, Output

# we also import plotly express to give us access to the dataset and the scatter plot figure type.
import plotly.express as px

# these external style sheet allow us to collaborate together with designers on our team, who can
# create the visuals in CSS, which we can then import like this into our Python code.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# we use the gapminder dataset from express here.
df = px.data.gapminder()

# the layout consists of a standard html <div> container, in which we place the components for the
# visualization and the slider. Notice how we assign an id to both componets, which allows us to
# reference these components later on in the callback function.
# The properties differ between components. The Dash API explains in detail, what properties are
# available and how to use them.
# for more involved layouts, we can also use the dash_bootstrap_components module, which we can
# install via pip.
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


# In callback functions like this one, we can define, how the data flows between our components.
# In this case, we want the value of our slider to update the scatterplot figure everytime we move
# it around.
# We use the Output('component-id', 'property') function to define, which component should receive
# the output of the function into which property, and the Input() function to define, where our data
# comes from (and based on which events we want to update our visualization).
# Notice that we can define multiple inputs here: We could have multiple widgets to configure the
# gapminder scatter plot, and each would show up as a Input() in the Array below.
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    # our static gapminder visualization in plotly. Since the data is filtered based on the value
    # we set on our sliders, the figure will show only one year at a time.
    fig = px.scatter(filtered_df,
        x="gdpPercap",
        log_x=True,
        y="lifeExp",
        color="continent",
        size="pop",
        size_max=75,
        height=750,
        hover_name="country"
    )

    # these two lines ensure, that the axes stay the same at different years. Without them, plotly
    # would "optimize" the axes, which makes it hard to follow the data.
    fig.update_yaxes(range=[20, 90])
    fig.update_xaxes(range=[2.5, 5])

    # this line makes plotly animate the visualization between two years.
    fig.update_layout(transition_duration=500)

    return fig

# the code below starts webserver on the default port :8050 in debug mode.
app.run_server(debug=True)