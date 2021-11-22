from os import path

from yt_dlp import YoutubeDL

from ZeroTwo.config import DURATION_LIMIT
from ZeroTwo.helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"**Sorry!** 🥲 \n__I Can't Play Songs Longer Than {DURATION_LIMIT} Minutes!__",
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"**Sorry!** 🥲 \n__I Can't Play Songs Longer Than {DURATION_LIMIT} Minutes!__",
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
