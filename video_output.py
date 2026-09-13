#!/usr/bin/env python3
"""
video_output.py - optional bonus output for voxel_cli.py: turns a finished
picture book (pages with text + generated illustration images) into a
narrated marketing video (one image on screen per page, narrated aloud,
concatenated into a single MP4).

Uses Chatterbox TTS, per Zia's own established preference across Nova,
Marius, and TechPulse (all three ended up on Chatterbox after trying
Kokoro and Edge TTS first - see HANDOFF.md for that history). No new
paid API, no new secret required.

Requires ffmpeg to be installed (already present on GitHub Actions'
ubuntu-latest runners by default; on a laptop, `apt install ffmpeg` /
`brew install ffmpeg`).

This is book-only marketing content, separate from the print product
itself (the interior/cover PDFs are unaffected either way).
"""

import subprocess
import wave
from pathlib import Path


def _synthesize_narration(text, out_wav_path):
    """One page's narration audio via Chatterbox, run on CPU (no GPU
    assumed - GitHub Actions runners are CPU-only)."""
    from chatterbox.tts import ChatterboxTTS  # imported lazily - only needed if --video is used
    import torchaudio

    model = _synthesize_narration._model
    if model is None:
        model = ChatterboxTTS.from_pretrained(device="cpu")
        _synthesize_narration._model = model

    wav = model.generate(text)
    torchaudio.save(str(out_wav_path), wav, model.sr)


_synthesize_narration._model = None  # cached across pages so it only loads once per run


def _wav_duration_seconds(wav_path):
    with wave.open(str(wav_path), "rb") as f:
        return f.getnframes() / float(f.getframerate())


def build_narrated_video(pages, image_files, out_path, fps=24):
    """
    pages: Voxel's page list (dicts with 'text' and 'page_number')
    image_files: matching list of image file paths (same order as pages)
    out_path: where to write the final .mp4

    Skips pages with no usable image. Pages with empty text get a fixed
    2s silent hold instead of narration, so front/back-matter-only pages
    don't break the pipeline.
    """
    out_path = Path(out_path)
    work_dir = out_path.parent / "_video_work"
    work_dir.mkdir(parents=True, exist_ok=True)

    clip_paths = []
    for i, (page, image_path) in enumerate(zip(pages, image_files)):
        if not image_path or not Path(image_path).exists():
            continue

        text = (page.get("text") or "").strip()
        clip_path = work_dir / f"clip_{i:03d}.mp4"

        if text:
            wav_path = work_dir / f"narration_{i:03d}.wav"
            _synthesize_narration(text, wav_path)
            duration = max(_wav_duration_seconds(wav_path), 1.0)

            # Still image for the narration's duration, audio muxed in.
            subprocess.run([
                "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
                "-i", str(wav_path),
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac",
                "-b:a", "192k", "-pix_fmt", "yuv420p",
                "-t", str(duration), "-r", str(fps),
                str(clip_path),
            ], check=True, capture_output=True)
        else:
            # No text on this page (e.g. a pure-illustration spread) -
            # fixed 2s silent hold instead of skipping it entirely.
            subprocess.run([
                "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
                "-c:v", "libx264", "-tune", "stillimage",
                "-pix_fmt", "yuv420p", "-t", "2", "-r", str(fps),
                str(clip_path),
            ], check=True, capture_output=True)

        clip_paths.append(clip_path)

    if not clip_paths:
        raise RuntimeError("No pages had usable images - nothing to build a video from.")

    concat_list_path = work_dir / "concat_list.txt"
    concat_list_path.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in clip_paths)
    )

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path), "-c", "copy", str(out_path),
    ], check=True, capture_output=True)

    return out_path
