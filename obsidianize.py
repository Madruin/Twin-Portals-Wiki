#!/usr/bin/env python3
"""
Add YAML frontmatter to all Twin Portals transcripts for Obsidian compatibility.
Also creates index/MOC and reference pages.
"""
import json, os, re
from pathlib import Path

BASE_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
EPISODES_FILE = BASE_DIR / "episodes.json"

with open(EPISODES_FILE, "r", encoding="utf-8") as f:
    episodes = json.load(f)

# Build lookup by episode number
ep_lookup = {ep["num"]: ep for ep in episodes}

# Map transcript files to episode numbers
transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.md"))

def extract_episode_num(filepath):
    """Extract the overall episode number from the transcript content."""
    text = filepath.read_text(encoding="utf-8")
    # Look for "Overall #N" pattern
    m = re.search(r"Overall #(\d+)", text)
    if m:
        return int(m.group(1))
    # Fallback: parse from filename S01E01 pattern
    m = re.search(r"S(\d+)E(\d+)", filepath.name)
    if m:
        season, ep = int(m.group(1)), int(m.group(2))
        if season == 1:
            return ep
        elif season == 2:
            return 30 + ep
        elif season == 3:
            return 68 + ep
    return None

def parse_duration(text):
    """Extract duration from transcript header."""
    m = re.search(r"\*\*Duration:\*\*\s*(\S+)", text)
    return m.group(1) if m else ""

print("Adding frontmatter to transcripts...")
for fp in transcript_files:
    text = fp.read_text(encoding="utf-8")

    # Skip if already has frontmatter
    if text.startswith("---\n"):
        print(f"  Skipping {fp.name} (already has frontmatter)")
        continue

    num = extract_episode_num(fp)
    if num is None or num not in ep_lookup:
        print(f"  WARNING: Could not map {fp.name} to episode number")
        continue

    ep = ep_lookup[num]
    duration = parse_duration(text)
    is_live = "LIVE" in ep["title"] or "Live" in ep["title"]

    # Build frontmatter
    frontmatter = f"""---
title: "{ep['title']}"
season: {ep['season']}
episode: {ep['episode']}
overall: {ep['num']}
date: {ep['date']}
duration: "{duration}"
type: episode
live: {str(is_live).lower()}
tags:
  - twin-portals
  - season-{ep['season']}
  - transcript
---

"""

    # Remove the old header (title, season/episode info, date, duration, ---)
    # and replace with frontmatter + clean header
    # Strip existing header up to "## Transcript"
    lines = text.split("\n")
    transcript_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "## Transcript":
            transcript_start = i
            break

    # Build new content
    new_content = frontmatter
    new_content += f"# {ep['title']}\n\n"
    new_content += f"[[Season {ep['season']}]] | Episode {ep['episode']} | Overall #{ep['num']}  \n"
    new_content += f"Air Date: {ep['date']} | Duration: {duration}\n\n"
    new_content += f"---\n\n"
    # Add the transcript content
    new_content += "\n".join(lines[transcript_start:])

    fp.write_text(new_content, encoding="utf-8")
    print(f"  Updated {fp.name}")

# --- Create reference pages ---

print("\nCreating reference pages...")

# Season MOC pages
for season_num in [1, 2, 3]:
    season_eps = [ep for ep in episodes if ep["season"] == season_num]
    date_range = f"{season_eps[0]['date']} to {season_eps[-1]['date']}"

    content = f"""---
title: "Season {season_num}"
type: season
tags:
  - twin-portals
  - season-{season_num}
---

# Season {season_num}

**Episodes:** {len(season_eps)} | **Dates:** {date_range}

## Episodes

| # | Episode | Date |
|---|---------|------|
"""
    for ep in season_eps:
        # Find the transcript filename
        matching = [f for f in transcript_files if f"S{ep['season']:02d}E{ep['episode']:02d}" in f.name]
        if matching:
            link = f"[[{matching[0].stem}|{ep['title']}]]"
        else:
            link = ep["title"]
        content += f"| {ep['num']} | {link} | {ep['date']} |\n"

    (TRANSCRIPTS_DIR / f"Season {season_num}.md").write_text(content, encoding="utf-8")
    print(f"  Created Season {season_num}.md")

