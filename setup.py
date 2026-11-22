import csv
from pathlib import Path


def setup_project() -> None:
    """Create required folders and a starter topics.csv if missing."""
    base_dir = Path(__file__).parent

    required_folders = ["clips", "output_reels"]
    for folder_name in required_folders:
        folder_path = base_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Folder ready: {folder_path}")

    topics_csv = base_dir / "topics.csv"
    if not topics_csv.exists():
        headers = ["topic", "hook", "cta", "video_file", "start_sec", "status"]
        sample_row = [
            "Real-Time Snow Physics in Hearthplow",
            "Watch this snowplow breach a massive berm!",
            "Comment LINK to play in your browser",
            "sample_clip.mp4",
            "0",
            "pending",
        ]
        with open(topics_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(sample_row)
        print(f"[OK] Created starter file: {topics_csv}")
    else:
        print(f"[SKIP] {topics_csv.name} already exists (not overwritten).")

    print("\nSetup complete! Next steps:")
    print("1. Put your raw .mp4 screen recording inside clips/")
    print("2. Update topics.csv with your video filename and hook")
    print("3. Run: python reel_automator.py")


if __name__ == "__main__":
    setup_project()