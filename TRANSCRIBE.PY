import whisper

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    
    print("\nTranscription Result:")
    print(result["text"])
    return result

if __name__ == "__main__":
    audio_file = "audio/sample_audio.wav"
    transcribe(audio_file)