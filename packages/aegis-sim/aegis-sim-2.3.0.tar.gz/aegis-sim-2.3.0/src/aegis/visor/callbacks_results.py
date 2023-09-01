from dash import html, dcc, callback, Output, Input, State, ALL, MATCH, ctx
import datetime

from aegis.visor import funcs
from aegis.help.container import Container
import subprocess

SELECTION = set()


@callback(
    Output({"type": "delete-simulation-button", "index": MATCH}, "children"),
    Input({"type": "delete-simulation-button", "index": MATCH}, "n_clicks"),
    State({"type": "delete-simulation-button", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
@funcs.print_function_name
def delete_simulation(_, filename):
    config_path = funcs.get_config_path(filename)
    sim_path = config_path.parent / filename

    if filename in SELECTION:
        SELECTION.remove(filename)

    subprocess.run(["rm", "-r", sim_path], check=True)
    subprocess.run(["rm", config_path], check=True)
    return "deleting"


# @callback(
#     Output("result-section", "children", allow_duplicate=True),
#     [Input("testo", "n_clicks")],
#     [State("result-section", "children")],
#     prevent_initial_call=True,
# )
# def test(_, children):
#     # children += html.P("asdf")
#     children.append(html.P("asdfjkwerj"))
#     return children


@callback(
    Output("result-section", "children"),
    Input("result-view-button", "n_clicks"),
    Input({"type": "delete-simulation-button", "index": ALL}, "children"),
    prevent_initial_call=True,
)
@funcs.print_function_name
def refresh_result_section(*_):
    paths = funcs.get_sim_paths()
    containers = [Container(path) for path in paths]
    table_elements = [
        # html.Button(id="testo", children="testo"),
        html.Tr(
            [
                html.Th(
                    "ID", style={"padding-left": "1.3rem", "padding-right": "0.8rem"}
                ),
                html.Th("DISPLAY"),
                html.Th("CREATED"),
                # html.Th("edited"),
                html.Th("FINISHED"),
                html.Th("EXTINCT"),
                html.Th("ETA"),
                # html.Th("stage"),
                # html.Th("STAGE PER MINUTE"),
                html.Th("FILEPATH"),
                html.Th("DELETE", style={"padding-right": "1rem"}),
            ],
        ),
    ]

    for container in containers:
        if len(container.get_log()) > 0:
            logline = container.get_log().iloc[-1].to_dict()
        else:
            logline = {"ETA": None, "stage": None, "stg/min": None}
        input_summary = container.get_input_summary()
        output_summary = container.get_output_summary()

        if output_summary is None:
            status = ["not finished", "not extinct"]
        elif output_summary["extinct"]:
            status = ["finished", "extinct"]
        else:
            status = ["finished", "not extinct"]

        time_of_creation = (
            datetime.datetime.fromtimestamp(input_summary["time_start"]).strftime('%Y-%m-%d %H:%M')
            if input_summary
            else None
        )

        time_of_finishing = (
            datetime.datetime.fromtimestamp(input_summary["time_start"]).strftime('%Y-%m-%d %H:%M')
            if output_summary
            else None

        )
        # time_of_edit = datetime.datetime.fromtimestamp(
        #     container.paths["log"].stat().st_mtime
        # )

        element = html.Tr(
            children=[
                html.Td(
                    container.basepath.stem,
                    style={"padding-left": "1.3rem", "padding-right": "0.8rem"},
                ),
                html.Td(
                    children=[
                        html.Button(
                            children="display",
                            id={
                                "type": "result-checklist",
                                "index": container.basepath.stem,
                            },
                            className="checklist"
                            if container.basepath.stem not in SELECTION
                            else "checklist checked",
                            # id={
                            #     "type": "result-checklist",
                            #     "index": container.basepath.stem,
                            # },
                            # options=[{"label": "", "value": "y"}],
                            # value=["y"] if container.basepath.stem in SELECTION else [],
                        ),
                        # dcc.Checklist(
                        #     id={
                        #         "type": "result-checklist",
                        #         "index": container.basepath.stem,
                        #     },
                        #     options=[{"label": "", "value": "y"}],
                        #     value=["y"] if container.basepath.stem in SELECTION else [],
                        # ),
                    ]
                ),
                html.Td(html.P(time_of_creation)),
                # date created
                # html.Td(html.P(time_of_edit)),
                html.Td(html.P(time_of_finishing)),
                html.Td(html.P(status[1])),
                html.Td(html.P(logline["ETA"] if time_of_finishing is None else "       ")),
                # html.Td(html.P(logline["stage"])),
                # html.Td(html.P(logline["stg/min"])),
                html.Td(html.P(str(container.basepath))),
                html.Td(
                    html.Button(
                        "delete",
                        id={
                            "type": "delete-simulation-button",
                            "index": container.basepath.stem,
                        },
                        value=container.basepath.stem,
                    ),
                    style={"padding-right": "1rem"},
                ),
            ],
        )
        table_elements.append(element)

    return html.Table(children=table_elements, className="result-table")


@callback(
    Output({"type": "result-checklist", "index": MATCH}, "className"),
    Input({"type": "result-checklist", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def update_selection(n_clicks):
    sim = ctx.triggered_id["index"]
    if sim not in SELECTION:
        SELECTION.add(sim)
        return "checked checklist"
    else:
        SELECTION.remove(sim)
        return "checklist"
