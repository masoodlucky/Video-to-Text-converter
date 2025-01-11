# Audio to Text Converter
**This tool extracts audio from a video file, enhances the audio quality, splits it into manageable chunks, and transcribes the audio into text using OpenAI's Whisper model. The resulting text is saved to a file, making this tool ideal for transcribing interviews, lectures, podcasts, or any audio embedded in video files.**

## Features:
1. **Audio Extraction**: Converts audio from video formats (MP4, MKV, etc.) into WAV format.
2. **Audio Enhancement**: Improves quality through normalization, noise reduction, and conversion to mono for better transcription accuracy.
3. **Silence-Based Splitting**: Dynamically splits audio into smaller chunks based on silence, optimizing long audio processing.
4. **Efficient Transcription**: Leverages Whisper to transcribe audio chunks in parallel, accelerating the transcription process.
5. **Automated Cleanup**: Removes temporary files after transcription, maintaining a clutter-free environment.

## Requirements:
Ensure the following are installed before using the tool:
1. ***Python 3.7+***
2. ***FFmpeg***: Required for extracting audio from video files. Download it from the FFmpeg website. You can also follow this YouTube guide for installation assistance.

## Installing Dependencies:
Run the following command to install required Python libraries:
***pip install -r requirements.txt***  
This installs:
**moviepy**
**pydub**
**speech_recognition**
**noisereduce**
**whisper**

## How to Use:
1. Clone or download this repository.
2. Install Python dependencies using pip install -r requirements.txt.
3. Run the script:
python audio_to_text_converter.py  
4. Enter the path to your video file when prompted, e.g.:
Enter the path to your video file (e.g., 'video.mp4'): /path/to/your/video.mp4  
5. The tool processes the video and generates a transcription saved as extracted_text.txt in the working directory.

## How It Works:
1. **Extract Audio**: Audio is extracted from the video using moviepy and saved as a WAV file.
2. **Audio Preprocessing**: The audio is normalized, denoised, and converted to mono using pydub and noisereduce.
3. **Silence Detection & Splitting**: Audio is split into chunks based on silence, improving transcription accuracy.
4. **Transcription**: Whisper transcribes each audio chunk in parallel.
5. **Output**: The transcriptions are combined and saved in extracted_text.txt.

## Troubleshooting:
Common Issues:
1. File Not Found: Verify the video file path and ensure the file exists.
2. Audio Extraction Failure: Ensure FFmpeg is properly installed.
3. Slow Transcription: Check CPU resources. The script uses all available CPU cores for parallel processing.

## Contributing:
Contributions are welcome! Feel free to open issues or submit pull requests for improvements or bug fixes.

## Acknowledgments:
Whisper by OpenAI for its powerful transcription capabilities.
Thanks to moviepy, pydub, and noisereduce for their excellent audio processing libraries.
