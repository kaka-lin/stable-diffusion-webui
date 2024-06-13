import os, sys
import glob

import cv2
import numpy as np
import torch
from torchvision import transforms
import gradio as gr
from gradio_image_prompter import ImagePrompter
from pathlib import Path

from modules import shared, paths, script_callbacks
from modules.ui_components import ToolButton
from efficient_sam.build_efficient_sam import build_efficient_sam_vitt, build_efficient_sam_vits

try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


models = {}
# Build the EfficientSAM-Ti model.
models['efficientsam_ti'] = build_efficient_sam_vitt()


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
    saved_path = paths.script_path + "log/images/"
    os.makedirs(saved_path, exist_ok=True)

    # save image for download
    output_image = saved_path + 'output.png'
    cv2.imwrite(output_image, images)
    fullfns.append(output_image)

    return gr.File(value=fullfns, visible=True)


def run_model(prompts):
    test_image = prompts["image"]
    points_prompts = prompts["points"]

    # processing the image
    input_image = transforms.ToTensor()(test_image)

    # processing the points to point and label
    for points in points_prompts:
        
        input_points = torch.tensor([[[[points[0], points[1]], [points[3], points[4]]]]])
        input_labels = torch.tensor([[[points[2], points[5]]]])

    # Run inference for both EfficientSAM-Ti models.
    for model_name, model in models.items():
        print('Running inference using ', model_name)
        predicted_logits, predicted_iou = model(
            input_image[None, ...],
            input_points,
            input_labels,
        )
        sorted_ids = torch.argsort(predicted_iou, dim=-1, descending=True)
        predicted_iou = torch.take_along_dim(predicted_iou, sorted_ids, dim=2)
        predicted_logits = torch.take_along_dim(
            predicted_logits, sorted_ids[..., None, None], dim=2
        )

        mask = torch.ge(predicted_logits[0, 0, 0, :, :], 0).cpu().detach().numpy()
        masked_image_np = test_image.copy().astype(np.uint8) * mask[:,:,None]

    return (masked_image_np, points_prompts)


def sam_demo():
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
                        output_image = gr.Image(show_label=False, interactive=False)
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
            fn=run_model,
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
