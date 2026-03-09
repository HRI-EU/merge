#!/usr/bin/env python
#
#  BSD 3-Clause License
#
#  Copyright (c) 2025, Honda Research Institute Europe GmbH
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#
#
# -*- coding: utf-8 -*-

from __future__ import annotations
import base64
from io import BytesIO
import re
from typing import List, Optional, Tuple

import numpy
import cv2
from PIL import Image


def get_image_type(image) -> str:
    if isinstance(image, str):
        base64.b64decode(image.encode("utf-8"), validate=True)
        return "string"
    if isinstance(image, numpy.ndarray):
        return "cv2"
    if isinstance(image, Image.Image):
        return "pillow"
    return "unknown"


def convert_image(image, target_type: str):
    current_type = get_image_type(image)

    if current_type == "unknown":
        raise ValueError("Unsupported input image type.")
    if current_type == target_type:
        return image
    if current_type == "string":
        image_cv = image_str_to_cv(image)
    elif current_type == "cv2":
        image_cv = image
    elif current_type == "pillow":
        image_cv = image_pil_to_cv
    else:
        raise ValueError("Unsupported input image type.")

    # Step 2: Convert the PIL image to the target format
    if target_type == "string":
        return image_cv_to_str(image_cv)
    elif target_type == "cv2":
        return image_cv
    elif target_type == "pillow":
        return image_cv_to_pil(image_cv)

    else:
        raise ValueError(f"Unsupported target image type: {target_type}")


def image_pil_to_cv(image_pil: Image.Image) -> numpy.ndarray:
    image_np = numpy.array(image_pil)
    if image_np.ndim == 3:  # Check if it's a color image
        return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    else:
        return image_np


def image_str_to_cv(image_str: str) -> numpy.ndarray:
    image_bytes = base64.b64decode(image_str)
    np_array = numpy.frombuffer(image_bytes, dtype=numpy.uint8)
    image_cv = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image_cv


