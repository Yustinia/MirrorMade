import subprocess
import shutil


class SrcpyWrapper:
    def __init__(self, audio: int, quality: int) -> None:
        if not shutil.which("scrcpy"):
            raise RuntimeError("scrcpy not found in PATH")

        self.base_opts = ["scrcpy"]

        audio_opt = self.audio_forwarding(audio)
        if audio_opt:
            self.base_opts.extend(audio_opt)

        quality_opt = self.quality(quality)
        if quality_opt:
            self.base_opts.extend(quality_opt)

    def audio_forwarding(self, sel_opt: int):
        audio_opts = {
            1: [],  # audio forward
            2: ["--no-audio"],  # disable audio forward
        }

        if sel_opt not in audio_opts:
            return f"'{sel_opt}' is not a PRESET"
        return audio_opts[sel_opt]

    def quality(self, sel_opt: int):
        quality_opts = {
            1: None,  # hq
            2: None,  # mq
            3: None,  # lq
        }

        if sel_opt not in quality_opts:
            return f"'{sel_opt}' is not an OPTION"
        return quality_opts[sel_opt]

    def runner(self):
        subprocess.run(self.base_opts)
