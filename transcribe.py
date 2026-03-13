#!/usr/bin/env python3
"""
Twin Portals Podcast - Download & Transcription Pipeline
Downloads each episode, transcribes with faster-whisper, saves as markdown.
Processes one episode at a time to conserve disk space.
"""

import json
import os
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

# Add ffmpeg to PATH
FFMPEG_DIR = r"C:\Users\valer\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")

from faster_whisper import WhisperModel

BASE_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
EPISODES_FILE = BASE_DIR / "episodes.json"
PROGRESS_FILE = BASE_DIR / "progress.json"
TEMP_AUDIO = BASE_DIR / "temp_audio.mp3"

TRANSCRIPTS_DIR.mkdir(exist_ok=True)


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def download_episode(url, dest):
    """Download an episode MP3 using urllib."""
    print(f"  Downloading...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            with open(dest, "wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        print(f"\r  Downloaded: {downloaded/(1024*1024):.1f}MB / {total/(1024*1024):.1f}MB ({pct:.0f}%)", end="", flush=True)
            print()
        return True
    except Exception as e:
        print(f"  Download failed: {e}")
        return False


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def transcribe_episode(audio_path, model):
    """Transcribe an audio file and return formatted text with timestamps."""
    print(f"  Transcribing...")
    start_time = time.time()

    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        language="en",
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    lines = []
    full_text_parts = []

    for segment in segments:
        ts = format_timestamp(segment.start)
        text = segment.text.strip()
        if text:
            lines.append(f"**[{ts}]** {text}")
            full_text_parts.append(text)

    elapsed = time.time() - start_time
    duration_str = format_timestamp(info.duration)
    print(f"  Transcription complete in {elapsed:.0f}s (audio duration: {duration_str})")

    return lines, full_text_parts, info.duration


def save_transcript(episode, lines, full_text_parts, duration):
    """Save transcript as a markdown file."""
    season = episode["season"]
    ep_num = episode["episode"]
    title = episode["title"]
    date = episode["date"]
    overall_num = episode["num"]

    filename = f"S{season:02d}E{ep_num:02d} - {title}.md"
    # Sanitize filename
    filename = filename.replace("/", "-").replace("\\", "-").replace(":", "-").replace("?", "").replace("!", "").replace('"', "'")

    filepath = TRANSCRIPTS_DIR / filename

    duration_str = format_timestamp(duration)

    content = f"""# Twin Portals - {title}

**Season {season}, Episode {ep_num}** (Overall #{overall_num})
**Air Date:** {date}
**Duration:** {duration_str}

---

## Transcript

{chr(10).join(lines)}

---

*Transcribed using faster-whisper (base model). Auto-generated transcript may contain errors.*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Saved: {filename}")
    return filepath


def main():
    # Load episodes
    with open(EPISODES_FILE) as f:
        episodes = json.load(f)

    # Load progress
    progress = load_progress()
    completed = set(progress["completed"])

    remaining = [ep for ep in episodes if ep["num"] not in completed]
    print(f"Twin Portals Transcription Pipeline")
    print(f"Total episodes: {len(episodes)}")
    print(f"Already completed: {len(completed)}")
    print(f"Remaining: {len(remaining)}")
    print()

    if not remaining:
        print("All episodes have been transcribed!")
        return

    # Load model (downloads on first run)
    print("Loading Whisper model (base)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Model loaded.")
    print()

    for i, episode in enumerate(remaining):
        num = episode["num"]
        title = episode["title"]
        print(f"[{i+1}/{len(remaining)}] Episode #{num}: {title}")

        # Download
        success = download_episode(episode["url"], TEMP_AUDIO)
        if not success:
            print(f"  SKIPPING - download failed")
            continue

        # Transcribe
        try:
            lines, full_text, duration = transcribe_episode(TEMP_AUDIO, model)
        except Exception as e:
            print(f"  SKIPPING - transcription failed: {e}")
            if TEMP_AUDIO.exists():
                TEMP_AUDIO.unlink()
            continue

        # Save
        save_transcript(episode, lines, full_text, duration)

        # Clean up audio
        if TEMP_AUDIO.exists():
            TEMP_AUDIO.unlink()

        # Update progress
        completed.add(num)
        progress["completed"] = sorted(list(completed))
        save_progress(progress)

        print()

    print(f"Done! Transcribed {len(remaining)} episodes.")
    print(f"Transcripts saved to: {TRANSCRIPTS_DIR}")


if __name__ == "__main__":
    main()
