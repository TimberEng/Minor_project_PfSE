import streamlit as st
import plotly.graph_objects as go
import app_module as appmo
from plotly import graph_objects as go
import plotly.express as px


st.markdown('# Structural Analysis Project')
st.markdown('## Project details as below:')


st.sidebar.subheader("Parameter Inputs")
Column_height = st.sidebar.number_input("Column height (mm)", value=3500, step= 100)
pressure = st.sidebar.number_input("Uniformly distributed wind pressure, Wp (kPa)", value=3.0, step= 1.0)
Angle = st.sidebar.number_input("Roof angle (deg)", value=10.0, step= 1.0)
Length = st.sidebar.number_input("Frame spacing (mm)", value=10000.0, step= 100.0)






frame_model = appmo.build_frame(Column_height,Length, pressure, Angle)


edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4]
]

Frame_fig = go.Figure()
for i_node, j_node in edges:
    x_coord_i = appmo.get_nodes(frame_model)[0][i_node]
    y_coord_i = appmo.get_nodes(frame_model)[1][i_node]
    x_coord_j = appmo.get_nodes(frame_model)[0][j_node]
    y_coord_j = appmo.get_nodes(frame_model)[1][j_node]
    trace = go.Scatter(
        x = [x_coord_i, x_coord_j],
        y = [y_coord_i, y_coord_j],
        line = {
            'color':'rgb(255,0,0)',
            'width':5
        },
        marker={
            'size': 10
        },
        showlegend = False
    )
    Frame_fig.add_trace(trace)
Frame_fig.layout.height=600
Frame_fig.layout.width=800
Frame_fig.update_layout(annotations = [x = 0.5,
                                       y = -0.1
                                       ])
Frame_fig



max_moment = appmo.find_max_moment(frame_model)
max_shear= appmo.find_max_shear(frame_model)
max_vertical = appmo.find_max_vertical(frame_model)
max_horizontal= appmo.find_max_horizontal(frame_model)





tab1, tab2, tab3, tab4, tab5 = st.tabs(['Calculation','Shear', 'Bending','Vertical','Horizontal'])
with tab1:
    st.write(f"Max bending moment: {round(max_moment,2)} kNm")
    st.write(f"Max shear force: {round(max_shear, 2)} kN")
    st.write(f"Max vertical displacement: {round(max_vertical,2)} mm")
    st.write(f"Max horizontal displacement: {round(max_horizontal,2)} mm")

with tab2:
    Shear_fig = go.Figure()
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][0][0],
                                   y = appmo.get_list(frame_model)[0][0][1],
                                   name="Member 1",
                                   line=dict(color = "firebrick", width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][1][0],
                                   y = appmo.get_list(frame_model)[0][1][1],
                                   name="Member 2",
                                   line=dict(width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][2][0],
                                   y = appmo.get_list(frame_model)[0][2][1],
                                   name="Member 3",
                                   line=dict(width = 4)))
    Shear_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[0][3][0],
                                   y = appmo.get_list(frame_model)[0][3][1],
                                   name="Member 4",
                                   line=dict(width = 4)))
    Shear_fig   

with tab3:
    Moment_fig = go.Figure()
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][0][0],
                                    y = appmo.get_list(frame_model)[1][0][1],
                                    name="Member 1"))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][1][0],
                                    y = appmo.get_list(frame_model)[1][1][1],
                                    name="Member 2"))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][2][0],
                                    y = appmo.get_list(frame_model)[1][2][1],
                                    name="Member 3"))
    Moment_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[1][3][0],
                                    y = appmo.get_list(frame_model)[1][3][1],
                                    name="Member 4"))
    Moment_fig

with tab4:
    Vertical_dis_fig = go.Figure()
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][0][0],
                                          y = appmo.get_list(frame_model)[2][0][1],
                                          name="Memnber 1"))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][1][0],
                                          y = appmo.get_list(frame_model)[2][1][1],
                                          name="Memnber 2"))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][2][0],
                                          y = appmo.get_list(frame_model)[2][2][1],
                                          name="Memnber 3"))
    Vertical_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[2][3][0],
                                          y = appmo.get_list(frame_model)[2][3][1],
                                          name="Memnber 4"))
    Vertical_dis_fig

with tab5:
    Horizontal_dis_fig = go.Figure()
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][0][0],
                                            y = appmo.get_list(frame_model)[3][0][1],
                                            name="Member 1"))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][1][0],
                                            y = appmo.get_list(frame_model)[3][1][1],
                                            name="Member 2"))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][2][0],
                                            y = appmo.get_list(frame_model)[3][2][1],
                                            name="Member 3"))
    Horizontal_dis_fig.add_trace(go.Scatter(x = appmo.get_list(frame_model)[3][3][0],
                                            y = appmo.get_list(frame_model)[3][3][1],
                                            name="Member 4"))
    Horizontal_dis_fig