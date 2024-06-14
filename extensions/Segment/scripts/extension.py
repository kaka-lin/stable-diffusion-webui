import os, sys
from pathlib import Path

import gradio as gr

from modules import shared, paths, script_callbacks


def on_ui_tabs():
    sys.path.extend([paths.script_path+'/extensions/Segment'])
    repo_dir = paths.script_path+'/extensions/Segment/'

    from seg_app import sam_demo

    sam_image = sam_demo()

    #  (gradio_component, title, elem_id)
    return [(sam_image, "Segment", "Segment")]


script_callbacks.on_ui_tabs(on_ui_tabs)
