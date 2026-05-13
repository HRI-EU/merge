import subprocess

top_left_video = "/hri/storage/rawvideo/Smile/ICRA_2026/1P0R-st.mkv"
top_right_video = "/hri/storage/rawvideo/Smile/ICRA_2026/1P1R-st.mkv"
bot_left_video = "/hri/storage/rawvideo/Smile/ICRA_2026/2P0R-st.mkv"
bot_right_video = "/hri/storage/rawvideo/Smile/ICRA_2026/2P1R-st.mkv"

output_video = "output.mp4"

width = 1024
height = 768

cmd = [
    "ffmpeg",
    "-i", top_left_video,
    "-i", top_right_video,
    "-i", bot_left_video,
    "-i", bot_right_video,
    "-filter_complex",
    (
        f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[tl];"

        f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[tr];"

        f"[2:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[bl];"

        f"[3:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[br];"

        f"[tl][tr]hstack=inputs=2[top];"
        f"[bl][br]hstack=inputs=2[bottom];"
        f"[top][bottom]vstack=inputs=2[v]"
    ),
    "-map", "[v]",
    "-map", "0:a?",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "medium",
    "-c:a", "aac",
    "-shortest",
    output_video,
]

subprocess.run(cmd)