import cv2
import numpy as np
import torch
from torchvision import transforms

from efficient_sam.build_efficient_sam import build_efficient_sam_vitt, build_efficient_sam_vits


class SegmentModel():
    def __init__(self, checkpoint_path=None):
        # TODO: load the EfficientSAM-Ti model here
        pass 

    def process_points(self, points_prompts):
        # input_points: [batch_size, num_queries, max_num_pts, 2], 2: x, y
        # input_labels: [batch_size, num_queries, max_num_pts], 1: point, 2: box topleft, 3: box bottomright, 4: None
        input_points = []
        input_labels = []
        # processing the points to point and label
        for points in points_prompts:
            if points[2] == 1.0:
                input_points.append([points[0], points[1]])
                input_labels.extend([points[2]])
            elif points[2] == 2.0 and points[5] == 3.0:
                input_points.append([points[0], points[1]])
                input_points.append([points[3], points[4]])
                input_labels.extend([points[2], points[5]])
        
        input_points = torch.reshape(torch.FloatTensor(input_points), [1, 1, -1, 2])
        input_labels = torch.reshape(torch.FloatTensor(input_labels), [1, 1, -1])

        return input_points, input_labels
    
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

        # processing the `points_prompts` to point and label
        input_points, input_labels = self.process_points(points_prompts)

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
        # masked_image_np = test_image.copy().astype(np.uint8) * mask[:,:,None]

        # Generate a image matting with the mask
        # make image that has alpha channel (background transparent)
        #
        # 1. Create an Alpha channel
        alpha_channel = np.zeros_like(mask, dtype=np.uint8)
        # 2. Set the foreground part in the mask to 255 (completely opaque)
        alpha_channel[mask] = 255
        # 3. Convert the original image to 4 channels (RGBA)
        rgba_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2RGBA)
        # 4. Add the Alpha channel to the image
        rgba_image[:, :, 3] = alpha_channel

        return (rgba_image, points_prompts)