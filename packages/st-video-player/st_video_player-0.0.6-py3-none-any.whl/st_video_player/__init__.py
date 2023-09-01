import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_video_player",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_video_player", path=build_dir)


def st_video_player(videoBytes, height, key=None):
    component_value = _component_func(videoBytes=videoBytes, height=height, key=key, default=0)
    
    return component_value
