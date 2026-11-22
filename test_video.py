
from pathlib import Path
from moviepy.editor import VideoFileClip

video_path = Path("clips/test_clip_01.mp4")

if not video_path.exists():
    print("ERROR: Test video not found!")
else:
    try:
        clip = VideoFileClip(str(video_path))

        print("\nVIDEO INFORMATION")
        print("-------------------------")
        print("Filename:", video_path.name)
        print("Duration:", round(clip.duration, 2), "seconds")
        print("Resolution:", clip.size)
        print("FPS:", clip.fps)
        print("Audio:", clip.audio is not None)

        clip.close()

        print("\nSUCCESS: Video loaded correctly!")

    except Exception as error:
        print("VIDEO ERROR:", error)
