import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

from dash.dependencies import Input, Output

################################################################################
# Dataframe #                                                                  #
#############                                                                  #
# We are going to analize and visualize the decay of the doubly charged Higgs  #
# with the decay widths and Branching ratio data generated through Madgraph.   #
################################################################################

# Here we can joint two data sets generated separately (1000+500 points), but we keep just the 1000 points data
# for simplicity.

# data_frame_dir1 = 'D:/projects/LLP/23_model/Random_Analisis_2/Cards/Total_Decays_1000.csv'
# data_frame_dir2 = 'D:/projects/LLP/23_model/Random_Analisis_2/Cards/Total_Decays_517.csv'
# df1 = pd.read_csv(data_frame_dir1, index_col=False)
# df2 = pd.read_csv(data_frame_dir2, index_col=False)
# df = pd.concat([df1,df2])


data_frame_dir1 = 'data/Total_Decays_1000.csv'
df = pd.read_csv(data_frame_dir1, index_col=False)
df = df.loc[(df.LHT2 >= -4.0) & (df.VevTriplet >= 1e-4)  ,:]
df.drop(list(df)[0], inplace=True, axis=1)

##########
# Colors #
##########

my_colors = ['#14213d', '#fca311', '#e5e5e5', '#ffffff','000000'  ]


"""
#####################################
# Functions that generate the plots #
#####################################
"""


##########################
# Principal scatter plot #
##########################

fig = go.Figure()

to_sci = lambda x: np.format_float_scientific(x, precision=2)

customdata    = np.stack((df.index, df.VevTriplet.apply(to_sci), 
                            df.LHT2, df.Kappa.apply(to_sci)), axis=-1)

hovertemplate = ('<i>index</i>: %{customdata[0]}'+\
                 '<br><b>&#955;<sup>\'</sup><sub>HT</sub> </b>: %{customdata[2]:.2f}'+\
                 '<br><b>&#957;<sub>&#916;</sub></b>: %{customdata[1]}'+\
                 '<br><b>&#954;	</b>: %{customdata[3]}')



trace_vev = go.Scattergl(
    x = df.Hppmass,
    y = np.log10((2.998*1e+8*6.582e-25)*df.TotalDecayHpp**(-1)),
    
    mode='markers',
    marker=dict(
        size=6,
        color= np.log10(df.VevTriplet),  #  set color equal to a variable
        colorscale= 'Blues',             #  'Blues', # one of plotly colorscales
        showscale=True,
        colorbar = dict(x = 1, thickness=10, title= '&#957;<sub>&#916;</sub>',
                        tickvals=[-2.5, -3, -3.5], ticktext=["10<sup>-2.5</sup>", "10<sup>-3</sup>", "10<sup>-3.5</sup>"])
    ),
    hovertext= df.LHT2,
    hoverinfo = 'text',
    customdata= customdata,
    hovertemplate= hovertemplate
)

trace_lht2 = go.Scattergl(
    x = df.Hppmass,
    y = np.log10((2.998*1e+8*6.582e-25)*df.TotalDecayHpp**(-1)),
    
    mode='markers',
    marker=dict(
        size= 10,
        color= df.LHT2, #set color equal to a variable
        colorscale= 'YlOrBr', # one of plotly colorscales
        showscale=True,
        colorbar = dict(x = 1.12, thickness=10,
                         title= '&#955;<sup>\'</sup><sub>HT</sub>',
                         tickfont=dict(size=14) )
        
    )
    ,
    hoverinfo='skip',
)


fig.add_trace(trace_lht2)
fig.add_trace(trace_vev)
fig.update_traces(showlegend=False)


fig.update_layout(xaxis=dict(
        title='m<sub>H<sup>&#x00B1;&#x00B1; </sup></sub> [GeV]'
    ),
    yaxis=dict(
        title=" c&#964; [m]",
        tickvals=[1, 0, -1,-2,-3,-4,-5],
        ticktext =['10 m', '1 m', '10 cm', '1 cm', "1 mm",'10<sup>-4</sup>','10<sup>-5</sup>']
    ))

fig.update_layout(hovermode='closest')
fig.update_layout(template = 'plotly_dark')
fig.update_layout(  font=dict(
                    family="Times New Roman",
                    size=18))
fig.update_layout(width=800, height=500)

fig.add_annotation( text =    
"Scatter plot for c&#964; versus m<sub>H<sup>&#x00B1;&#x00B1;</sup></sub> values. \
You can see more information about each point in <br>the parameter space \
through the plots on the right and the data table.  ",
                    xref="paper", yref="paper",
                    x=  -0.05, y=1.23, showarrow=False, align = 'left')


##############
# Bar masses #
##############

