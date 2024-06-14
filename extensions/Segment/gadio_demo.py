import numpy as np
import torch
from torchvision import transforms

from efficient_sam.build_efficient_sam import build_efficient_sam_vitt, build_efficient_sam_vits


class SegmentModel():
    def __init__(self, checkpoint_path=None):
        # TODO: load the EfficientSAM-Ti model here
        pass 
    
    def run_model(self, prompts):
        # XXX: load the model outside the fuction
        #   if the model loads outside the function 
        #   that is being called when the `gradio button` clicked
        #   would occur error:
        #     `RuntimeError: Tensor on device meta is not on the expected device cpu!`
        #
        #   But if in the extensions folder add the `SadTalker` extension, 
        #   there would not be an error.
        self.model = build_efficient_sam_vitt()

        test_image = prompts["image"]
        points_prompts = prompts["points"]

        # processing the image
        input_image = transforms.ToTensor()(test_image)

        # processing the points to point and label
        for points in points_prompts:
            input_points = torch.tensor([[[[points[0], points[1]], [points[3], points[4]]]]])
            input_labels = torch.tensor([[[points[2], points[5]]]])
       
        # Run inference for both EfficientSAM-Ti models.
        print('Running inference using ', 'EfficientSAM-Ti')
        predicted_logits, predicted_iou = self.model(
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