# Character pages
characters = [
    {
        "name": "Scoot Sparkles",
        "player": "Scott Hebert",
        "race": "Half-Orc",
        "class": "Barbarian",
        "background": "Sailor",
        "aliases": ["Scoots", "Scoot"],
    },
    {
        "name": "Ylka Gralhund",
        "player": "Beth",
        "race": "Human",
        "class": "Bard",
        "background": "",
        "aliases": ["Ylka", "Ilka"],
    },
    {
        "name": "Malark Wavesilver",
        "player": "Justin",
        "race": "Human",
        "class": "Rogue",
        "background": "",
        "aliases": ["Lark", "Malark"],
    },
    {
        "name": "Xaerine Rumblestride",
        "player": "Kendra",
        "race": "",
        "class": "",
        "background": "",
        "aliases": ["Xae", "Xaerine"],
    },
]

for char in characters:
    aliases_str = ", ".join(char["aliases"])
    content = f"""---
title: "{char['name']}"
type: character
player: "{char['player']}"
race: "{char['race']}"
class: "{char['class']}"
tags:
  - twin-portals
  - character
  - swoj
---

# {char['name']}

**Player:** {char['player']}
"""
    if char["race"]:
        content += f"**Race:** {char['race']}  \n"
    if char["class"]:
        content += f"**Class:** {char['class']}  \n"
    if char["background"]:
        content += f"**Background:** {char['background']}  \n"
    content += f"**Also known as:** {aliases_str}  \n"
    content += f"**Party:** [[Silver Waves of Justice|SWOJ]]\n"

    (TRANSCRIPTS_DIR / f"{char['name']}.md").write_text(content, encoding="utf-8")
    print(f"  Created {char['name']}.md")

# SWOJ page
swoj_content = """---
title: "Silver Waves of Justice"
type: party
aliases:
  - SWOJ
tags:
  - twin-portals
  - party
---

# Silver Waves of Justice (SWOJ)

The adventuring party at the heart of Twin Portals.

## Members

- [[Scoot Sparkles]] — Half-Orc Barbarian (played by Scott Hebert)
- [[Ylka Gralhund]] — Human Bard (played by Beth)
- [[Malark Wavesilver]] — Human Rogue (played by Justin)
- [[Xaerine Rumblestride]] — (played by Kendra)

## About

SWOJ is the adventuring party in the Twin Portals D&D 5E actual play podcast, recorded in Duluth, Minnesota. The podcast is co-created and DM'd by Matias Valero, with co-host Scott Hebert.
"""
(TRANSCRIPTS_DIR / "Silver Waves of Justice.md").write_text(swoj_content, encoding="utf-8")
print("  Created Silver Waves of Justice.md")

# Main index / MOC
index_content = """---
title: "Twin Portals Wiki"
type: index
tags:
  - twin-portals
  - moc
---

# Twin Portals Wiki

A searchable archive of all **78 episodes** of the [Twin Portals](https://twinportals.libsyn.com/) D&D 5E actual play podcast from Duluth, Minnesota.

**DM:** Matias Valero | **Co-host:** Scott Hebert

## The Party

[[Silver Waves of Justice|SWOJ — Silver Waves of Justice]]

| Character | Player | Race | Class |
|-----------|--------|------|-------|
| [[Scoot Sparkles]] | Scott Hebert | Half-Orc | Barbarian |
| [[Ylka Gralhund]] | Beth | Human | Bard |
| [[Malark Wavesilver]] | Justin | Human | Rogue |
| [[Xaerine Rumblestride]] | Kendra | | |

## Seasons

- [[Season 1]] — 30 episodes (Dec 2018 – Dec 2021)
- [[Season 2]] — 38 episodes (Feb 2022 – May 2025)
- [[Season 3]] — 10 episodes (May 2025 – Feb 2026)

## All Episodes

"""

for ep in episodes:
    matching = [f for f in transcript_files if f"S{ep['season']:02d}E{ep['episode']:02d}" in f.name]
    if matching:
        link = f"[[{matching[0].stem}|{ep['title']}]]"
    else:
        link = ep["title"]
    index_content += f"1. {link} ({ep['date']})\n"

index_content += """
---

*Transcripts generated with [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (base model). Speaker diarization not included.*
"""

(TRANSCRIPTS_DIR / "Twin Portals Wiki.md").write_text(index_content, encoding="utf-8")
print("  Created Twin Portals Wiki.md")

print("\nDone! All transcripts updated with Obsidian frontmatter and reference pages created.")
