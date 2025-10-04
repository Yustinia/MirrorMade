import subprocess
import shutil


class SrcpyWrapper:
    def __init__(self, audio: int, quality: int, latency: int) -> None:
        if not shutil.which("scrcpy") or not shutil.which("adb"):
            raise RuntimeError("scrcpy and adb not found in PATH")

        self.base_opts = ["scrcpy"]

        audio_opt = self.with_audio(audio)
        if audio_opt:
            self.base_opts.extend(audio_opt)

        quality_opt = self.quality(quality)
        if quality_opt:
            self.base_opts.extend(quality_opt)

        latency_opt = self.with_latency(latency)
        if latency_opt:
            self.base_opts.extend(latency_opt)

    def with_audio(self, sel_opt: int):
        audio_opts = {
            1: [],  # audio forward
            2: ["--no-audio"],  # disable audio forward
        }

        return audio_opts[sel_opt]

    def quality(self, sel_opt: int):
        quality_opts = {
            1: ["--video-bit-rate=8M", "--audio-bit-rate=128K"],  # hq
            2: ["--video-bit-rate=4M", "--audio-bit-rate=96K"],  # mq
            3: ["--video-bit-rate=2M", "--audio-bit-rate=64K"],  # lq
        }

        return quality_opts[sel_opt]

    def with_latency(self, sel_opt: int):
        latency_opt = {
            1: ["--video-buffer=1000", "--audio-buffer=1000"],
            2: ["--video-buffer=0", "--audio-buffer=0"],
        }

        return latency_opt[sel_opt]

    def runner(self):
        subprocess.run(self.base_opts)


def choice_with_audio(choice):
    if choice in [1, 2]:
        return choice
    raise ValueError(f"{choice} is not an option for audio")


def choice_quality(choice):
    if choice in [1, 2, 3]:
        return choice
    raise ValueError(f"{choice} is not an option for quality")


def choice_with_latency(choice):
    if choice in [1, 2]:
        return choice
    raise ValueError(f"{choice} is not an option for latency")


def display_opts() -> None:
    disp = [
        "Usage: Enter 3 digits",
        "Audio: 1 — Audio Forward, 2 — No Audio Forward",
        "Quality: 1 — HQ, 2 — MD, 3 — LQ",
        "Latency: 1 — 1s, 2 — No latency",
    ]

    print()
    for line in disp:
        print(line)
    print()


def main():
    display_opts()
    try:
        user_opts = input("Enter options: ")

        if len(user_opts) != 3 or not user_opts.isdigit():
            raise ValueError("Must enter 3 digits")

        capture_errors = []
        aopt = bopt = copt = 0

        try:
            aopt = choice_with_audio(int(user_opts[0]))
        except ValueError as e:
            capture_errors.append(str(e))

        try:
            bopt = choice_quality(int(user_opts[1]))
        except ValueError as e:
            capture_errors.append(str(e))

        try:
            copt = choice_with_latency(int(user_opts[2]))
        except ValueError as e:
            capture_errors.append(str(e))

        if capture_errors:
            raise ValueError("\n".join(capture_errors))

        scrcpy = SrcpyWrapper(aopt, bopt, copt)
        scrcpy.runner()

    except ValueError as e:
        print(f"Error: {e}")


main()
