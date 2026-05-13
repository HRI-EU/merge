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

from pathlib import Path
import shutil
import subprocess
import cv2

SRC_DIR = Path("/hri/storage/rawvideo/Smile/ocad/GROUND-eval")
TRG_DIR = Path("data")

BLUR_FACES = True
FPS = 30

BOX_W = 150
BOX_H = 150
MARGIN_X = 20
MARGIN_Y = 17


def blur_fixed_bottom_right(img_path: Path):
    img = cv2.imread(str(img_path))
    if img is None:
        raise RuntimeError(f"Could not read image: {img_path}")

    h, w = img.shape[:2]

    x1 = max(0, w - BOX_W - MARGIN_X)
    y1 = max(0, h - BOX_H - MARGIN_Y)
    x2 = min(w, w - MARGIN_X)
    y2 = min(h, h - MARGIN_Y)

    if x2 <= x1 or y2 <= y1:
        print(f"Skipping invalid blur box for {img_path}")
        return

    roi = img[y1:y2, x1:x2]

    # use black box for debugging:
    # img[y1:y2, x1:x2] = 0

    blurred = cv2.GaussianBlur(roi, (151, 151), 80)
    img[y1:y2, x1:x2] = blurred

    ok = cv2.imwrite(str(img_path), img)
    if not ok:
        raise RuntimeError(f"Could not write image: {img_path}")


def process_image(img_path: Path):
    tmp_path = img_path.with_name(img_path.stem + ".blurred" + img_path.suffix)

    if BLUR_FACES:
        subprocess.run(
            [
                "deface",
                str(img_path),
                "--output",
                str(tmp_path),
                "--mask-scale",
                "1.1",
                "--thresh",
                "0.5",
            ],
            check=True,
        )
        shutil.move(tmp_path, img_path)

    blur_fixed_bottom_right(img_path)


def main():
    TRG_DIR.mkdir(parents=True, exist_ok=True)

    for src_scene in sorted(SRC_DIR.glob("scene_*")):
        if not src_scene.is_dir():
            continue

        folder_name = src_scene.name
        trg_scene = TRG_DIR / folder_name

        print(f"=== Processing: {folder_name}")

        trg_scene.mkdir(parents=True, exist_ok=True)

        for subfolder in ["images", "object_images", "person_images"]:
            src_sub = src_scene / subfolder
            trg_sub = trg_scene / subfolder

            if trg_sub.exists():
                shutil.rmtree(trg_sub)

            if src_sub.exists():
                shutil.copytree(src_sub, trg_sub)

        for img_path in sorted(trg_scene.rglob("*")):
            if img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                print(f"Editing {img_path}")
                process_image(img_path)

        print(f"=== Done: {folder_name}\n")

    print("=== Creating combined video from all images folders")

    list_file = TRG_DIR / "merge_eval.txt"
    video_out = TRG_DIR / "merge_eval.mp4"

    image_files = sorted(
        p for p in TRG_DIR.glob("*/images/*")
        if p.suffix.lower() in [".jpg", ".jpeg", ".png"]
    )

    with open(list_file, "w") as f:
        for img in image_files:
            f.write(f"file '{img.resolve()}'\n")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-r",
            str(FPS),
            "-i",
            str(list_file),
            "-vf",
            "format=yuv420p",
            str(video_out),
        ],
        check=True,
    )

    print(f"=== Video created: {video_out}")


if __name__ == "__main__":
    main()