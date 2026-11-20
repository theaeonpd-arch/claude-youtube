---
name: kids-story-studio
description: >
  Semi-automated production pipeline for a kids' (ages 4-7) animated moral-story
  YouTube channel. One command turns a value (sharing, honesty, courage...) into a
  complete episode package: fixed-structure story script, value song lyrics,
  character-consistent scene prompts, narration, Higgsfield image/video/audio
  generation (cost-approved), upload metadata, Shorts cut points and a QA checklist.
  Triggers on: "kids-story-studio", "new episode", "kids episode", "moral story
  episode", "story for kids about", "bölüm üret", "çocuk hikayesi", "değer bölümü".
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Kids Story Studio

Produces one episode of Huggleberry Studios, an English-language hand-drawn
2D animated moral-story channel for ages 4-7. Every episode teaches exactly ONE value, uses the same recurring
characters, and follows the same fixed structure so production is repeatable.

The goal is "smart automation", not mass production: YouTube's July 2025
"Inauthentic content" policy targets templated, repetitive, mass-produced
videos. Every episode must have an original story, a real lesson, consistent
characters and a human review pass. Never skip the QA step.

## Commands

| Command | What it does |
|---------|--------------|
| `/kids-story-studio <value>` | Full episode package for that value (steps 1-7, generation in step 5 needs approval) |
| `/kids-story-studio script <value>` | Steps 1-3 only (story, song, scenes); no generation |
| `/kids-story-studio generate <episode-folder>` | Step 5 only for an existing package |
| `/kids-story-studio compilation <month or values>` | Plan a 20+ min monthly compilation from finished episodes |
| `/kids-story-studio characters` | Create/refresh character sheets from `characters/` |
| `/kids-story-studio ideas` | Next 6 values + one-line story premises, avoiding repeats |

If no value is given, run `ideas` and ask the user to pick.

## Before Every Run (mandatory)

1. Read `characters/characters.md`. If it still contains `TODO`, stop and ask the
   user for the missing character details (name, age, species/look, personality,
   catchphrase, reference image). Never invent the main cast.
2. Read `channel.md` for channel name, voice style and episode counter.
3. Glob `episodes/*/` in the current working directory to find the next episode
   number and the values already used. Do not repeat a value within 6 episodes,
   and never reuse a previous story premise.

## Pipeline

### Step 1 — Story script
Load `references/episode-structure.md` and follow it exactly (6 beats, 4-6 min).
Load `references/values-bank.md` for the value's age-appropriate framing.
Rules:
- One value, one problem, one clear choice. Concrete everyday setting
  (playground, kitchen, school, park) a 4-year-old recognizes.
- The "wrong choice" beat shows a gentle, non-scary consequence (sadness,
  a friend walking away). No violence, danger, humiliation or shaming.
- The child-character solves it themselves; adults may guide, never lecture.
- Sentences <= 10 words, present tense, lots of repetition of the value word.
- Write the script to `episodes/<NN>-<value>/script.md`.

### Step 2 — Value song
Load `references/song-guide.md`. Write a 4-8 line chorus + 1 short verse that
restates the lesson, uses the value word at least 3 times and fits ~60 seconds.
Save to `lyrics.txt`. The chorus is also the main Short.
Also write `suno.txt` for the user (they produce songs in Suno Pro): Title,
Style of Music (reuse the fixed Huggleberry style from `references/song-guide.md`),
Exclude Styles, and Lyrics with Suno section tags ([Intro], [Chorus], [Verse],
[Bridge], [Final Chorus], [Outro], [End]). Do not generate the song in Higgsfield
unless the user asks.

### Step 3 — Scene list (character-consistent)
Load `references/prompt-rules.md` and `characters/characters.md`.
Break the script into 12-20 scenes. For each scene write a JSON object to
`scenes.json`:
```json
{"id": 1, "beat": "opening", "duration_s": 6, "characters": ["<name>"],
 "setting": "...", "action": "...", "emotion": "...", "camera": "...",
 "narration": "...", "image_prompt": "...", "video_prompt": "..."}
```
Every prompt MUST start with the fixed style line from `prompt-rules.md` and
reference characters by their locked description from `characters.md`, never
by improvised descriptions.

### Step 4 — Narration
Write `narration.txt`: narrator lines + character dialogue, labelled by speaker,
in scene order, with `[pause]` marks. Voice settings come from `channel.md`.

### Step 5 — Generation (Higgsfield, needs approval)
Only if Higgsfield tools are available (load via ToolSearch "Higgsfield").
1. Call the balance tool and the estimate_*_cost tools for: N scene images,
   M video clips, narration audio, song audio.
2. Show the user a cost table (per item + total + remaining balance) and WAIT for
   explicit approval. Never generate without it. Respect any budget they give.
3. Generate in batches (batch tools + jobs_wait), using the character sheet /
   reference media ids stored in `characters/characters.md` for consistency.
4. Record every job id / media id / URL in `assets.json` in the episode folder.
5. If a scene fails QA (Step 7), regenerate only that scene, after re-confirming cost.
If Higgsfield is unavailable, deliver the prompts only and say so.

### Step 6 — Upload package
Load `references/metadata-template.md` and write `metadata.txt`:
title (<= 60 chars, value keyword first), description (hook line, lyrics,
moral summary for parents, 3 hashtags), thumbnail brief, playlist, and the
"Made for Kids: YES" reminder. Also write `shorts.md` with 1-2 Short cut points
(start/end scene ids, vertical crop notes, on-screen text).

### Step 7 — QA checklist
Copy `references/qa-checklist.md` into `qa.md` in the episode folder, pre-fill
every item you can verify from the text (value clarity, sentence length,
repetition, no scary content), and list the visual checks the human must do
on the generated media. Tell the user which items still need their eyes.

## Output

End every run with a short summary in the user's language (Turkish if they write
Turkish): episode folder path, files produced, generation cost actually spent,
open QA items, and the next suggested value.

## Folder Layout (in the current working directory)

```
episodes/
  01-sharing/
    script.md  lyrics.txt  scenes.json  narration.txt
    metadata.txt  shorts.md  qa.md  assets.json
```

## Hard Rules
- Made for Kids content: no external links for kids, no data collection asks,
  no "comment below" CTAs (comments are disabled on MFK videos).
- No real brands, licensed characters or copyrighted songs/melodies
  (no "to the tune of ..." of copyrighted works; public-domain nursery melodies are fine).
- No fake "educational" claims; the value is social-emotional, not medical.
- Never auto-publish. Uploading stays a human step.
