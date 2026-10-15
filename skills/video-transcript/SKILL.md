---
name: video-transcript
description: "Extract the spoken text from a video or audio file so it can be read, discussed and checked. Use when the user pastes a link to Instagram, Facebook, X, TikTok, YouTube or similar and says 'transcribe this', 'extract the text', 'what does this video say', 'here's a video about X, let's talk about it', or drops a video URL with little other context. Also handles local .mp4/.mp3/.m4a files, and is the transcription step of meeting-to-notes."
metadata:
  version: 0.9.0
  maturity: working
  related-playbook: [memory-system]
  tags: [research, media, transcription, ingest]
---

# video-transcript

A video is not a source until someone has read what it says. This turns one into text, locally, in
seconds to a few minutes.

## The command

```sh
python3 <this-skill-folder>/vidtext.py <url-or-file>
```

| Flag | Use |
|---|---|
| `--model large` | Bad audio or a heavy accent. **Not automatically better**, see below. Naming a model always transcribes from the audio (skips captions) |
| `--lang es` | Force a language when auto-detect picks the wrong one |
| `--out DIR` | Write into a project instead of the cache |
| `--no-captions` | Ignore platform captions and transcribe from the audio |

## What it does

1. **Reads the metadata:** title, uploader, upload date, duration, and the post text. The caption
   under a video often carries the links, the disclosure and the sales pitch, so it's kept next to
   the speech.
2. **Takes the platform's captions if they exist.** Seconds, and free.
3. **Otherwise downloads the audio and transcribes it on your machine** (mlx-whisper on Apple
   Silicon, falling back to openai-whisper). Nothing is uploaded anywhere.
4. **Writes a markdown file with provenance frontmatter** and prints its path.

**Signed-in content.** Logged-out fetches fail on Instagram, Facebook and X. The script tries
without cookies first, then uses the cookies of a browser you're signed into (Chrome, Brave, Safari,
Firefox, Edge) and says which one it used. That is your own session reading content you can already
see; it never stores or sends the cookies anywhere else. If every browser fails, the post is private,
deleted, or needs a login you don't have.

## A bigger model is a second opinion, not an upgrade

Measured on a real 90-second Spanish clip, not assumed:

| | medium | large |
|---|---|---|
| Technical terms | garbled | **correct** |
| Company names | wrong | **still wrong, differently** |
| Content | complete | **silently dropped a sentence** with two hard numbers |

So `--model large` is a **comparison**: run once with `--model medium` and once with `--model large`,
and the script keeps both files instead of overwriting.
Read them against each other. **Neither model can be trusted on proper nouns.** Names, tickers and
product codes are exactly what a speech model guesses at. Treat every name in a transcript as
something to look up, and where two runs disagree, say so instead of picking one.

## Where the output goes

Default: `~/.cache/vidtext/<date>-<platform>-<title>.md`, deliberately outside any repo, so running it
inside a notes folder or a project can't leave stray files. A file is replaced only by a re-run of the
same source with the same method; anything else (another model, another source with the same
title) gets the next free `-2`, `-3`, claimed atomically, so even two runs at once never overwrite
each other. Each run also uses its own temporary work folder. Pass `--out` when the transcript should
be kept, so its provenance frontmatter survives.

## After extracting: say what it actually claims

Don't summarize a transcript into agreement with itself. Speech that sounds authoritative in 90
seconds reads thin on the page, and that gap is the useful part. Report:

- **The claims, listed**, with every product, company or number named.
- **Which carry evidence and which are assertion.** A number with no source is an assertion.
- **What is being sold:** affiliate links, a course, a newsletter, a position. Check the post text too.
- **What it leaves out:** time horizon, downside, cost, whether the speaker benefits.

A social video is navigation, a pointer to something worth checking, and never the source of a
number. The best thing it offers is a question: *is the thing this person is excited about true?*

## Requirements

`yt-dlp`, `ffmpeg`, and either `uv` (preferred, pulls mlx-whisper on first run) or `whisper`.
On macOS: `brew install yt-dlp ffmpeg`.