def image_file_to_str(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return image_bytes_to_str(image_file.read())


def image_bytes_to_str(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def image_cv_to_pil(image_cv: numpy.ndarray) -> Image.Image:
    if not isinstance(image_cv, numpy.ndarray):
        raise ValueError("Input must be a NumPy array (OpenCV image).")
    image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)


def image_cv_to_str(image_cv: numpy.ndarray, extension: str = ".jpg") -> str:
    return image_bytes_to_str(cv2.imencode(extension, image_cv)[1].tobytes())


def read_image_as_str(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return image_bytes_to_str(image_file.read())


def read_image_as_cv(image_path: str) -> numpy.ndarray:
    return cv2.imread(image_path)


def save_image_as_cv(image: numpy.ndarray, image_path: str) -> None:
    if not isinstance(image, numpy.ndarray):
        raise ValueError("The image must be a NumPy array.")
    cv2.imwrite(image_path, image)


def images_cv_to_mp4(images, output_path, fps=1):
    """
    images: list of np.ndarray (BGR format, same width/height)
    output_path: e.g. "output.mp4"
    fps: frames per second
    """
    if len(images) == 0:
        raise ValueError("No images provided")

    # Ensure all images have same size
    height, width = images[0].shape[:2]

    for img in images:
        if img.shape[:2] != (height, width):
            raise ValueError("All images must have the same size")

    # MP4 codec
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for img in images:
        video.write(img)

    video.release()


def show_image_cv(
    image: numpy.ndarray,
    wait_key: int = 1,
    destroy_all_windows: bool = True,
    window_name: str = "Image",
) -> None:
    if not isinstance(image, numpy.ndarray):
        raise ValueError("The image must be a NumPy array.")
    cv2.imshow(window_name, image)
    if wait_key > -1:
        key = cv2.waitKey(wait_key) & 0xFF
        if key == ord("q"):
            exit()
    if destroy_all_windows:
        cv2.destroyAllWindows()


def image_str_to_pil(image_str: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(image_str)))


def scale_image_cv(image_cv: numpy.ndarray, scale: float) -> numpy.ndarray:
    return cv2.resize(image_cv, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


def resize_image_cv(image_cv: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    dsize = (width, height)
    return cv2.resize(image_cv, dsize=dsize)


def scale_image_cv_max_size(image_cv: numpy.ndarray, size: int) -> numpy.ndarray:
    height, width = image_cv.shape[:2]
    if size < height >= width:
        width, height = round(size / height * width), size
    elif size < width > height:
        width, height = size, round(size / width * height)
    else:
        return image_cv

    return cv2.resize(image_cv, (width, height), interpolation=cv2.INTER_AREA)


def scale_image_cv_to_fit_size(
    image_cv: numpy.ndarray, want_width: int, want_height: int
) -> numpy.ndarray:
    have_height, have_width = image_cv.shape[:2]

    scale_factor_x = want_width / have_width
    scale_factor_y = want_height / have_height

    if scale_factor_x < scale_factor_y:
        new_width, new_height = want_width, round(scale_factor_x * have_height)
    else:
        new_width, new_height = round(scale_factor_y * have_width), want_height

    return cv2.resize(image_cv, (new_width, new_height), interpolation=cv2.INTER_AREA)


def crop_rois(image: numpy.ndarray, rois: dict = {}):
    cropped_images = {}
    for label, [left, top, right, bottom] in rois.items():
        cropped_image = image[top:bottom, left:right]
        cropped_images.update({label: cropped_image})

    return cropped_images


def wrap_text(text, font, max_width):
    """Wrap text based on maximum width."""
    lines = []
    words = text.split(" ")
    while words:
        line = ""
        while (
            words
            and cv2.getTextSize(line + words[0], font[0], font[1], font[2])[0][0]
            < max_width
        ):
            line += words.pop(0) + " "
        lines.append(line)
    return lines


def draw_rois(
    image: numpy.ndarray, rois: dict, show_labels: bool = True
) -> numpy.ndarray:
    output_image = image.copy()

    # Loop through each ROI and draw a rectangle and label
    for obj_name, bbox in rois.items():
        x_min, y_min, x_max, y_max = bbox

        # Draw a rectangle around the ROI
        cv2.rectangle(
            output_image, (x_min, y_min), (x_max, y_max), color=(0, 0, 255), thickness=2
        )

        # Add the object name as a label
        if show_labels:
            label_position = (x_min, y_min - 10 if y_min > 10 else y_min + 10)
            cv2.putText(
                output_image,
                obj_name,
                label_position,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(0, 0, 255),
                thickness=2,
            )

    return output_image


def stitch_images(
    images: List[numpy.ndarray],
    grid_size: Optional[Tuple[int, int]] = None,
    scale: float = 0.5,
    width: Optional[int] = None,
    font_size: float = 1.0,
    font_thickness=1,
    line_offset: int = 15,
    border_size: int = 0,
    pre_text: Optional[str] = None,
    post_text: Optional[str] = None,
    caption_text: Optional[List[str]] = None,
    transpose: bool = False,
    bold_thickness: int = 1,
    gap_before_pre_text: int = 10,
    gap_after_pre_text: int = 10,
    gap_between_image_and_caption: int = 20,
    gap_between_caption_and_next_row: int = 10,
    gap_before_post_text: int = 20,
    gap_after_post_text: int = 0,  # 👈 NEU
    tab_size: int = 4,
) -> Optional[numpy.ndarray]:

    def _normalize_tabs_and_split_lines(text: Optional[str]) -> List[str]:
        if not text:
            return []
        text = text.replace("\\t", "\t")
        text = text.expandtabs(tab_size)
        return text.splitlines()

    def _strip_md_bold(s: str) -> str:
        return re.sub(r"\*\*(.*?)\*\*", r"\1", s)

    def _parse_bold_segments(line: str) -> List[Tuple[str, bool]]:
        segs: List[Tuple[str, bool]] = []
        i = 0
        while i < len(line):
            if line.startswith("**", i):
                j = line.find("**", i + 2)
                if j != -1:
                    segs.append((line[i + 2 : j], True))
                    i = j + 2
                    continue
            next_md = line.find("**", i)
            if next_md == -1:
                segs.append((line[i:], False))
                break
            if next_md > i:
                segs.append((line[i:next_md], False))
            i = next_md
        return segs

    def _measure(text: str, font, thickness: int) -> int:
        (tw, _), _ = cv2.getTextSize(text, font[0], font[1], thickness)
        return tw

    def _wrap_preserve_ws(text: Optional[str], font, max_width: int) -> List[str]:
        lines = _normalize_tabs_and_split_lines(text)
        wrapped: List[str] = []
        for raw in lines:
            if raw == "":
                wrapped.append("")
                continue
            tokens = re.split(r"(\s+)", raw)
            cur = ""
            for tok in tokens:
                test = cur + tok
                test_measure = _strip_md_bold(test)
                if _measure(test_measure, font, font[2]) <= max_width or cur == "":
                    cur = test
                else:
                    wrapped.append(cur.rstrip())
                    cur = tok.lstrip() if cur.strip() == "" else tok
                    if _measure(_strip_md_bold(cur), font, font[2]) > max_width:
                        s = ""
                        for ch in cur:
                            test2 = s + ch
                            if (
                                _measure(_strip_md_bold(test2), font, font[2])
                                <= max_width
                                or s == ""
                            ):
                                s = test2
                            else:
                                wrapped.append(s.rstrip())
                                s = ch
                        cur = s
            if cur != "":
                wrapped.append(cur.rstrip())
        return wrapped

    def _draw_line_segments(
        img, x, y, line: str, font, color, normal_thickness: int, bold_thickness: int
    ) -> int:
        segs = _parse_bold_segments(line)
        cur_x = x
        for text, is_bold in segs:
            th = bold_thickness if is_bold else normal_thickness
            if text:
                cv2.putText(img, text, (cur_x, y), font[0], font[1], color, th)
                cur_x += _measure(text, font, th)
        return y + max(line_offset, 1)

    if not images:
        return None

    if grid_size:
        rows, cols = grid_size
    else:
        rows, cols = 1, len(images)

    if transpose:
        images = [images[(i % cols) * rows + i // cols] for i in range(len(images))]

    base_h, base_w = images[0].shape[:2]
    if width:
        tgt_w = int(width * scale)
        tgt_h = int(base_h * (width / base_w) * scale)
    else:
        tgt_w = int(base_w * scale)
        tgt_h = int(base_h * scale)

    font = (cv2.FONT_HERSHEY_SIMPLEX, float(font_size), font_thickness)
    normal_th = font[2]
    bold_th = max(normal_th + 2, bold_thickness)

    col_slot = tgt_w + 2 * border_size
    row_slot = tgt_h + 2 * border_size

    max_text_width = max(cols * col_slot - 20, 1)
    pre_lines = _wrap_preserve_ws(pre_text, font, max_text_width) if pre_text else []
    post_lines = _wrap_preserve_ws(post_text, font, max_text_width) if post_text else []

    cap_wrapped: List[List[str]] = []
    if caption_text:
        for t in caption_text:
            cap_wrapped.append(_wrap_preserve_ws(t, font, max(tgt_w, 1)))

    pre_text_height = len(pre_lines) * max(line_offset, 1)
    caption_heights_per_image = (
        [len(cw) * max(line_offset, 1) for cw in cap_wrapped] if caption_text else []
    )
    caption_heights_per_row = []
    for r in range(rows):
        row_caps = (
            caption_heights_per_image[r * cols : (r + 1) * cols] if caption_text else []
        )
        caption_heights_per_row.append(max(row_caps) if row_caps else 0)

    # Total height calculation
    total_height = gap_before_pre_text
    if pre_lines:
        total_height += pre_text_height + gap_after_pre_text

    for r in range(rows):
        total_height += row_slot
        if caption_heights_per_row[r] > 0:
            total_height += gap_between_image_and_caption + caption_heights_per_row[r]
        if r < rows - 1:
            total_height += gap_between_caption_and_next_row

    if post_lines:
        total_height += (
            gap_before_post_text
            + len(post_lines) * max(line_offset, 1)
            + gap_after_post_text
        )

    total_height = max(total_height, 1)

    stitched_image = (
        numpy.ones((total_height, cols * col_slot, 3), dtype=numpy.uint8) * 255
    )

    # Pre-text rendering
    y = gap_before_pre_text
    x_left = 10
    for line in pre_lines:
        y = _draw_line_segments(
            stitched_image, x_left, y, line, font, (0, 0, 0), normal_th, bold_th
        )
    if pre_lines:
        y += gap_after_pre_text

    cur_y = y
    last_caption_bottom = cur_y
    for idx, image in enumerate(images):
        if idx >= rows * cols:
            break
        r = idx // cols
        c = idx % cols

        resized = cv2.resize(image, (tgt_w, tgt_h))
        bordered = cv2.copyMakeBorder(
            resized,
            border_size,
            border_size,
            border_size,
            border_size,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        )

        y_img = cur_y
        for rr in range(r):
            y_img += row_slot
            if caption_heights_per_row[rr] > 0:
                y_img += gap_between_image_and_caption + caption_heights_per_row[rr]
            y_img += gap_between_caption_and_next_row

        x_img = c * col_slot
        stitched_image[y_img : y_img + row_slot, x_img : x_img + col_slot, :] = bordered

        cap_y = y_img + row_slot
        if caption_text and idx < len(cap_wrapped) and cap_wrapped[idx]:
            cap_y += gap_between_image_and_caption
            for line in cap_wrapped[idx]:
                cap_y = _draw_line_segments(
                    stitched_image,
                    x_img + 10,
                    cap_y,
                    line,
                    font,
                    (0, 0, 0),
                    normal_th,
                    bold_th,
                )
        last_caption_bottom = max(last_caption_bottom, cap_y)

    # Post-text rendering
    y_post = last_caption_bottom + (gap_before_post_text if post_lines else 0)
    for line in post_lines:
        y_post = _draw_line_segments(
            stitched_image, x_left, y_post, line, font, (0, 0, 0), normal_th, bold_th
        )

    # Optional: y_post_end = y_post + gap_after_post_text

    return stitched_image
