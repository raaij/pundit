import os

import dash_bootstrap_components as dbc

from wdo.constant import PATH_EXPERIMENTS

files = os.listdir(PATH_EXPERIMENTS)
final_list = []
for file in files:
    if file.endswith(".json"):
        final_list.append(file.replace(".json", ""))
items = [dbc.DropdownMenuItem(i) for i in final_list]

dropdown1 = dbc.DropdownMenu(
    label="Choose Experiment",
    direction="down",
    children=items,
)
