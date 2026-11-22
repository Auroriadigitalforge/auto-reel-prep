# Auto Reel Prep 🎬

A lightweight Python automation tool that turns raw screen recordings into ready-to-post vertical (`1080×1920`) Instagram Reels with a 3-second hook banner, text-to-speech voiceover, and a ready-to-paste caption file.

## What It Does

1. **Reads a CSV queue (`topics.csv`):** Picks every row marked `pending`.
2. **Auto-edits the video:** Scales any long raw `.mp4` recording into a 24-second vertical (`1080×1920`) timelapse using [MoviePy](https://zulko.github.io/moviepy/), adds a 3-second hook banner with [Pillow](https://pillow.readthedocs.io/), and attaches a spoken voiceover via [gTTS](https://gtts.readthedocs.io/).
3. **Preps your caption & best posting time:** Saves a matching `_caption.txt` file in `output_reels/` with today's target posting time, your hook, CTA, and niche hashtags.
4. **Tracks queue status:** Updates processed rows in `topics.csv` from `pending` to `ready_to_post` so clips aren't re-edited twice.
5. **Evaluates performance:** Includes an insights helper (`evaluate_edits_metrics`) to flag weak hooks (`avg_watch_time / duration < 65%`) or low share/save engagement.

## Quick Start

1. **Clone the repository and enter the folder:**
   ```bash
   git https://github.com/Auroriadigitalforge/auto-reel-prep.git
   cd auto-reel-prep
   ```

2. **Install dependencies:**
   ```bash
   pip install moviepy pillow gTTS
   ```

3. **Create the required folders and starter `topics.csv` automatically:**
   ```bash
   python setup_project.py
   ```

4. **Add your raw screen recording and topic:**
   * Drop your `.mp4` file inside `clips/`.
   * Add a row to `topics.csv` with `topic`, `hook`, `cta`, `video_file`, `start_sec`, and `status` set to `pending`.

5. **Run the auto-editor:**
   ```bash
   python reel_automator.py
   ```
   Your finished `.mp4` and `_caption.txt` will appear inside `output_reels/`.

## Project Structure

```text
├── clips/             # Raw screen recordings (ignored by Git)
├── output_reels/      # Finished 1080x1920 Reels & _caption.txt files (ignored by Git)
├── reel_automator.py  # Main auto-editing & caption-prep script
├── setup_project.py   # Creates clips/, output_reels/, and starter topics.csv
├── topics.csv         # Content queue
└── .gitignore         # Keeps media files and secrets out of Git
```

## Planned Improvements

* Auto-generated word-by-word subtitles
* Motion/audio-peak highlight detection instead of uniform timelapse
* Automated A/B hook tracking in a performance CSV
