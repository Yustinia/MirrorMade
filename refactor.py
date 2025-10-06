import subprocess
import shutil


class SrcpyWrapper:
    def __init__(self, audioQuality: int, videoQuality: int, latency: int) -> None:
        if not shutil.which("scrcpy") or not shutil.which("adb"):
            raise RuntimeError("SCRCPY or ADB not found in PATH")

        self.baseOpts = ["scrcpy"]

        ifWithAudio = self.ifWithAudio(audioQuality)
        if ifWithAudio:
            self.baseOpts.extend(ifWithAudio)

        defVideoQuality = self.defVideoQuality(videoQuality)
        if defVideoQuality:
            self.baseOpts.extend(defVideoQuality)

        delayLatency = self.delayLatency(latency)
        if delayLatency:
            self.baseOpts.extend(delayLatency)

    def ifWithAudio(self, selOption):
        audioOpts = {
            1: [],  # audio forward
            2: ["--no-audio"],  # no audio forward
        }

        return audioOpts[selOption]

    def defVideoQuality(self, selOption):
        vidQualityOpts = {
            1: ["--video-bit-rate=8M", "--audio-bit-rate=128K"],  # hq
            2: ["--video-bit-rate=4M", "--audio-bit-rate=96K"],  # mq
            3: ["--video-bit-rate=2M", "--audio-bit-rate=64K"],  # lq
        }

        return vidQualityOpts[selOption]

    def delayLatency(self, selOption):
        latencyOpts = {
            1: ["--video-buffer=1000", "--audio-buffer=1000"],
            2: ["--video-buffer=0", "--audio-buffer=0"],
        }

        return latencyOpts[selOption]

    def _scrcpyRunner(self):
        subprocess.run(self.baseOpts)


class ScrcpyChoice:
    @staticmethod
    def choiceWithAudio(choice):
        if choice in [1, 2]:
            return choice
        raise ValueError(f"{choice} is not an option for AUDIO")

    @staticmethod
    def choiceVidQuality(choice):
        if choice in [1, 2, 3]:
            return choice
        raise ValueError(f"{choice} is not an option for VIDEO QUALITY")

    @staticmethod
    def choiceWithLatency(choice):
        if choice in [1, 2]:
            return choice
        raise ValueError(f"{choice} is not an option for LATENCY")


try:
    testInput = int(input("Enter choice"))
    ScrcpyChoice.choiceWithAudio(testInput)

except ValueError as e:
    print("Error:", e)
