# """
# ****** Important! *******
# If you run this app locally, un-comment line 127 to add the theme change components to the layout
# """

# from dash import Dash, dcc, html, Input, Output, callback, Patch, clientside_callback
# import plotly.express as px
# import plotly.io as pio
# import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
# import dash_ag_grid as dag

# df = px.data.gapminder()
# years = df.year.unique()
# continents = df.continent.unique()

# # stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])


# color_mode_switch =  html.Span(
#     [
#         dbc.Label(className="fa fa-moon", html_for="switch"),
#         dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
#         dbc.Label(className="fa fa-sun", html_for="switch"),
#     ]
# )

# # The ThemeChangerAIO loads all 52  Bootstrap themed figure templates to plotly.io
# theme_controls = html.Div(
#     [ThemeChangerAIO(aio_id="theme"), color_mode_switch],
#     className="hstack gap-3 mt-2"
# )

# header = html.H4(
#     "Theme Explorer Sample App", className="bg-primary text-white p-2 mb-2 text-center"
# )

# grid = dag.AgGrid(
#     id="grid",
#     columnDefs=[{"field": i} for i in df.columns],
#     rowData=df.to_dict("records"),
#     defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
#     dashGridOptions={"rowSelection":"multiple"},
# )

# dropdown = html.Div(
#     [
#         dbc.Label("Select indicator (y-axis)"),
#         dcc.Dropdown(
#             ["gdpPercap", "lifeExp", "pop"],
#             "pop",
#             id="indicator",
#             clearable=False,
#         ),
#     ],
#     className="mb-4",
# )

# checklist = html.Div(
#     [
#         dbc.Label("Select Continents"),
#         dbc.Checklist(
#             id="continents",
#             options=continents,
#             value=continents,
#             inline=True,
#         ),
#     ],
#     className="mb-4",
# )

# slider = html.Div(
#     [
#         dbc.Label("Select Years"),
#         dcc.RangeSlider(
#             years[0],
#             years[-1],
#             5,
#             id="years",
#             marks=None,
#             tooltip={"placement": "bottom", "always_visible": True},
#             value=[years[2], years[-2]],
#             className="p-0",
#         ),
#     ],
#     className="mb-4",
# )
# theme_colors = [
#     "primary",
#     "secondary",
#     "success",
#     "warning",
#     "danger",
#     "info",
#     "light",
#     "dark",
#     "link",
# ]
# colors = html.Div(
#     [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
# )
# colors = html.Div(["Theme Colors:", colors], className="mt-2")


# controls = dbc.Card(
#     [dropdown, checklist, slider],
#     body=True,
# )

# tab1 = dbc.Tab([dcc.Graph(id="line-chart", figure=px.line(template="bootstrap"))], label="Line Chart")
# tab2 = dbc.Tab([dcc.Graph(id="scatter-chart", figure=px.scatter(template="bootstrap"))], label="Scatter Chart")
# tab3 = dbc.Tab([grid], label="Grid", className="p-4")
# tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

# app.layout = dbc.Container(
#     [
#         header,
#         dbc.Row([
#             dbc.Col([
#                 controls,
#                 # ************************************
#                 # Uncomment line below when running locally!
#                 # ************************************
#                 theme_controls,
#             ],  width=4),
#             dbc.Col([tabs, colors], width=8),
#         ]),
        
#     ],
#     fluid=True,
#     className="dbc dbc-ag-grid",
# )



# @callback(
#     Output("line-chart", "figure" ),
#     Output("scatter-chart", "figure"),
#     Output("grid", "rowData"),
#     Input("indicator", "value"),
#     Input("continents", "value"),
#     Input("years", "value"),
#     Input(ThemeChangerAIO.ids.radio("theme"), "value"),
#     Input("switch", "value"),
# )
# def update(indicator, continent, yrs, theme, color_mode_switch_on):

#     if continent == [] or indicator is None:
#         return {}, {}, []

#     theme_name = template_from_url(theme)
#     template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

#     dff = df[df.year.between(yrs[0], yrs[1])]
#     dff = dff[dff.continent.isin(continent)]

#     fig = px.line(
#         dff,
#         x="year",
#         y=indicator,
#         color="continent",
#         line_group="country",
#         template=template_name
#     )

#     fig_scatter = px.scatter(
#         dff[dff.year == yrs[0]],
#         x="gdpPercap",
#         y="lifeExp",
#         size="pop",
#         color="continent",
#         log_x=True,
#         size_max=60,
#         template=template_name,
#         title="Gapminder %s: %s theme" % (yrs[1], template_name),
#     )

#     return fig, fig_scatter, dff.to_dict("records")


# # updates the Bootstrap global light/dark color mode
# clientside_callback(
#     """
#     switchOn => {       
#        switchOn
#          ? document.documentElement.setAttribute('data-bs-theme', 'light')
#          : document.documentElement.setAttribute('data-bs-theme', 'dark')
#        return window.dash_clientside.no_update
#     }
#     """,
#     Output("switch", "id"),
#     Input("switch", "value"),
# )


# # This callback isn't necessary, but it makes updating figures with the new theme much faster
# @callback(
#     Output("line-chart", "figure", allow_duplicate=True ),
#     Output("scatter-chart", "figure", allow_duplicate=True),
#     Input(ThemeChangerAIO.ids.radio("theme"), "value"),
#     Input("switch", "value"),
#     prevent_initial_call=True
# )
# def update_template(theme, color_mode_switch_on):
#     theme_name = template_from_url(theme)
#     template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

#     patched_figure = Patch()
#     # When using Patch() to update the figure template, you must use the figure template dict
#     # from plotly.io  and not just the template name
#     patched_figure["layout"]["template"] = pio.templates[template_name]
#     return patched_figure, patched_figure

# if __name__ == "__main__":
#     app.run_server(debug=True)

# import dash
# import dash_bootstrap_components as dbc
# from dash import Input, Output, dcc, html

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# # the style arguments for the sidebar. We use position:fixed and a fixed width
# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

# # the styles for the main content position it to the right of the sidebar and
# # add some padding.
# CONTENT_STYLE = {
#     "margin-left": "18rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
# }

# sidebar = html.Div(
#     [
#         html.H2("Sidebar", className="display-4"),
#         html.Hr(),
#         html.P(
#             "A simple sidebar layout with navigation links", className="lead"
#         ),
#         dbc.Nav(
#             [
#                 dbc.NavLink("Home", href="/", active="exact"),
#                 dbc.NavLink("Page 1", href="/page-1", active="exact"),
#                 dbc.NavLink("Page 2", href="/page-2", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#     ],
#     style=SIDEBAR_STYLE,
# )

# content = html.Div(id="page-content", style=CONTENT_STYLE)

# app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == "/":
#         return html.P("This is the content of the home page!")
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return html.Div(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ],
#         className="p-3 bg-light rounded-3",
#     )


# if __name__ == "__main__":
#     app.run_server(port=8888)

# from dash import Dash, html, dcc, Input, Output, callback
# import dash_daq as daq

# app = Dash(__name__)

# app.layout = html.Div([
#     daq.Gauge(
#         id='my-gauge-1',
#         label="Default",
#         value=6
#     ),
#     dcc.Slider(
#         id='my-gauge-slider-1',
#         min=0,
#         max=10,
#         step=1,
#         value=5
#     ),
# ])

# @callback(Output('my-gauge-1', 'value'), Input('my-gauge-slider-1', 'value'))
# def update_output(value):
#     return value

# if __name__ == '__main__':
#     app.run(debug=True)
    

    
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)