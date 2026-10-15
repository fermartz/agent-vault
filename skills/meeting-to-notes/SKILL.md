---
name: meeting-to-notes
description: "Turn a meeting recording into durable notes: transcribe it locally, keep the raw transcript as evidence, confirm the takeaways with the user, then update the project notes, tasks and open loops. Use when the user says 'transcribe the meeting', 'read the last audio', 'here's the recording of my call with X', 'I forgot two more audios from the same meeting', or drops a call recording (.m4a, .mp3, .mp4, voice notes) and wants it in their notes, even if they only say 'transcribe it'."
metadata:
  version: 0.10.0
  maturity: working
  related-playbook: [memory-system, human-context]
  related-skills: [video-transcript, llm-wiki]
  tags: [meetings, transcription, notes, memory, agents]
---

# meeting-to-notes

A meeting that isn't written down didn't decide anything. The decisions, the numbers and who owes
what live in the recording until an agent moves them into files. This is
[Give the Agent a Memory](../../playbook/memory-system.md) applied to calls.

## Requirements

Same as [video-transcript](../video-transcript/SKILL.md#requirements), minus `yt-dlp` (recordings are local files):
Python 3.10+, `ffmpeg`, and `uv` or `whisper`.

One-line check: `python3 -c 'import sys; assert sys.version_info >= (3, 10)'; ffmpeg -version | head -1; uv --version || whisper --help | head -1`

**Check before the first run.** Run the check command. If anything is missing, tell the user exactly what and the install command, and **ask before installing anything**: installing changes their machine ([Hand Over Keys, Not the Keyring](../../playbook/least-privilege.md)). On Windows, use WSL or the commands in [getting started](../../docs/getting-started.md#windows).

## Procedure

1. **Find the recording and pin its date.** File timestamps lie: a call recorded on a phone and
   sent to the laptop days later carries the transfer date. If the user says "last week" and the file
   says today, ask which meeting it was, and use the meeting's date everywhere after this.
2. **Look for the other parts.** Phones split long calls, and users forget files. Check the
   download folder for siblings from the same day. Order parts by content, not by filename: a part
   that ends mid-sentence ("let me check with my team…") continues in the part that starts there.
3. **Transcribe locally.** Use [video-transcript](../video-transcript/SKILL.md)
   (`vidtext.py <file> --lang <language>`) or Whisper `medium` directly. Set the language. Run
   in the background and one file at a time: two transcriptions in parallel fight over the CPU and
   both finish later. On a CPU, expect roughly real time per file.
4. **Save the raw transcript as evidence.** One file per meeting, all parts in order, with a header
   that records: meeting date, participants, source files and lengths, the model, gaps (e.g. "the
   recording starts mid-meeting"), and **likely mishearings listed in the header, never corrected in
   the text**. After that, the body is never rewritten. Notes can be wrong and get fixed; the evidence
   stays what was said.
5. **Read it against what you already know.** If a prep sheet or question list exists for this
   meeting, check every question: answered, or "not covered". Note what the recording can't answer.
6. **Give the takeaways and stop.** Short, per
   [Protect the Human's Context](../../playbook/human-context.md): decisions, numbers, who owes what
   by when, open questions. Quote the exact words for anything that matters ("one series of four or
   five episodes"). Then ask if it's right. Don't touch the notes before the user confirms: they
   were in the room, and the transcript can't hear tone.
7. **Update the notes in the same turn as the confirmation.** The project page, the prep sheet's
   answers, people's pages if a fact about them changed. Every commitment becomes a task: owed by the
   user = their turn; waiting on someone else = waiting, with who. Close tasks the meeting resolved.
8. **Report what changed**, one line per file, and the next action.

## Notes

- **Consent and privacy.** Recordings capture other people. Transcribe locally, keep raw files in
  private storage, and never paste a transcript into a public place.
- **Proper nouns are guesses.** Product names, company names and people's names are where speech
  models fail. Flag them in the header and confirm the important ones with the user.
- **Don't price, plan or promise from the transcript alone.** If the user then asks "what can we
  charge?", answer as a separate step and label it an estimate, not something the meeting said.
- **Late parts.** If more parts arrive before anything is committed, rebuild the raw file with all
  parts in order. Once committed, add later material as a new, clearly dated section.
