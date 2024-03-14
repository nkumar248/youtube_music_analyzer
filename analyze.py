import yt_dlp
import madmom
import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def get_wav_from_url(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
    }

    # Download audio to the current working directory
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            raise Exception("Download failed.") from e  


def extract_chords(path_to_wav_file: str):
    proc = madmom.features.chords.CNNChordFeatureProcessor()
    features = proc(path_to_wav_file)

    decode = madmom.features.chords.CRFChordRecognitionProcessor()
    chords = decode(features)

    return chords


def visualize_chords(chords: list, min_time: int, max_time: int):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Building the y_ticks dictionary from the chord_mapping for proper y-axis labels
    chord_mapping = {
        "N": 0,  # Placeholder for "no chord" or silence
        "C": 1,
        "C#": 2, "Db": 2,
        "D": 3,
        "D#": 4, "Eb": 4,
        "E": 5,
        "F": 6,
        "F#": 7, "Gb": 7,
        "G": 8,
        "G#": 9, "Ab": 9,
        "A": 10,
        "A#": 11, "Bb": 11,
        "B": 12
    }

    # Reverse map for y_ticks labels
    y_ticks = {}
    for chord, position in chord_mapping.items():
        y_ticks[position] = chord

    filtered_chords = [chord for chord in chords if chord[0] >= min_time and chord[1] <= max_time]

    # Loop through each chord to plot it
    for start, end, chord_str in filtered_chords:
        if chord_str == "N":
            chord_root = "N"
            chord_type = "None"
        else:
            chord_root, chord_type = chord_str.split(":")  

        y = chord_mapping.get(chord_root, 0)

        width = end - start
        
        if chord_type == "maj":
            facecolor = 'orange'
        elif chord_type == "min":
            facecolor = 'blue'
        else:
            facecolor = 'none'

        rect = patches.Rectangle((start, y - 0.4), width, 0.8, linewidth=1, edgecolor='r', facecolor=facecolor)
        ax.add_patch(rect)

        ax.text(start + width / 2, y, chord_root, ha='center', va='center', color='black', fontsize=8)


    plt.yticks(list(y_ticks.keys()), list(y_ticks.values()))
    plt.xticks(range(min_time, max_time + 1)) 
    plt.xlim(min_time, max_time)
    plt.xlabel('Time (s)')
    plt.ylabel('Chord')
    plt.title('Chord Progression Over Time')
    plt.show()


def main():
    print("analyze.py is running.")

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--youtube-url", required=True, help="Youtube link to audio to be analyzed")
    parser.add_argument("--min-time", default=0, help="Specify time frame using min / max")
    parser.add_argument("--max-time", default=60, help="Specify time frame using min / max")
    args = parser.parse_args()

    # Get audio file from YouTube
    print("Start download from YouTube.")
    get_wav_from_url(args.youtube_url)
    print("Download complete.")

    # Analyze chords using madmom
    chords = extract_chords('downloaded_audio.wav')
    assert str(args.min_time).isdigit() and str(args.max_time).isdigit()
    visualize_chords(chords, int(args.min_time), int(args.max_time))

    # Delete audio file
    if os.path.exists('downloaded_audio.wav'):
        os.remove('downloaded_audio.wav')
        print("Deleted downloaded wav. Analysis successful.")


if __name__ == "__main__":
    main()
