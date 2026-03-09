#!/usr/bin/env bash
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

set -euo pipefail
shopt -s nullglob

SRC_DIR="/hri/storage/rawvideo/Smile/ocad/GROUND-eval"
TRG_DIR="data/"

BLACKLIST=(
  "scene_007_PsortO"
  "scene_008_PsortO"
)

for src_path in "$SRC_DIR"/scene_*; do
  [[ -d "$src_path" ]] || continue
  folder_name="$(basename "$src_path")"

  echo "=== Processing: $folder_name"

  # ---- Check blacklist ----
  skip=false
  for blocked in "${BLACKLIST[@]}"; do
    if [[ "$folder_name" == "$blocked" ]]; then
      skip=true
      break
    fi
  done

  if $skip; then
    echo "Skipping (blacklisted): $folder_name"
    continue
  fi

  echo "Processing: $folder_name"

  rm -rf "$TRG_DIR"/"$folder_name"/"images"
  cp -r "$SRC_DIR"/"$folder_name"/"images" "$TRG_DIR"/"$folder_name"
  rm -rf "$TRG_DIR"/"$folder_name"/"object_images"
  cp -r "$SRC_DIR"/"$folder_name"/"object_images" "$TRG_DIR"/"$folder_name"
  rm -rf "$TRG_DIR"/"$folder_name"/"person_images"
  cp -r "$SRC_DIR"/"$folder_name"/"person_images" "$TRG_DIR"/"$folder_name"
  echo "=== Done: $folder_name"
  echo
done
