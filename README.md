# Audio to Text Converter

This tool extracts audio from a video file, processes the audio to enhance its quality, splits it into smaller chunks, and then transcribes the audio into text using Whisper. The transcription is then saved to a text file. This tool can be particularly useful for transcribing interviews, lectures, podcasts, or any audio within video files.

## Features
- **Extracts Audio from Video Files**: Converts audio from video formats (MP4, MKV, etc.) into a WAV format.
- **Audio Preprocessing**: Enhances audio quality by normalizing, reducing noise, and converting to mono to improve transcription accuracy.
- **Dynamic Audio Splitting**: Splits audio based on silence periods, making it easier to handle long recordings.
- **Parallel Transcription**: Uses the Whisper model for transcribing chunks of audio in parallel, significantly improving transcription speed.
- **Temporary File Cleanup**: Automatically deletes temporary audio files after transcription to keep your system clean.

## Requirements
Before running the tool, make sure you have the following installed:

- Python 3.7+
- **FFmpeg**: Required for extracting audio from video files. Follow the instructions on the [FFmpeg website](https://ffmpeg.org/download.html) to install it.
- you can take help from this youtube to install ffmpeg https://www.youtube.com/watch?v=4jx2_j5Seew.
### Installing Dependencies
You can install all the required Python dependencies by running:
pip install -r requirements.txt
This will install all the necessary libraries, including:
1. **moviepy**
2. **pydub**
3. **speech_recognition**
4. **noisereduce**
5. **whisper**

## How to Use
1. Clone or download this repository to your local machine.
2. Ensure that you have Python 3.7+ installed and that all dependencies are installed by running pip install -r requirements.txt.
3. Run the script:
python audio_to_text_converter.py
You will be prompted to input the path to your video file. For example:
Enter the path to your video file (e.g., 'video.mp4'): /path/to/your/video.mp4

The script will extract the audio, preprocess it, split it into smaller chunks, and transcribe each chunk using Whisper. After the transcription is complete, the resulting text will be saved as extracted_text.txt.

Check the directory for the extracted_text.txt file, which contains the full transcription.

## How It Works
1. **Extract Audio**: The tool uses moviepy to extract audio from the video and saves it as a temporary WAV file.
2. **Preprocess Audio**: The audio is then processed using pydub to normalize the volume, reduce noise with noisereduce, and convert the audio to mono for better transcription accuracy.
3. **Split Audio**: The audio is split into smaller chunks based on silence using pydub.silence.split_on_silence. This helps improve the accuracy of the transcription.
4. **Transcribe Audio**: Each chunk is transcribed in parallel using Whisper, a powerful transcription model.
5. **Save Transcription**: The transcriptions are combined into a single string and saved as a text file.

## Troubleshooting
Error: 
1. **File Not Found**: If you receive a "File not found" error, ensure that the path to your video file is correct and that the file exists.
2. **No Audio Extracted**: If the tool fails to extract audio, make sure you have ffmpeg properly installed as it is required by moviepy.
3. **Slow Transcription**: If transcription takes too long, ensure that your system has sufficient CPU resources. The script transcribes in parallel using all available CPU cores.

## Contributing
Feel free to open issues or submit pull requests if you have improvements or bug fixes. Contributions are always welcome!

## Acknowledgments
The Whisper model used in this tool is developed by OpenAI and is known for its high accuracy in speech-to-text transcription.
Thanks to moviepy, pydub, and noisereduce for providing the powerful libraries used in audio processing.
