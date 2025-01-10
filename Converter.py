import moviepy as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.silence import split_on_silence
import os
from multiprocessing import Pool, cpu_count
import noisereduce as nr
import whisper

model = whisper.load_model("base")

def extract_audio(video_path):
    print("Extracting audio from video...")
    video = mp.VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path, codec="pcm_s16le")
    return audio_path

def preprocess_audio(audio_path):
    print("Enhancing audio quality...")
    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)
    audio = normalize(audio)
    
    samples = audio.get_array_of_samples()
    samples = nr.reduce_noise(y=samples, sr=audio.frame_rate)
    cleaned_path = "cleaned_audio.wav"
    audio = audio._spawn(samples)
    audio.export(cleaned_path, format="wav")
    
    return cleaned_path

def calculate_silence_threshold(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    return audio.dBFS - 14

def split_audio(audio_path, min_silence_len=700, silence_thresh=None, keep_silence=300):
    print("Splitting audio into smaller chunks...")
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
        if len(chunk) > 1000:
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)
            print(f"Chunk {i + 1}: {len(chunk) / 1000:.2f} seconds")
    
    return chunk_paths

def transcribe_chunk_whisper(chunk_path):
    print(f"Transcribing {chunk_path} with Whisper...")
    result = model.transcribe(chunk_path)
    text = result["text"].strip()
    return text

def transcribe_audio_chunks_parallel(chunk_paths):
    print("Transcribing audio chunks in parallel...")
    with Pool(cpu_count()) as pool:
        results = pool.map(transcribe_chunk_whisper, chunk_paths)
    return ' '.join(results)

def cleanup_temp_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def main():
    try:
        video_path = input("Enter the path to your video file (e.g., 'video.mp4'): ").strip()
        if not os.path.exists(video_path):
            print("Error: File not found. Please provide a valid path.")
            return
        
        audio_path = extract_audio(video_path)
        cleaned_audio_path = preprocess_audio(audio_path)
        
        chunk_paths = split_audio(cleaned_audio_path)
        transcribed_text = transcribe_audio_chunks_parallel(chunk_paths)
        
        output_path = "extracted_text.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        print(f"\nTranscription complete! Text saved to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        temp_files = ["temp_audio.wav", "cleaned_audio.wav"] + [f"chunk_{i}.wav" for i in range(1000)]
        cleanup_temp_files(temp_files)

# Run the program
if __name__ == "__main__":
    main()
