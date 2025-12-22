# Tonie Studio

A comprehensive workflow dashboard and tools for preparing audio files for Tonie devices. This project provides a two-step process to merge multiple MP3 files and convert them to the Tonie-compatible format.

## Overview

Tonie Studio simplifies the process of creating custom audio content for Tonie devices by providing:

1. **Python MP3 Merger Script** - Merges multiple MP3 files into a single file with optional cover artwork embedding
2. **Docker-based Conversion** - Converts merged MP3 files to Tonie-compatible format specifications
3. **Interactive Dashboard** - Web-based interface with copyable commands and workflow guidance

## Features

- ✅ Merge multiple MP3 files into a single file
- ✅ Embed cover artwork (JPEG/PNG) into MP3 files
- ✅ Convert audio to Tonie format specifications (48kHz, stereo, 128k bitrate)
- ✅ User-friendly HTML dashboard with copyable commands
- ✅ Cross-platform support (Linux, Mac, Windows)
- ✅ Complete workflow automation scripts

## Quick Start

### Prerequisites

1. **Python 3.x** with pip installed
2. **Docker** installed and running
3. **ffmpeg** installed on your system (required by pydub)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/soenkebruns/tonie-studio.git
cd tonie-studio
```

2. Install Python dependencies:
```bash
pip install pydub mutagen
```

3. Pull the Docker image:
```bash
docker pull ghcr.io/soenkebruns/tonie-podcast-sync:main
```

## Usage

### Method 1: Using the Dashboard (Recommended)

Open `tonie_manager.html` in your web browser for an interactive workflow dashboard with copyable commands for each step.

### Method 2: Command Line

#### Step 1: Merge MP3 Files

Basic merge:
```bash
python merge_mp3.py file1.mp3 file2.mp3 file3.mp3 -o output.mp3
```

Merge with cover art:
```bash
python merge_mp3.py *.mp3 -o merged.mp3 -c cover.jpg
```

Merge all MP3s in a directory:
```bash
python merge_mp3.py /path/to/files/*.mp3 -o result.mp3 -c artwork.png
```

#### Step 2: Convert to Tonie Format

Linux/Mac:
```bash
docker run --rm -v $(pwd):/data ghcr.io/soenkebruns/tonie-podcast-sync:main ffmpeg -i /data/merged.mp3 -ar 48000 -ac 2 -b:a 128k /data/tonie_output.mp3
```

Windows PowerShell:
```powershell
docker run --rm -v ${PWD}:/data ghcr.io/soenkebruns/tonie-podcast-sync:main ffmpeg -i /data/merged.mp3 -ar 48000 -ac 2 -b:a 128k /data/tonie_output.mp3
```

Windows CMD:
```cmd
docker run --rm -v %cd%:/data ghcr.io/soenkebruns/tonie-podcast-sync:main ffmpeg -i /data/merged.mp3 -ar 48000 -ac 2 -b:a 128k /data/tonie_output.mp3
```

### Method 3: Automated Workflow Script

Create a bash script (Linux/Mac) `tonie_workflow.sh`:
```bash
#!/bin/bash
# Tonie Workflow - Complete Script

# Step 1: Merge MP3 files
echo "Step 1: Merging MP3 files..."
python merge_mp3.py *.mp3 -o merged.mp3 -c cover.jpg

# Step 2: Convert to Tonie format
echo "Step 2: Converting to Tonie format..."
docker run --rm -v $(pwd):/data ghcr.io/soenkebruns/tonie-podcast-sync:main ffmpeg -i /data/merged.mp3 -ar 48000 -ac 2 -b:a 128k /data/tonie_output.mp3

echo "✓ Complete! Your Tonie file is ready: tonie_output.mp3"
```

Make it executable and run:
```bash
chmod +x tonie_workflow.sh
./tonie_workflow.sh
```

## Workflow Details

### Two-Step Process

1. **Python Merging (Step 1)**
   - Combines multiple MP3 files sequentially
   - Optionally embeds cover artwork into the merged file
   - Uses `pydub` for audio manipulation and `mutagen` for metadata
   - Supports JPEG and PNG cover art formats

2. **Docker Conversion (Step 2)**
   - Converts the merged MP3 to Tonie specifications
   - Uses ffmpeg within the tonie-podcast-sync Docker container
   - Output format: 48kHz sample rate, stereo, 128k bitrate
   - Ensures compatibility with Tonie devices

### File Structure

```
tonie-studio/
├── README.md              # This file - comprehensive documentation
├── merge_mp3.py          # Python script for merging MP3 files
├── tonie_manager.html    # Interactive workflow dashboard
└── (your MP3 files and cover art)
```

## Dependencies

### Python Packages

- **pydub** - Audio file manipulation and merging
- **mutagen** - MP3 metadata and cover art embedding

Install with:
```bash
pip install pydub mutagen
```

### System Requirements

- **ffmpeg** - Required by pydub for audio processing
  - Linux: `sudo apt-get install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

- **Docker** - For the conversion step
  - Download from [docker.com](https://www.docker.com/get-started)

## Command Line Options

### merge_mp3.py

```
usage: merge_mp3.py [-h] -o OUTPUT [-c COVER] input_files [input_files ...]

Merge multiple MP3 files into a single file and optionally embed cover artwork.

positional arguments:
  input_files           Input MP3 files to merge

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output merged MP3 file path
  -c COVER, --cover COVER
                        Cover art image file (JPEG or PNG)
```

## Examples

### Example 1: Simple Merge
```bash
python merge_mp3.py chapter1.mp3 chapter2.mp3 chapter3.mp3 -o audiobook.mp3
```

### Example 2: Merge with Cover Art
```bash
python merge_mp3.py episode*.mp3 -o podcast_season1.mp3 -c podcast_cover.jpg
```

### Example 3: Complete Workflow
```bash
# Merge all MP3 files with cover art
python merge_mp3.py *.mp3 -o merged.mp3 -c cover.png

# Convert to Tonie format
docker run --rm -v $(pwd):/data ghcr.io/soenkebruns/tonie-podcast-sync:main ffmpeg -i /data/merged.mp3 -ar 48000 -ac 2 -b:a 128k /data/tonie_ready.mp3
```

## Troubleshooting

### Common Issues

**Issue: "pydub is not installed"**
```bash
pip install pydub mutagen
```

**Issue: "ffmpeg not found"**
- Install ffmpeg on your system (see Dependencies section)

**Issue: "Docker command not found"**
- Ensure Docker is installed and running
- On Linux, you may need to add your user to the docker group: `sudo usermod -aG docker $USER`

**Issue: "Permission denied" on Docker volume mount**
- On Linux/Mac, ensure the directory has appropriate permissions
- Try running Docker command with `sudo` (not recommended for regular use)

### Getting Help

If you encounter issues:
1. Check that all prerequisites are installed
2. Verify ffmpeg is in your system PATH
3. Ensure Docker daemon is running
4. Check file paths are correct and accessible

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for use in preparing audio content for Tonie devices.

## Acknowledgments

- Uses the [tonie-podcast-sync](https://github.com/soenkebruns/tonie-podcast-sync) Docker image for audio conversion
- Built with pydub and mutagen for Python audio processing

## Related Projects

- [tonie-podcast-sync](https://github.com/soenkebruns/tonie-podcast-sync) - Synchronize podcasts to Tonie devices

---

**Note:** This tool is for personal use in preparing audio content for your own Tonie devices. Please respect copyright and licensing when working with audio files.