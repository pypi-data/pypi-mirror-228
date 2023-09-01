# streamlit-custom-component

Streamlit component that allows you to do play videos from bytes

## Installation instructions

```sh
pip install pip install st-video-player
```

## Usage instructions

```python
import streamlit as st
from st_video_player import st_video_player

mp4_file_path = "./path/to/video/*.mp4"

with open(file_path, "rb") as file:
    mp4_bytes = file.read()
    st_video_player(mp4_bytes, height=600)

```