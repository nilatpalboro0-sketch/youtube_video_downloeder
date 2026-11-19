"""Simple interactive YouTube video downloader."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yt_dlp


ROOT = Path(__file__).resolve().parent
DOWNLOADS = ROOT / "downloads"
ARCHIVE = DOWNLOADS / "archive.txt"
COOKIES_FILE = ROOT / "cookies.txt"


def find_ffmpeg() -> str | None:
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    try:
        import imageio_ffmpeg

        bundled = Path(imageio_ffmpeg.get_ffmpeg_exe())
        return str(bundled) if bundled.exists() else None
    except Exception:
        return None


def get_url(command_line_url: str | None) -> str:
    if command_line_url:
        return command_line_url.strip()

    print("YouTube Video Downloader")
    print("------------------------")
    try:
        return input("Paste a YouTube URL: ").strip()
    except EOFError:
        # stdin is not available (e.g. redirected input ended).
        return ""


def is_single_video_url(url: str) -> bool:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "v" in query:
        return True
    if parsed.netloc.lower() in {"youtu.be", "www.youtu.be"}:
        return bool(parsed.path.strip("/"))
    return any(
        parsed.path.lower().startswith(prefix)
        for prefix in ("/shorts/", "/embed/", "/live/")
    )


def download(url: str) -> int:
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg()

    options = {
        "outtmpl": str(DOWNLOADS / "%(title)s [%(id)s].%(ext)s"),
        "download_archive": str(ARCHIVE),
        # YouTube often adds an automatic Mix playlist to video URLs.
        # This application downloads one video, not the whole Mix.
        "noplaylist": True,
        "ignoreerrors": False,
        "continuedl": True,
        "retries": 5,
        "fragment_retries": 5,
        "socket_timeout": 30,
        "windowsfilenames": os.name == "nt",
        "noprogress": False,
        "quiet": False,
        # yt-dlp only enables deno by default. Enable every supported
        # runtime so Node.js (if installed) can solve YouTube's JS
        # challenges; runtimes that are not installed are ignored.
        "js_runtimes": {"deno": {}, "node": {}, "bun": {}, "quickjs": {}},
    }

    # Optional login cookies. If cookies.txt is in the project folder, yt-dlp
    # uses it automatically. This avoids Chrome's locked cookie database.
    if COOKIES_FILE.is_file():
        options["cookiefile"] = str(COOKIES_FILE)
        print(f"Using cookies from: {COOKIES_FILE}")

    if ffmpeg:
        options["format"] = "bv*+ba/b"
        options["merge_output_format"] = "mp4"
        options["ffmpeg_location"] = ffmpeg
    else:
        print("Warning: ffmpeg was not found; using a single-file format.")
        options["format"] = "b"

    print(f"\nDownloading to: {DOWNLOADS}\n")

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.download([url])
    except Exception as error:
        message = str(error)
        lower_msg = message.lower()
        print(f"\nDownload failed: {message}")
        if "not a bot" in lower_msg or "sign in to confirm" in lower_msg:
            print(
                "\nYouTube requires a signed-in session to download this video."
            )
            if not COOKIES_FILE.is_file():
                print(
                    "Fix: export YouTube cookies as a Netscape cookies.txt file "
                    "and save it here:"
                )
                print(f"  {COOKIES_FILE}")
                print("See README.md for the cookie export steps.")
            else:
                print(
                    "The cookies.txt file may be expired. Export a fresh copy "
                    "from a browser that is signed in to YouTube."
                )
        elif "403" in lower_msg or "forbidden" in lower_msg or "429" in lower_msg:
            print(
                "\nYouTube blocked this request (403/429 error). "
                "This often happens with automated downloads."
            )
            if not COOKIES_FILE.is_file():
                print(
                    "Fix: export YouTube cookies as a Netscape cookies.txt file "
                    "and save it here:"
                )
                print(f"  {COOKIES_FILE}")
                print("See README.md for the cookie export steps.")
            else:
                print(
                    "The cookies.txt file may be expired. Export a fresh copy "
                    "from a browser that is signed in to YouTube."
                )
        elif "cookie" in lower_msg or "database" in lower_msg:
            print(
                "\nChrome cookies could not be read. Close Chrome completely "
                "and try again."
            )
        else:
            print("\nCheck the URL and your internet connection, then try again.")
        return 1

    if result:
        print("\nThe download finished with an error.")
        return 1

    print("\nDownload complete.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a single YouTube video to the downloads folder."
    )
    parser.add_argument(
        "--url",
        help="YouTube URL. If omitted, the program asks for one.",
    )
    args = parser.parse_args()

    url = get_url(args.url)
    if not url:
        print("No URL was entered.")
        return 1
    if not is_single_video_url(url):
        print("\nPlease paste a single-video YouTube link.")
        print("It should contain watch?v=VIDEO_ID or look like youtu.be/VIDEO_ID.")
        print("A playlist link does not identify one particular video.")
        return 1

    return download(url)


if __name__ == "__main__":
    sys.exit(main())
