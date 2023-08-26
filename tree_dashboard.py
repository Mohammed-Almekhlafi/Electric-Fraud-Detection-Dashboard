from dash import Dash, dcc, html
import plotly.graph_objects as go

from dash.dependencies import Input, Output
import numpy as np

# function to generate random numbers between 0 and 50 , but 95% the generated numbers must be in 45 to 50 range to make generated data as real data
def generate_custom_random():
    # Generate a random number to determine the range
    range_selector = np.random.uniform()

    # Decide which range to select based on the random number
    if range_selector <= 0.05:  # 5% chance
        return int(np.random.uniform(0, 45))
    else:  # 95% chance
        return int(np.random.uniform(45, 50))

#lables of all nodes (from 0 to 20 )
labels = list(map(str, range(21)))
# x and y coordinates of nodes
Xn=[4, 10, 16, 2, 4, 6, 8, 10, 12, 14, 16, 18, 2, 4, 6, 8, 10, 12, 14, 16, 18]
Yn=[ 12, 12, 12, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4]

# every line can represent by 2 points, here list of x and y coordinates of lines between nodes
# the math structure Xl= [x values for line 1 , x values for line 1,...x values for line 18]
# Xl=[(4, 2), (4, 4), (4, 6), ......(18, 18)]
Xl=[4, 2, 4, 4, 4, 6, 10, 8, 10, 10, 10, 12, 16, 14, 16, 16, 16, 18, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10, 12, 12, 14, 14, 16, 16, 18, 18]
Yl=[12, 8, 12, 8, 12, 8, 12, 8, 12, 8, 12, 8, 12, 8, 12, 8, 12, 8, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4]


x_y = []
fig = go.Figure()

def tree_draw(Xn, Yn, Xl, Yl):
    node_values = [150, 150, 150, 50, 50, 50, 50, 50, 50, 50, 50, 50, generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random(), generate_custom_random()]

    #draw the inital tree chart
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             mode='markers+text',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=40,
                                         color= '#FFFFFF',
                                         line=dict(color='rgb(217, 227, 23)', width=1)
                                         ),
                             text=node_values,
                             hoverinfo='text',
                             opacity=0.8
                             ))
    # make nested list have all lines = [[[nod1 of line1], [node2 of line1]],[[node1 of line2],[node2 of line2]],[...etc]]
    # nod1 of line1=[x1, y1, node_value]

    for i in range(0, len(Xl), 2):
        lnm = []
        ln1 = []
        ln2 = []

        ln1.append(Xl[i])
        ln1.append(Yl[i])
        lnm.append(ln1)

        ln2.append(Xl[i + 1])
        ln2.append(Yl[i + 1])
        lnm.append(ln2)

        x_y.append(lnm)

    # adding nodes values
    for i in range(len(x_y)):
        if i in [0, 1, 2]:
            x_y[i][0].append(node_values[0])
            x_y[i][1].append(node_values[i + 3])
        elif i in [3, 4, 5]:
            x_y[i][0].append(node_values[1])
            x_y[i][1].append(node_values[i + 3])

        elif i in [6, 7, 8]:
            x_y[i][0].append(node_values[2])
            x_y[i][1].append(node_values[i + 3])


        else:
            x_y[i][0].append(node_values[i - 6])
            x_y[i][1].append(node_values[i + 3])
    # draw red line for the detected path and blue for the normal paths
    for i in range(len(x_y)):
        x = [x_y[i][0][0], x_y[i][1][0]]
        y = [x_y[i][0][1], x_y[i][1][1]]
        if i in range(9,18) and  (x_y[i][0][2] - x_y[i][1][2]) > 10:


            fig.add_trace(go.Scatter(x=x,
                                     y=y,
                                     mode='lines',
                                     line=dict(color='rgb(255,0,0)', width=3),
                                     hoverinfo='none'
                                     ))
        else:
            fig.add_trace(go.Scatter(x=x,
                                     y=y,
                                     mode='lines',
                                     line=dict(color='rgb(137, 207, 240)', width=2),
                                     hoverinfo='none'
                                     ))
    return fig


app = Dash()
app.layout = html.Div([
    # Add title to the dashboard
    html.H1("electric fraud detection dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
    # add the network graph
    dcc.Graph(id='dynamic-graph',figure=fig),

    # make dashboard updated automatically updated every 20 seconds
    dcc.Interval(
        id='interval-component',
        interval=20 * 1000,  # Update every 20 seconds (adjust as needed)
        n_intervals=0,
        max_intervals=50
    )
])
@app.callback(Output('dynamic-graph', 'figure'), Input('interval-component', 'n_intervals'))

def update_graph(n):

    x_y.clear()
    fig.data = []

    new_cycle= tree_draw(Xn, Yn, Xl, Yl)
    return new_cycle
if __name__ == '__main__':
    app.run_server(debug=True, )
