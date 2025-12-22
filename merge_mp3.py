#!/usr/bin/env python3
"""
Tonie MP3 Merger Script
Merges multiple MP3 files into a single file and optionally embeds cover artwork.
"""

import argparse
import os
import sys
from pathlib import Path


def merge_mp3_files(input_files, output_file, cover_art=None):
    """
    Merge multiple MP3 files into a single MP3 file.
    
    Args:
        input_files: List of input MP3 file paths
        output_file: Path to the output merged MP3 file
        cover_art: Optional path to cover art image file
    """
    try:
        from pydub import AudioSegment
    except ImportError:
        print("Error: pydub is not installed. Install it with: pip install pydub")
        sys.exit(1)
    
    # Validate input files
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            sys.exit(1)
        if not input_file.lower().endswith('.mp3'):
            print(f"Warning: {input_file} may not be an MP3 file")
    
    print(f"Merging {len(input_files)} MP3 files...")
    
    # Load and merge MP3 files
    combined = AudioSegment.empty()
    for i, input_file in enumerate(input_files, 1):
        print(f"  [{i}/{len(input_files)}] Loading: {input_file}")
        audio = AudioSegment.from_mp3(input_file)
        combined += audio
    
    # Export the merged file
    print(f"Exporting merged file to: {output_file}")
    combined.export(output_file, format="mp3")
    
    # Embed cover art if provided
    if cover_art:
        embed_cover_art(output_file, cover_art)
    
    print(f"✓ Successfully merged {len(input_files)} files into {output_file}")
    duration_seconds = len(combined) / 1000
    print(f"  Total duration: {duration_seconds:.2f} seconds ({duration_seconds/60:.2f} minutes)")


def embed_cover_art(mp3_file, cover_art_file):
    """
    Embed cover artwork into an MP3 file.
    
    Args:
        mp3_file: Path to the MP3 file
        cover_art_file: Path to the cover art image file
    """
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC
    except ImportError:
        print("Error: mutagen is not installed. Install it with: pip install mutagen")
        sys.exit(1)
    
    if not os.path.exists(cover_art_file):
        print(f"Error: Cover art file not found: {cover_art_file}")
        sys.exit(1)
    
    print(f"Embedding cover art: {cover_art_file}")
    
    # Determine image MIME type
    cover_ext = os.path.splitext(cover_art_file)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
    }
    mime_type = mime_types.get(cover_ext, 'image/jpeg')
    
    # Load the MP3 file
    audio = MP3(mp3_file, ID3=ID3)
    
    # Add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except Exception:
        pass  # Tags already exist
    
    # Read cover art file
    with open(cover_art_file, 'rb') as img:
        cover_data = img.read()
    
    # Embed the cover art
    audio.tags.add(
        APIC(
            encoding=3,  # UTF-8
            mime=mime_type,
            type=3,  # Cover (front)
            desc='Cover',
            data=cover_data
        )
    )
    
    # Save the file
    audio.save()
    print("✓ Cover art embedded successfully")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Merge multiple MP3 files into a single file and optionally embed cover artwork.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge multiple MP3 files
  python merge_mp3.py file1.mp3 file2.mp3 file3.mp3 -o output.mp3
  
  # Merge MP3 files with cover art
  python merge_mp3.py *.mp3 -o merged.mp3 -c cover.jpg
  
  # Merge all MP3 files in a directory
  python merge_mp3.py /path/to/files/*.mp3 -o result.mp3
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input MP3 files to merge'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output merged MP3 file path'
    )
    
    parser.add_argument(
        '-c', '--cover',
        help='Cover art image file (JPEG or PNG)'
    )
    
    args = parser.parse_args()
    
    # Ensure output has .mp3 extension
    if not args.output.lower().endswith('.mp3'):
        args.output += '.mp3'
    
    # Merge the files
    merge_mp3_files(args.input_files, args.output, args.cover)


if __name__ == '__main__':
    main()
