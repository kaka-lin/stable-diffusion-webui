import launch
from modules import paths

# install the requirement module 
if not launch.is_installed("gradio_image_prompter"):
    component_path = f"{paths.script_path}/gradio_components/gradio-image-prompter"
    component_frontend_path = component_path + "/frontend"

    # launch.run_pip("install gradio_image_prompter", "requirements for Segment extension")
    print("Installing requirements for Segment extension")
    launch.run(f'cd {component_frontend_path} && npm install', live=True)
    launch.run(f'cd {component_path} && npm install', live=True)
    launch.run(f'cd {component_path} && gradio cc install', live=True)
