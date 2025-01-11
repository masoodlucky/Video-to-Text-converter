import moviepy as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.silence import split_on_silence
import os
from multiprocessing import Pool, cpu_count
import noisereduce as nr
import whisper
from datetime import datetime

# Initialize the Whisper model
model = whisper.load_model("base")  # Use "small", "medium", or "large" as needed

def log_message(message):
    """Log messages with timestamps for better debugging."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def extract_audio(video_path):
    """Extract audio from video and save as a WAV file."""
    log_message("Extracting audio from video...")
    audio_path = "temp_audio.wav"
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec="pcm_s16le")
    except Exception as e:
        raise RuntimeError(f"Failed to extract audio: {e}")
    return audio_path

def preprocess_audio(audio_path):
    """Enhance audio quality by normalizing, reducing noise, and converting to mono."""
    log_message("Enhancing audio quality...")
    try:
        audio = AudioSegment.from_wav(audio_path)
        audio = audio.set_channels(1)  # Convert to mono
        audio = normalize(audio)  # Normalize audio
        
        # Reduce noise
        samples = audio.get_array_of_samples()
        samples = nr.reduce_noise(y=samples, sr=audio.frame_rate)
        cleaned_path = "cleaned_audio.wav"
        audio = audio._spawn(samples)
        audio.export(cleaned_path, format="wav")
    except Exception as e:
        raise RuntimeError(f"Audio preprocessing failed: {e}")
    
    return cleaned_path

def calculate_silence_threshold(audio_path):
    """Dynamically calculate silence threshold."""
    audio = AudioSegment.from_wav(audio_path)
    return audio.dBFS - 14

def split_audio(audio_path, min_silence_len=700, silence_thresh=None, keep_silence=300):
    """Split audio into smaller chunks based on silence."""
    log_message("Splitting audio into smaller chunks...")
    audio = AudioSegment.from_wav(audio_path)
    
    if silence_thresh is None:
        silence_thresh = calculate_silence_threshold(audio_path)
    
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        if len(chunk) > 1000:  # Ensure chunk is at least 1 second long
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)
            log_message(f"Chunk {i + 1}: {len(chunk) / 1000:.2f} seconds")
    
    return chunk_paths

def transcribe_chunk_whisper(chunk_path):
    """Transcribe a single audio chunk using Whisper."""
    log_message(f"Transcribing {chunk_path} with Whisper...")
    try:
        result = model.transcribe(chunk_path)
        return result["text"].strip()
    except Exception as e:
        log_message(f"Failed to transcribe {chunk_path}: {e}")
        return ""

def transcribe_audio_chunks_parallel(chunk_paths):
    """Transcribe audio chunks in parallel using Whisper."""
    log_message("Transcribing audio chunks in parallel...")
    with Pool(cpu_count()) as pool:
        results = pool.map(transcribe_chunk_whisper, chunk_paths)
    return ' '.join(results)  # Combine all transcriptions into one string

def cleanup_temp_files():
    """Delete temporary files to clean up the directory."""
    log_message("Cleaning up temporary files...")
    temp_files = [f for f in os.listdir() if f.startswith("temp_") or f.startswith("chunk_") or f == "cleaned_audio.wav"]
    for file in temp_files:
        try:
            os.remove(file)
            log_message(f"Deleted {file}")
        except Exception as e:
            log_message(f"Failed to delete {file}: {e}")

def main():
    try:
        # Ask for video file input
        video_path = input("Enter the path to your video file (e.g., 'video.mp4'): ").strip()
        if not os.path.exists(video_path):
            log_message("Error: File not found. Please provide a valid path.")
            return
        
        # Extract and preprocess audio
        audio_path = extract_audio(video_path)
        cleaned_audio_path = preprocess_audio(audio_path)
        
        # Split and transcribe audio
        chunk_paths = split_audio(cleaned_audio_path)
        transcribed_text = transcribe_audio_chunks_parallel(chunk_paths)
        
        # Save the final text
        output_path = "extracted_text.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        log_message(f"Transcription complete! Text saved to {output_path}")
    
    except Exception as e:
        log_message(f"An error occurred: {e}")
    
    finally:
        # Clean up temporary files
        cleanup_temp_files()

# Run the program
if __name__ == "__main__":
    main()