def create_mass_plot(index):    
    
    masses = df[df.index==index].to_numpy()[0][0:5]

    names_html = ['hSM', 'A', 'H', 'H<sup>&#x00B1; </sup>','H<sup>&#x00B1;&#x00B1; </sup>']

    fig_masses = go.Figure()
    colors = [my_colors[0]] * 5
    colors[4] = my_colors[1]


    bar_trace = go.Bar( x=names_html , y=masses, text=np.round(masses,2),
                        textposition='inside',marker_color=colors)

    fig_masses.add_trace(bar_trace)
    fig_masses.update_layout(template = 'plotly_dark')
    #fig.update_layout(template = 'plotly_white')
    fig_masses.update_layout(   font=dict(  family="Times New Roman",
                                            size=18))
    fig_masses.update_layout(width=400, height=500)

    fig_masses.update_layout(xaxis=dict(
            title='Particle'
        ),
        yaxis=dict(
            title=" Mass [GeV]",
        
        ))
    fig_masses.update_layout(   font=dict(
                                family="Times New Roman",
                                size=18),
                                title_text = 'Mass spectrum')

    fig_masses.add_annotation(  text="Mass value for all the scalar particles",
                                xref="paper", yref="paper",
                                x=  -0.25, y=1.1, showarrow=False, align = 'left')

    return fig_masses

#############
# PIE CHART #
#############

BRS_dir = 'data/Hpp_BRs.csv'
BR_df = pd.read_csv(BRS_dir)
BR_df.set_index(['index','NDA'], inplace=True)

def values_labels(ind):
    channels = BR_df.loc[ind].index.unique()
    labels = [(str(i)+' body' )for i in channels]
    values = [(BR_df.loc[ind,i].BR.sum()) for i in channels]
    return labels, values


def create_pie(ind):
    
    labels, values = values_labels(ind)

    # Use `hole` to create a donut-like pie chart
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3 , marker_colors = my_colors)])
    fig_pie.update_layout(template = 'plotly_dark')
    fig_pie.update_layout(width=400, height=500)
    fig_pie.update_layout(  font=dict(
                            family="Times New Roman",
                            size=18),
                            title_text = 'Decay channels for point: '+str(ind))
    fig_pie.add_annotation( text="Percentages of total branching ratios for each <br>n-body decay channel",
                            xref="paper", yref="paper",
                            x=  -0.3, y=-0.1, showarrow=False, align = 'left')
                            

        
    
    return fig_pie

###########################
# DECAY CHANNELS CONTOURS #
###########################

df_dec = pd.read_csv('data/df_channels')
df_dec.set_index(['index'], inplace= True)

def create_contour(x):
    # Channel can be: two_body, x= 2/ three_body, x = 3 / four_body, x= 4
    #
    fig_contour = go.Figure()
    if (x == 2):
        fig_contour.add_trace(go.Histogram2dContour(
                x = df_dec.loc[df_dec.two_body == True].Hppmass ,
                y = df_dec.loc[df_dec.two_body == True].ctau,
        ))
        fig_contour.update_layout(  font=dict(
                            family="Times New Roman",
                            size=15),
                            )
    elif (x == 3):
        fig_contour.add_trace(go.Histogram2dContour(
                x = df_dec.loc[df_dec.three_body == True].Hppmass ,
                y = df_dec.loc[df_dec.three_body == True].ctau,
        ))
        fig_contour.update_layout(  font=dict(
                            family="Times New Roman",
                            size=15),
                            )
    elif (x == 4):
        fig_contour.add_trace(go.Histogram2dContour(
                x = df_dec.loc[df_dec.four_body == True].Hppmass ,
                y = df_dec.loc[df_dec.four_body == True].ctau,
        ))
        fig_contour.update_layout(  font=dict(
                            family="Times New Roman",
                            size=15),
                            )

    fig_contour.update_layout(template = 'plotly_dark')
    fig_contour.update_traces(contours = dict(coloring = 'lines'),
                        colorscale = 'Blues',
                        #ncontours =  30,
                        reversescale = False,
                        colorbar = dict(thickness = 10),
                        line = dict( width = 2))
    fig_contour.update_layout(xaxis=dict(
            title='m<sub>H<sup>&#x00B1;&#x00B1; </sup></sub> [GeV]',

            tickvals=[40,60,80,100,120],
        ),
        yaxis=dict(
            title=" c&#964; [m]",
            tickvals=[1, 0, -1,-2,-3,-4,-5],
            ticktext =['10 m', '1 m', '10 cm', '1 cm', "1 mm",'10<sup>-4</sup>','10<sup>-5</sup>']
        )
        
    )
    fig_contour.update_layout(  font=dict(
                        family="Times New Roman",
                        size=18))
    fig_contour.update_layout(xaxis_range=[30,140])
    fig_contour.update_layout(yaxis_range=[-5,2])
    fig_contour.update_layout(width=800, height=500)

    return fig_contour

    


######################
# Display data frame #
######################

to_sci4 = lambda x: np.format_float_scientific(x, precision=4)

def display_data(ind):
        
    display = BR_df.reset_index()
    display.set_index(['index'], inplace=True)
    display = display[['NDA',  'ID1', 'ID2', 'ID3', 'ID4','BR']]
    display = display.loc[ind].sort_values(by=['BR'], ascending=False) 
    display.BR = display.BR.apply(to_sci4)
    
    return display




"""
##################
# App initiation # 
##################
"""



