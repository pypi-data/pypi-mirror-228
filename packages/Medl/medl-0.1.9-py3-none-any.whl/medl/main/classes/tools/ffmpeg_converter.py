from pathlib import Path
import subprocess
from typing import List

from medl.common import MedlException

__all__ = ["FfmpegConverter"]


class FfmpegConverter:
    FFMPEG_FORMATS = {
        "mp3": ["-codec:a", "libmp3lame"],
        "flac": ["-codec:a", "flac", "-sample_fmt", "s16"],
        "ogg": ["-codec:a", "libvorbis"],
        "opus": ["-codec:a", "libopus"],
        "m4a": ["-codec:a", "aac"],
        "wav": ["-codec:a", "pcm_s16le"],
    }

    def __init__(self):
        pass

    def convert(self, input_file: Path, output_file: Path) -> None:
        arguments: List[str] = [
            "-nostdin",
            "-y",
            "-i",
            str(input_file.resolve()),
            "-movflags",
            "+faststart",
            "-v",
            "debug",
            "-progress",
            "-",
            "-nostats",
            "-vn",
        ]

        file_format = input_file.suffix[1:]
        output_format = output_file.suffix[1:]

        # Add output format to command
        # -c:a is used if the file is not an matroska container
        # and we want to convert to opus
        # otherwise we use arguments from FFMPEG_FORMATS
        if output_format == "opus" and file_format != "webm":
            arguments.extend(["-c:a", "libopus"])
        elif (output_format == "opus" and file_format == "webm") or (
            output_format == "m4a" and file_format == "m4a"
        ):
            # Copy the audio stream to the output file
            arguments.extend(["-c:a", "copy"])
        else:
            arguments.extend(self.FFMPEG_FORMATS[output_format])

        arguments.append(str(output_file.resolve()))

        with subprocess.Popen(
            ["ffmpeg", *arguments],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        ) as process:
            proc_out = process.communicate()  # wait for process

            if process.returncode != 0:  # if error
                # join stdout and stderr and decode to utf-8
                message = b"".join([out for out in proc_out if out]).decode("utf-8")
                raise MedlException(
                    f"Command : {' '.join(['ffmpeg', *arguments])}\nError message : {message}"
                )
