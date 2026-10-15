#!/usr/bin/env python3
"""URL in, transcript out. Instagram, Facebook, X, TikTok, YouTube, or a local file.

    vidtext.py <url> [--model medium|large|small] [--lang es] [--out DIR]
    vidtext.py <file.mp4|file.mp3> [...]

Two paths, cheapest first:

  1. If the platform already has captions, take them. Seconds, and free.
  2. Otherwise pull the audio with yt-dlp and transcribe it locally with Whisper.

Nothing is uploaded anywhere. The transcription runs on this machine.

Writes a markdown file with provenance frontmatter and prints its path. It never
writes into the current repo unless you pass --out, so it cannot pollute a wiki
or a research directory by accident.
"""
import argparse
import platform
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

CACHE = Path.home() / ".cache" / "vidtext"
# Logged-out fetches fail on Instagram/Facebook/X. Try clean first, then borrow
# cookies from whichever browser is actually signed in.
BROWSERS = ["chrome", "brave", "safari", "firefox", "edge"]

MODELS = {
    "small": "mlx-community/whisper-small-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "large": "mlx-community/whisper-large-v3-mlx",
}


def sh(cmd, quiet=True):
    return subprocess.run(
        cmd,
        capture_output=quiet,
        text=True,
        stdin=subprocess.DEVNULL,
    )


APPLE_SILICON = platform.system() == "Darwin" and platform.machine() == "arm64"


def installed_browsers():
    if platform.system() != "Darwin":
        # yt-dlp finds each browser's profile itself on Windows and Linux, and fails fast
        # when one isn't there. Inside WSL the browsers live on the Windows side, so this
        # finds nothing and login-gated posts need a public link or a local file instead.
        return ["chrome", "brave", "firefox", "edge", "chromium"]
    apps = {
        "chrome": "Google Chrome",
        "brave": "Brave Browser",
        "safari": "Safari",
        "firefox": "Firefox",
        "edge": "Microsoft Edge",
    }
    return [b for b in BROWSERS if Path(f"/Applications/{apps[b]}.app").exists()]


def with_auth(base_cmd):
    """Run a yt-dlp command, escalating to browser cookies only if needed.

    Returns (CompletedProcess, cookie_arg_used). A private or age-gated post is
    the normal reason for the first attempt to fail, and it is not an error worth
    reporting until every browser has been tried.
    """
    r = sh(base_cmd)
    if r.returncode == 0:
        return r, []
    for b in installed_browsers():
        arg = ["--cookies-from-browser", b]
        r = sh(base_cmd + arg)
        if r.returncode == 0:
            print(f"   (used {b} cookies)", file=sys.stderr)
            return r, arg
    return r, None


def slugify(s, n=60):
    s = re.sub(r"[^\w\s-]", "", (s or "").lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:n] or "video"


def vtt_to_text(path: Path) -> str:
    """Caption files are timestamps, positioning tags and duplicated rolling lines."""
    out, seen = [], None
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if (
            not line
            or "-->" in line
            or line.isdigit()
            or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE"))
        ):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\{\\[^}]+\}", "", line).strip()
        if line and line != seen:
            out.append(line)
            seen = line
    return " ".join(out)


def get_captions(url, work: Path, langs: str):
    cmd = [
        "yt-dlp", "--skip-download",
        "--write-subs", "--write-auto-subs",
        "--sub-langs", langs, "--sub-format", "vtt",
        "-o", str(work / "cap.%(ext)s"), url,
    ]
    with_auth(cmd)
    vtts = sorted(work.glob("cap*.vtt"))
    if not vtts:
        return None
    text = vtt_to_text(vtts[0])
    return text if len(text) > 200 else None


def get_audio(url, work: Path):
    cmd = [
        "yt-dlp", "-f", "bestaudio/best",
        "-x", "--audio-format", "mp3", "--audio-quality", "5",
        "-o", str(work / "audio.%(ext)s"), url,
    ]
    r, _ = with_auth(cmd)
    hits = sorted(work.glob("audio.*"))
    if not hits:
        sys.exit(f"could not download audio.\n{(r.stderr or '')[-1500:]}")
    return hits[0]


