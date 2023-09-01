import os

import streamlit as st  
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _table_update_create_scenario = components.declare_component(
        "table_update_create_scenario",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _table_update_create_scenario = components.declare_component("table_update_create_scenario", path=build_dir)


def table_update_create_scenario(key=None,data=None,shape=None ,scenarios=None,package_list=None ,active_scenario=None):
    return _table_update_create_scenario(key=key, data=data ,shape=shape,scenarios=scenarios,package_list=package_list,active_scenario=active_scenario)



# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    shape = {
        "no_rows": 5,
        "no_cols": 5,
        "width": "100%",
        "height": "350px"
    }
    package_list={'ssd_cans_7.5z_10pk_3ct': ['optimization1', 'optimization2', 'optimization3'], 'ssd_cans_7.5z_6pk_4ct': ['optimization1', 'optimization2', 'optimization3'], 'ssd_cans_core_12z_12pk_2ct': ['optimization1'], 'ssd_nr_.5l_6pk_4ct': ['optimization1', 'optimization2', 'optimization3']}
    data ={'Period': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20', 'P21', 'P22', 'P23', 'P24', 'P25', 'P26', 'P27', 'P28', 'P29', 'P30', 'P31', 'P32', 'P33', 'P34', 'P35', 'P36', 'P37', 'P38', 'P39', 'P40', 'P41', 'P42', 'P43', 'P44', 'P45', 'P46', 'P47', 'P48', 'P49', 'P50', 'P51', 'P52'], 'ssd_cans_7.5z_10pk_3ct': ['edv', 'edv', 'p1', 'p1', 'p1', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv', 'edv', 'edv', 'edv', 'edv', 'p1', 'edv', 'edv'], 'ssd_cans_7.5z_6pk_4ct': ['EDV', 'P2', 'P1', 'P1', 'P1', 'P1', 'P2', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P2', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P2', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P2', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P1', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P1', 'EDV', 'EDV', 'P1', 'EDV', 'EDV', 'P1', 'P1', 'EDV', 'EDV', 'P1'], 'ssd_cans_core_12z_12pk_2ct': ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1', 'P1', 'P2', 'P1'], 'ssd_nr_.5l_6pk_4ct': ['P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2', 'P2']}
    active_scenario = {'ssd_cans_7.5z_10pk_3ct': 'optimization1', 'ssd_cans_7.5z_6pk_4ct':  'optimization3', 'ssd_cans_core_12z_12pk_2ct': 'optimization1', 'ssd_nr_.5l_6pk_4ct': 'optimization3'}
    df = table_update_create_scenario(key=2,data=data,shape= shape,package_list=package_list ,active_scenario=active_scenario)
    st.write(df)
   