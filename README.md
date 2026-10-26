# 🎬 AI-Powered Video Caption Generator

An AI-powered video captioning application that automatically extracts speech from videos, generates timestamped subtitles, and burns captions directly into videos. Built with Python, OpenAI Whisper, Streamlit, MoviePy, and FFmpeg.

## ✨ Features

- **Video Upload:** Supports MP4, MOV, AVI, MKV, and WEBM.
- **Automatic Language Detection:** Detects the spoken language using Whisper.
- **Multilingual Transcription:** Generates subtitles in the original spoken language for supported languages.
- **English Translation:** Translates supported non-English speech into English subtitles.
- **SRT Subtitle Generation:** Creates downloadable subtitle files with timestamps.
- **Burned-in Captions:** Embeds subtitles directly into the output video.
- **Video Preview:** Preview the uploaded video and generated captioned video.
- **Download Options:** Download the SRT subtitle file and final captioned MP4.
- **Model Caching:** Reuses the loaded Whisper model between Streamlit reruns.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| OpenAI Whisper | Speech recognition and English translation |
| Streamlit | Web interface |
| MoviePy | Audio extraction from videos |
| FFmpeg | Video processing and subtitle rendering |
| SRT | Subtitle formatting and generation |
| PyTorch | Deep learning framework used by Whisper |

## 🏗️ Project Workflow

1. Upload a video through the Streamlit interface.
2. Select the spoken language or use automatic detection.
3. Choose original-language subtitles or English translation.
4. Extract audio from the video using MoviePy.
5. Process the audio using the Whisper speech recognition model.
6. Generate timestamped subtitles in SRT format.
7. Burn subtitles into the video using FFmpeg.
8. Preview and download the resulting video and subtitle file.

## 📁 Project Structure

```text
SUBTITLES/
├── app.py
├── extract_audio.py
├── transcribe.py
├── generate_srt.py
├── burn_captions.py
├── videos/
│   ├── uploaded_video.mp4
│   └── captioned_output.mp4
├── audio/
│   └── temp_audio.wav
├── captions/
│   └── output.srt
└── README.md
```

Generated files and filenames may vary depending on the application workflow.

## ⚙️ Requirements

- Python 3.10
- pip
- FFmpeg
- Internet access for the initial Whisper model download
- Sufficient RAM and storage for audio/video processing

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SUBTITLES
```

Replace the placeholder with your actual repository URL.

### 2. Create a Conda environment

```bash
conda create -n capture_caption python=3.10 -y
conda activate capture_caption
```

### 3. Install Python dependencies

```bash
python -m pip install moviepy==1.0.3 openai-whisper srt streamlit
```

Install FFmpeg separately if it is not already available:

```bash
conda install -c conda-forge ffmpeg -y
```

**Windows note:** If FFmpeg is installed separately, update the `FFMPEG_EXE` path in `app.py` to match your system.

### 4. Run the application

From the project directory, execute:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## 🌐 Supported Languages

The application includes language selections such as:

- English
- Telugu
- Hindi
- Tamil
- Kannada
- Malayalam
- Bengali
- Marathi
- Gujarati
- French
- Spanish
- German
- Japanese
- Chinese
- Korean
- Arabic

Whisper supports additional languages. Recognition quality varies by language, accent, audio clarity, and model size.

## 📤 Output Files

| Output | Description |
|---|---|
| `output.srt` | Timestamped subtitle file |
| `captioned_output.mp4` | Video with embedded subtitles |

The actual output paths depend on the application configuration.

## ⚠️ Limitations

- Transcription accuracy depends on audio quality and the selected Whisper model.
- The built-in Whisper translation task translates speech into English; it does not directly translate between arbitrary language pairs.
- Processing time depends on video duration, hardware, and model size.
- FFmpeg must be installed and accessible at the configured executable path.
- The current application uses local processing and saves generated files on the computer running Streamlit.

## 🔮 Future Enhancements

- Direct translation between multiple target languages.
- Subtitle editing and timing adjustment.
- Custom subtitle fonts, colors, and positioning.
- Speaker identification and diarization.
- Batch processing for multiple videos.
- GPU acceleration and improved processing performance.
- Progress tracking and improved error handling.

## 👨‍💻 Author

**Konjeti Sohith**

B.Tech — Computer Science and Engineering, Artificial Intelligence and Machine Learning

GitHub: [konjetisohith](https://github.com/konjetisohith)


