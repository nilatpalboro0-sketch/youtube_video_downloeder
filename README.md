# YouTube Video Downloader

This is a small Windows program. It asks for a YouTube link and saves the
video in the `downloads` folder.

The program downloads **one video only**. If YouTube adds a Mix playlist to the
link, the other recommended videos are ignored.

## Quick start

### Step 1: Install Python

Download Python from <https://www.python.org/downloads/>.

During installation, select:

```text
Add Python to PATH
```

### Step 2: Install Node.js (recommended)

Node.js helps yt-dlp solve YouTube's JavaScript challenges. Without it, the
program may start but YouTube downloads can fail or offer fewer formats.

1. Download the **LTS** version from <https://nodejs.org/>.
2. Run the installer using the default options.
3. Close and reopen Command Prompt so the updated PATH is available.
4. Verify the installation:

```bat
node --version
```

If a version number is displayed, Node.js is installed correctly. The program
automatically detects Node.js; no additional configuration is needed.

### Step 3: Start the program

Double-click:

```text
run.bat
```

The first run automatically:

1. Creates a Python virtual environment.
2. Installs the required packages.
3. Starts the downloader.

The program also detects installed JavaScript runtimes, including Node.js, to
help yt-dlp complete YouTube's JavaScript challenges.

### Step 4: Paste a link

When you see:

```text
Paste a YouTube URL:
```

Paste a single-video YouTube link and press **Enter**.

Use a link like:

```text
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
```

Do not paste a link that only contains `playlist?list=...`. A playlist link
does not identify one particular video.

Your video will be saved here:

```text
downloads\
```

## Dependencies

Dependencies are the programs and Python packages needed by this project.

### Required

- **Windows 10 or newer**
- **Python 3.9 or newer**
- **yt-dlp** — downloads the YouTube video
- **imageio-ffmpeg** — helps combine video and audio

You do not need to install `yt-dlp` or `imageio-ffmpeg` manually. The
`run.bat` file installs them automatically.

The downloader does not automatically read Chrome cookies. New Chrome versions
can lock or protect the cookie database, which causes errors. Most public
videos work without cookies.

### Optional

- **ffmpeg** — improves video and audio quality.
- **Node.js** — helps yt-dlp pass YouTube's JavaScript challenges. Download it
  from <https://nodejs.org/>.

Install ffmpeg from <https://ffmpeg.org/download.html> and add it to the
Windows PATH. The program includes a bundled ffmpeg through `imageio-ffmpeg`,
but a separate installation may provide better compatibility.

## Other ways to run

Start the program and enter the link manually:

```bat
run.bat
```

Or provide the link directly:

```bat
run.bat --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Login cookies (only if YouTube asks)

YouTube sometimes blocks downloads with:

```text
Sign in to confirm you're not a bot
```

To fix this, export your YouTube cookies:

1. Open Chrome and sign in to YouTube.
2. Install the **Get cookies.txt LOCALLY** extension:
   <https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc>
3. Click the extension and choose **Export**.
4. Save the file as `cookies.txt` in this project folder.

The program detects `cookies.txt` automatically. You do not need to change any
settings.

Keep `cookies.txt` private. It contains your YouTube login session, so do not
share it or upload it to GitHub. It is already excluded by `.gitignore`.

## Download folder

Downloaded videos are stored in:

```text
downloads\
```

The file name looks like this:

```text
Video title [video-id].mp4
```

The file `downloads\archive.txt` remembers downloaded videos so the same video
is not downloaded again.

## Project files

| File or folder | What it does |
| --- | --- |
| `main.py` | Asks for the link and downloads the video |
| `run.bat` | Installs dependencies and starts the program |
| `requirements.txt` | Lists the required Python packages |
| `downloads\` | Stores downloaded videos |
| `cookies.txt` | Optional YouTube login file (never upload this) |
| `README.md` | This guide |

## Troubleshooting

### The program does not start

Install Python again and make sure **Add Python to PATH** is selected. Then
close and reopen Command Prompt before running `run.bat`.

### The download fails

First check the displayed error message. YouTube may temporarily block
automated requests with a `403`, `429`, or
`Sign in to confirm you are not a bot` message. If this happens, export a fresh
`cookies.txt` file as described above and try again. Installing Node.js may
also help with YouTube JavaScript challenges.

Private, age-restricted, members-only, and region-blocked videos may not be
available. Make sure you provide a single-video link, not a playlist-only link.

### The video quality is low

Install ffmpeg and add it to the Windows PATH.

## Disclaimer

Download only videos you are allowed to download. Respect YouTube's Terms of
Service, copyright laws, and content creators' rights.
