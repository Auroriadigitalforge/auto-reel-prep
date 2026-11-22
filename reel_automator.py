import csv
import datetime
from pathlib import Path
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
)

# Configuration & Paths
BASE_DIR = Path(__file__).parent if "__file__" in globals() else Path.cwd()
CSV_PATH = BASE_DIR / "topics.csv"
CLIPS_DIR = BASE_DIR / "clips"
OUTPUT_DIR = BASE_DIR / "output_reels"
OUTPUT_DIR.mkdir(exist_ok=True)

HASHTAGS = ["#indiegamedev", "#browsergame", "#gamedev", "#physics", "#unity3d"]
OPTIMAL_TIMES = {
    "Monday": "09:00",
    "Tuesday": "11:00",
    "Wednesday": "10:00",
    "Thursday": "12:00",
    "Friday": "15:00",
    "Saturday": "11:00",
    "Sunday": "10:00"
}

def get_best_upload_time() -> str:
    """Calculates optimal posting time based on the current day."""
    today = datetime.datetime.now().strftime("%A")
    return OPTIMAL_TIMES.get(today, "12:00")


def auto_make_reel(raw_video_path: Path, topic_data: dict, output_path: Path) -> Path:

    """Builds a vertical 1080x1920 Reel with full-video timelapse speed-up, voiceover, and hook overlay."""

    hook = topic_data.get("hook", "")

    topic = topic_data.get("topic", "")

    cta = topic_data.get("cta", "")

    start_sec = int(topic_data.get("start_sec", 0))



    # 1. Generate Voiceover Audio

    full_text = f"{hook}. {topic}. {cta}"

    tts = gTTS(text=full_text, lang="en")

    audio_path = output_path.parent / f"temp_{output_path.stem}.mp3"

    tts.save(str(audio_path))

    audio = AudioFileClip(str(audio_path))



    # 2. Create Hook Banner Overlay

    banner_img = Image.new("RGBA", (1080, 300), (0, 0, 0, 180))

    draw = ImageDraw.Draw(banner_img)

    font = ImageFont.load_default()

    draw.text((540, 150), hook, fill="white", font=font, anchor="mm")

    banner_path = output_path.parent / f"temp_{output_path.stem}.png"

    banner_img.save(banner_path)



    # 3. Assemble Video with Speed Scaling (Timelapse)

    clip = VideoFileClip(str(raw_video_path))

    if start_sec > 0:

        clip = clip.subclipped(start_sec)



    orig_dur = clip.duration

    if clip.duration > 25:

        target_duration = 24

        clip = clip.with_speed_scaled(final_duration=target_duration)

        print(f"[Step 2] Sped up {orig_dur:.1f}s video to {target_duration}s timelapse")



    clip = clip.without_audio()

    clip = clip.resized(height=1920)

    if clip.w > 1080:

        clip = clip.cropped(x_center=clip.w / 2, width=1080)



    banner_clip = (ImageClip(str(banner_path))

                   .with_duration(3.0)

                   .with_position(("center", 150)))



    final_video = CompositeVideoClip([clip, banner_clip]).with_audio(audio)

    final_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac", fps=30)

    # Cleanup temp assets
    audio.close()
    clip.close()
    audio_path.unlink(missing_ok=True)
    banner_path.unlink(missing_ok=True)

    return output_path

def process_pending_reels():
    """Reads topics.csv, builds pending Reels & captions, and updates status."""
    if not CSV_PATH.exists():
        print(f"[Error] missing {CSV_PATH}")
        return
        
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    fieldnames = rows[0].keys() if rows else ["topic", "hook", "cta", "video_file", "start_sec", "status"]
    processed_count = 0
    
    for row in rows:
        if row.get("status") == "pending":
            raw_filename = row.get("video_file", "")
            raw_video_path = CLIPS_DIR / raw_filename
            
            if not raw_video_path.exists():
                print(f"[Warning] Clip {raw_filename} not found. Skipping row.")
                continue
                
            output_video_path = OUTPUT_DIR / f"reel_{raw_filename}"
            caption_path = OUTPUT_DIR / f"reel_{Path(raw_filename).stem}_caption.txt"
            
            print(f"[Processing] Rendering Reel for topic: '{row.get('topic')}'...")
            auto_make_reel(raw_video_path, row, output_video_path)
            
            # Build Caption file
            best_time = get_best_upload_time()
            hook = row.get("hook", "")
            topic = row.get("topic", "")
            cta = row.get("cta", "Follow for more!")
            hashtag_str = " ".join(HASHTAGS)
            
            caption_text = (
                f"RECOMMENDED POST TIME: Today at {best_time}\n"
                f"----------------------------------------\n\n"
                f"{hook}\n\n"
                f"In this Reel: {topic}\n\n"
                f"👉 {cta}\n\n"
                f"{hashtag_str}\n"
            )
            
            with open(caption_path, mode="w", encoding="utf-8") as cf:
                cf.write(caption_text)
                
            row["status"] = "ready_to_post"
            processed_count += 1
            print(f"[Success] Created Reel and Caption at {output_video_path.name}")
            
    # Update CSV with new statuses
    if processed_count > 0:
        with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nCompleted! Processed {processed_count} topics. CSV updated.")
    else:
        print("No pending topics found in CSV.")

def evaluate_edits_metrics(views: int, viewers: int, avg_watch_time: float, duration_sec: float, shares: int, saves: int) -> dict:
    """Helper to evaluate Instagram Edits screenshot metrics."""
    recommendations = []
    if duration_sec > 0 and (avg_watch_time / duration_sec) < 0.65:
        recommendations.append("[Hook Action] Watch ratio under 65%. Tighten opening 2-3s or start directly at visual payoff.")
    if shares + saves == 0:
        recommendations.append("[CTA Action] Zero shares/saves. Swap broad tags for niche tags (#indiegamedev) and use comment-driven CTA.")
    return {
        "views": views,
        "viewers": viewers,
        "avg_watch_time": avg_watch_time,
        "shares": shares,
        "saves": saves,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    process_pending_reels()
