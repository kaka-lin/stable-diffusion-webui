# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

from .efficient_sam import build_efficient_sam
from modules import paths

checkpoint_path = Path(paths.extensions_dir) / "Segment/weights"


def build_efficient_sam_vitt():
    return build_efficient_sam(
        encoder_patch_embed_dim=192,
        encoder_num_heads=3,
        checkpoint=str(checkpoint_path / "efficient_sam_vitt.pt"),
    ).eval()


def build_efficient_sam_vits():
    return build_efficient_sam(
        encoder_patch_embed_dim=384,
        encoder_num_heads=6,
        checkpoint=str(checkpoint_path / "efficient_sam_vits.pt"),
    ).eval()