app = dash.Dash(__name__, title='Decay data')
server = app.server


"""
##########
# LAYOUT #
##########
"""

colors = {
    'background': '#111111'
}



app.layout = html.Div(style={'backgroundColor': '#011627'}, children = [ 
    

    html.Div([

        html.H1(['23-Model'],style={'color': 'white', 'textAlign': 'center',
                                    'fontFamily': 'Times New Roman',} ),
        html.H6([   'Data dashboard to analize the decay channels of the doubly \
                    charged Higgs in the 23-Model'],
                    style={'color': 'white', 'textAlign': 'center',
                                    'fontFamily': 'Times New Roman',} )
    ],style = dict(backgroundColor = '#111111')),

    html.Div([


        dcc.Graph(
            id = 'scatter_plot',
            figure = fig
            )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0px 0px 0px 5px'}
    ),

    html.Div([
        

    dcc.Graph(
            id='pie_chart',
            figure = create_pie(3.)
        )

    ], style= dict( width= '25%', 
                    display= 'inline-block',
                    padding = '0px 0px 0px 5px' )
    ),


    html.Div([
        
        dcc.Graph(
            id='bar_masses',
            figure = create_mass_plot(3.)
        )
    ], style={'width': '25%', 'display': 'inline-block', 'padding': '0px 5px 0px 0px'}
    ),

   
    html.Div([
        html.Div([
            html.H3(['Density contours for N-Body decay channels'],style={'color': 'white', 'textAlign': 'left',
                                                             'fontFamily': 'Times New Roman'}),
            html.Div([
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': '2 Body decay', 'value': 2},
                        {'label': '3 Body decay', 'value': 3},
                        {'label': '4 Body decay', 'value': 4}
                    ],
                    placeholder="Select a N-body channel",
                    value=2,
                    style = dict(
                                #backgroundColor = 'rgb(27, 79, 114)', 
                                width = "80%",
                                fontFamily = 'Times New Roman',     
                                textAlign = 'center',
                                fontSize = '18px'
                                #color = 'black',
                                #padding = '0px 103px 0px 0px'
                            )
            )], style= dict(alignItems = 'center',
                            padding = '0px 0px 0px 5px',
                            backgroundColor = '#111111')),
            dcc.Graph(
                id='contour-plot',
                figure = create_contour(2)
            
        )], style={'width': '48.65%', 'display': 'inline-block', 'padding': '0px 0px 20px 5px', 'alignItems': 'center',
                    'justifyContent': 'center', 'backgroundColor' : '#111111'}),

        html.Div([],style=dict(width = '0.8%', display = 'inline-block')),
        
        html.Div([
        html.H6(['Branching ratios data frame'], style=dict(color='white', textAlign= 'left', fontFamily= 'Times New Roman')),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in display_data(259).columns],
            data=display_data(259).to_dict('records'),

            #style_as_list_view=True,
            style_header=dict(  backgroundColor= my_colors[0], border= '1px solid #34495E' ),
            style_cell=dict(    backgroundColor= 'rgb(30,30,30 )', color= 'white'),
            style_data=dict(    border= '1px solid #1B4F72' )
        )
        ], style=dict(  width= '16%', display= 'inline-block',backgroundColor = '#111111', 
                        padding = '10px 10px 10px 10px')),
                        
        html.Div([
            html.H6(['Particles IDs'], style=dict(color='white', textAlign= 'left', fontFamily= 'Times New Roman')),
            html.Div([
                html.Img(src=app.get_asset_url('pdg.png'),width="450", height="300")
            
            ], style= dict(width= '0.5%'))
        ], style=dict(  display= 'inline-block',backgroundColor = '#111111', padding = '10px 10px 10px 10px'))
    ], style=dict(display= 'flex'))
])


"""
#############
# Callbacks #
#############
"""

@app.callback(
    Output(component_id='bar_masses',component_property='figure'),
    Input(component_id='scatter_plot',component_property='hoverData')
)
def update_bars(hoverData):
    if hoverData == None:
        return  create_mass_plot(3)
    else:
        customdata = hoverData['points'][0]['customdata']        
        index = customdata[0]
        bar_plot = create_mass_plot(index) 
        return  bar_plot


@app.callback(
    Output(component_id='pie_chart',component_property='figure'),
    Input(component_id='scatter_plot',component_property='hoverData')
)
def update_pie(hoverData):
    if hoverData == None:
        return  create_pie(3)
    else:
        customdata = hoverData['points'][0]['customdata']        
        index = customdata[0]
        pie_chart = create_pie(index) 
        return  pie_chart

@app.callback(
    Output(component_id='contour-plot', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')])
def update_contour(value):
    return create_contour(value)

@app.callback(
    Output(component_id='table', component_property='data'),
    Input(component_id='scatter_plot',component_property='hoverData'))
def update_table(hoverData):
    if hoverData == None:
        return  display_data(3).to_dict('records')
    else:
        customdata = hoverData['points'][0]['customdata']        
        index = customdata[0]
        data = display_data(index).to_dict('records')
        return  data

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = True)  
