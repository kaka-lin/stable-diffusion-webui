import os, sys
import glob

import cv2
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import gradio as gr
from gradio_image_prompter import ImagePrompter
from pathlib import Path

from modules import shared, paths, script_callbacks
from modules.ui_components import ToolButton
from extensions.Segment.gadio_demo import SegmentModel

try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


def get_img_from_txt2img():
    talker_path = Path(paths.script_path) / "outputs"
    imgs_from_txt_dir = str(talker_path / "txt2img-images/")
    imgs = glob.glob(imgs_from_txt_dir+'/*/*.png')
    imgs.sort(key=lambda x:os.path.getmtime(os.path.join(imgs_from_txt_dir, x)))
    # img_from_txt_path = os.path.join(imgs_from_txt_dir, imgs[-1])
    img_from_txt_path = imgs[-1]
    return img_from_txt_path


def get_img_from_img2img():
    talker_path = Path(paths.script_path) / "outputs"
    imgs_from_img_dir = str(talker_path / "img2img-images/")
    imgs = glob.glob(imgs_from_img_dir+'/*/*.png')
    imgs.sort(key=lambda x:os.path.getmtime(os.path.join(imgs_from_img_dir, x)))
    # img_from_img_path = os.path.join(imgs_from_img_dir, imgs[-1])
    img_from_img_path = imgs[-1]
    return img_from_img_path


def save_files(images):
    fullfns = []

    # make output dir
    saved_path = paths.script_path + "/log/images/"
    os.makedirs(saved_path, exist_ok=True)

    # save image for download
    output_image = saved_path + 'output.png'
    Image.fromarray(images).save(output_image)
    fullfns.append(output_image)

    return gr.File(value=fullfns, visible=True)


def sam_demo():
    segment_model = SegmentModel()
   
    with gr.Blocks() as sam_interface:
        with gr.Row():
            with gr.Column(variant='panel'):
                with gr.Tabs("sam_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = ImagePrompter(show_label=False)
                            with gr.Row():
                                submit_image2 = gr.Button('load From txt2img', variant='primary')
                                submit_image3 = gr.Button('load From img2img', variant='primary')
                        with gr.Row():
                            prompt_button = gr.Button("Submit")

            with gr.Column(variant='panel'):
                with gr.Tabs("sam_genearted"):
                    with gr.TabItem('Result image'):
                        output_image = gr.Image(show_label=False, interactive=False, image_mode='RGBA')
                        output_points = gr.Dataframe(label="Points")

                        save_button = ToolButton('💾', elem_id=f'save_sam')
                        download_files = gr.File(None, file_count="multiple", interactive=False, show_label=False, visible=False, elem_id=f'download_files_sam')

        submit_image2.click(
            fn=get_img_from_txt2img,
            outputs=source_image)

        submit_image3.click(
            fn=get_img_from_img2img,
            outputs=source_image)

        prompt_button.click(
            fn=segment_model.run_model,
            inputs=source_image,
            outputs=[output_image, output_points])

        save_button.click(
            fn=save_files,
            inputs=[output_image],
            outputs=[download_files],
        )

    return sam_interface


if __name__ == "__main__":
    demo = sam_demo()
    demo.queue()
    demo.launch()
