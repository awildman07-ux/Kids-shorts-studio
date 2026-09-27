#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf


def main():
    episode_path = Path(sys.argv[1])
    episode = json.loads(episode_path.read_text())
    out = Path("build/voices")
    out.mkdir(parents=True, exist_ok=True)
    try:
        from kokoro import KPipeline
        pipeline = KPipeline(lang_code="a")
    except Exception:
        pipeline = None

    timeline = []
    cursor = 1.0
    for index, line in enumerate(episode["lines"]):
        actor = episode["characters"][line["speaker"]]
        wav = out / f"{index:02d}-{line['speaker'].lower()}.wav"
        if pipeline:
            chunks = []
            for _, _, audio in pipeline(line["text"], voice=actor["voice"], speed=actor["speed"]):
                chunks.append(audio)
            sf.write(wav, np.concatenate(chunks), 24000)
        else:
            subprocess.run([
                "espeak-ng", "-w", str(wav), "-s", str(int(155 * actor["speed"])),
                "-p", "58", line["text"]
            ], check=True)
        info = sf.info(wav)
        duration = info.frames / info.samplerate
        timeline.append({**line, "audio": str(wav), "start": cursor, "duration": duration})
        cursor += duration + 0.45

    Path("build").mkdir(exist_ok=True)
    Path("build/timeline.json").write_text(json.dumps({"duration": cursor + 2.5, "lines": timeline}, indent=2))


if __name__ == "__main__":
    main()

