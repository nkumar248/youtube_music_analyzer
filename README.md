# youtube_music_analyzer (work in progress)

## Description
I wrote a script that downloads a specified audio clip from YouTube using yt-dlp, extracts chord and timing information from the .wav file using madmom and visualizes the information using pyplot. I wrote this script because I was playing guitar and would have liked to know the chord progression of a music clip in a YouTube video. 

## Guide
- Run python analyze.py --youtube-url <youtube \url> --min-time <lower \bound of frame of interest in seconds> --max-time <upper \bound of frame of interest in seconds>
- Visualization shows chord progression over time with orange rectanlges being major chords, blue rectanlges being minor chords and "N" (colorless rectangle) meaning "no chord detected".

## More ideas
- Create a better visualization
- Extract and display more information about the audio
- Create more user-friendly interaction than command-line usage