def transcribe(audio: Path, model: str, lang: str | None, work: Path) -> tuple[str, str]:
    """mlx-whisper on Apple Silicon (several times faster); openai-whisper everywhere else."""
    lang_args = ["--language", lang] if lang else []
    if APPLE_SILICON and shutil.which("uv"):
        r = sh([
            "uv", "run", "--quiet", "--with", "mlx-whisper", "mlx_whisper",
            str(audio), "--model", MODELS.get(model, model),
            "--output-format", "txt", "--output-dir", str(work), *lang_args,
        ])
        txt = work / (audio.stem + ".txt")
        if r.returncode == 0 and txt.exists():
            return txt.read_text().strip(), f"mlx-whisper {model}"
    # openai-whisper: the installed command if there is one, else through uv (no global install).
    runner = (["whisper"] if shutil.which("whisper")
              else ["uv", "run", "--quiet", "--with", "openai-whisper", "whisper"] if shutil.which("uv")
              else None)
    if runner:
        r = sh([
            *runner, str(audio), "--model", model,
            "--output_format", "txt", "--output_dir", str(work), *lang_args,
        ])
        txt = work / (audio.stem + ".txt")
        if r.returncode == 0 and txt.exists():
            return txt.read_text().strip(), f"openai-whisper {model}"
        sys.exit(f"transcription failed.\n{(r.stderr or '')[-1500:]}")
    sys.exit("no whisper available. Install uv (preferred) or openai-whisper; see the skill's Requirements.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="video URL, or a local audio/video file")
    ap.add_argument("--model", default=None, help="small | medium | large (default medium). Naming a model skips platform captions")
    ap.add_argument("--lang", default=None, help="force a language, e.g. es. Default: auto-detect")
    ap.add_argument("--out", default=None, help="write the transcript here instead of the cache")
    ap.add_argument("--no-captions", action="store_true", help="always transcribe, ignore platform captions")
    a = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    local = Path(a.target)
    is_local = local.exists()
    # A fresh work folder per run, so two runs at once can't erase or mix each other's files.
    work = Path(tempfile.mkdtemp(prefix="work-", dir=CACHE))
    try:
        run(a, local, is_local, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run(a, local: Path, is_local: bool, work: Path):
    model = a.model or "medium"
    # Asking for a model means asking for a transcription: captions would bypass it.
    use_captions = not a.no_captions and a.model is None

    meta, method, text = {}, None, None

    if is_local:
        meta = {"title": local.stem, "webpage_url": str(local.resolve())}
    else:
        if not shutil.which("yt-dlp"):
            sys.exit("yt-dlp not found. brew install yt-dlp")
        print("→ reading video metadata", file=sys.stderr)
        r, _ = with_auth(["yt-dlp", "-J", "--no-warnings", a.target])
        if r.returncode != 0:
            sys.exit(
                "could not read that URL.\n"
                "Private, deleted, or login-gated. If it needs a login, open the post in a\n"
                "browser you are signed into and try again.\n\n" + (r.stderr or "")[-1200:]
            )
        try:
            meta = json.loads(r.stdout)
        except json.JSONDecodeError:
            meta = {}

        if use_captions:
            print("→ checking for existing captions", file=sys.stderr)
            langs = a.lang or "en,es"
            text = get_captions(a.target, work, f"{langs},{langs}-orig")
            if text:
                method = "platform captions"

    if text is None:
        audio = local if is_local else None
        if audio is None:
            print("→ no usable captions, downloading audio", file=sys.stderr)
            audio = get_audio(a.target, work)
        print(f"→ transcribing locally ({model})", file=sys.stderr)
        text, method = transcribe(audio, model, a.lang, work)

    title = meta.get("title") or "untitled"
    stem = f"{date.today()}-{slugify(meta.get('extractor_key', 'local'))}-{slugify(title, 48)}"
    outdir = Path(a.out) if a.out else CACHE
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / f"{stem}.md"
    # Never overwrite a different transcript. Re-running with a bigger model is a comparison,
    # not a replacement: on a real clip the large model fixed three proper nouns and silently
    # dropped a whole sentence the medium model caught. So a file is reused only when it holds
    # the same source AND the same method; anything else gets the next free suffix, claimed
    # atomically so two runs at once can't take the same name.
    source = str(meta.get("webpage_url") or a.target)
    n = 1
    while True:
        dest = outdir / (f"{stem}.md" if n == 1 else f"{stem}-{n}.md")
        try:
            os.close(os.open(dest, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except FileExistsError:
            prev = dest.read_text()
            same_src = re.search(r"^source_url: (.+)$", prev, re.M)
            same_method = re.search(r"^method: (.+)$", prev, re.M)
            if (same_src and same_src.group(1).strip() == source
                    and same_method and same_method.group(1).strip() == method):
                break
            n += 1

    dur = meta.get("duration")
    fm = [
        "---",
        f"source_url: {source}",
        f"platform: {meta.get('extractor_key', 'local file')}",
        f"title: {json.dumps(title)}",
        f"uploader: {json.dumps(meta.get('uploader') or meta.get('channel') or '~')}",
        f"upload_date: {meta.get('upload_date') or '~'}",
        f"duration_sec: {dur or '~'}",
        f"extracted: {date.today()}",
        f"method: {method}",
        "source_tier: 3          # social video. Navigation only, never the source of a number.",
        "---",
        "",
        f"# {title}",
        "",
    ]
    desc = (meta.get("description") or "").strip()
    if desc:
        fm += ["## Post text as published", "", "```", desc[:4000], "```", ""]
    fm += ["## Transcript", "", text, ""]
    dest.write_text("\n".join(fm))

    words = len(text.split())
    print(f"\n{dest}")
    dur = int(dur or 0)
    print(f"  {words} words · {method}" + (f" · {dur // 60}m{dur % 60:02d}s" if dur else ""))
    if words < 30:
        print("  WARNING: almost no speech recovered. The video may be music or text-on-screen only.")


if __name__ == "__main__":
    main()
