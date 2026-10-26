
from datetime import timedelta
import os
import subprocess

import streamlit as st
import whisper
import srt
from moviepy.editor import VideoFileClip


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

FFMPEG_EXE = r"C:\Users\konje\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"

MODEL_NAME = "base"

LANGUAGES = {
    "Auto-detect": None,
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Korean": "ko",
    "Arabic": "ar",
    "Turkish": "tr",
    "Dutch": "nl",
    "Indonesian": "id",
    "Thai": "th",
    "Vietnamese": "vi",
    "Polish": "pl",
    "Ukrainian": "uk",
    "Swedish": "sv",
    "Finnish": "fi",
    "Greek": "el",
    "Hebrew": "he",
    "Czech": "cs",
    "Danish": "da",
    "Norwegian": "no",
    "Romanian": "ro",
    "Hungarian": "hu",
    "Persian": "fa",
    "Swahili": "sw",
}


# --------------------------------------------------
# WHISPER MODEL
# Load the model once and reuse it between reruns.
# --------------------------------------------------

@st.cache_resource
def load_whisper_model():
    return whisper.load_model(MODEL_NAME)


# --------------------------------------------------
# STEP 1: EXTRACT AUDIO
# --------------------------------------------------

def extract_audio(video_path, output_audio_path):
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    video = VideoFileClip(video_path)

    try:
        audio = video.audio

        if audio is None:
            raise ValueError("No audio track found in this video.")

        audio.write_audiofile(
            output_audio_path,
            logger=None
        )
    finally:
        video.close()


# --------------------------------------------------
# STEP 2: TRANSCRIBE OR TRANSLATE
# --------------------------------------------------

def transcribe(audio_path, language=None, task="transcribe"):
    model = load_whisper_model()

    options = {
        "task": task,
        "verbose": False,
    }

    # None means Whisper automatically detects the language.
    if language is not None:
        options["language"] = language

    result = model.transcribe(audio_path, **options)

    return result


# --------------------------------------------------
# STEP 3: CONVERT WHISPER SEGMENTS TO SRT
# --------------------------------------------------

def convert_to_srt(transcription_result):
    subtitles = []

    for i, segment in enumerate(
        transcription_result["segments"]
    ):
        start = timedelta(seconds=segment["start"])
        end = timedelta(seconds=segment["end"])
        text = segment["text"].strip()

        if not text:
            continue

        subtitles.append(
            srt.Subtitle(
                index=len(subtitles) + 1,
                start=start,
                end=end,
                content=text
            )
        )

    return srt.compose(subtitles)


# --------------------------------------------------
# STEP 4: BURN SUBTITLES INTO VIDEO USING FFMPEG
# --------------------------------------------------

def burn_subtitles(video_path, srt_path, output_path):
    video_full = os.path.abspath(video_path)
    srt_full = os.path.abspath(srt_path)
    output_full = os.path.abspath(output_path)

    if not os.path.isfile(FFMPEG_EXE):
        raise FileNotFoundError(
            "FFmpeg executable was not found. Check FFMPEG_EXE."
        )

    if not os.path.isfile(srt_full):
        raise FileNotFoundError(
            f"Subtitle file was not found: {srt_full}"
        )

    # Escape special characters for the FFmpeg subtitles filter.
    subtitle_filter_path = (
        srt_full.replace("\\", "/")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace(",", r"\,")
        .replace("[", r"\[")
        .replace("]", r"\]")
    )

    command = [
        FFMPEG_EXE,
        "-y",
        "-i", video_full,
        "-vf", f"subtitles='{subtitle_filter_path}'",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        output_full,
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


# --------------------------------------------------
# STREAMLIT USER INTERFACE
# --------------------------------------------------

st.set_page_config(
    page_title="AI Video Caption Generator",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI-Powered Video Caption Generator")

st.write(
    "Generate subtitles from videos in multiple languages "
    "or translate spoken audio into English subtitles."
)

uploaded_file = st.file_uploader(
    "Upload a video",
    type=["mp4", "mov", "avi", "mkv", "webm"],
)

st.subheader("Caption Settings")

language_names = list(LANGUAGES.keys())

selected_language = st.selectbox(
    "Spoken language",
    language_names,
    index=0,
    help=(
        "Choose Auto-detect to let Whisper identify the spoken "
        "language, or select a language to guide recognition."
    ),
)

caption_mode = st.radio(
    "Subtitle output",
    [
        "Original spoken language",
        "Translate into English",
    ],
    horizontal=True,
)

st.caption(
    "English translation uses Whisper's built-in translation "
    "task. Original-language mode keeps the speech in its "
    "original language."
)


if uploaded_file is not None:
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("captions", exist_ok=True)

    # Use a stable filename rather than trusting an uploaded path.
    extension = os.path.splitext(uploaded_file.name)[1].lower()
    input_video_path = os.path.join(
        "videos", "uploaded_video" + extension
    )

    with open(input_video_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    st.video(input_video_path)

    if st.button("Generate Captions", type="primary"):
        try:
            # Step 1: Extract audio
            st.info("Step 1/4: Extracting audio...")

            audio_path = os.path.join(
                "audio", "temp_audio.wav"
            )

            extract_audio(
                input_video_path,
                audio_path,
            )

            # Step 2: Transcribe or translate
            st.info(
                "Step 2/4: Processing speech with Whisper..."
            )

            language_code = LANGUAGES[selected_language]

            # Translation output is always English.
            task = (
                "translate"
                if caption_mode == "Translate into English"
                else "transcribe"
            )

            # For translation, provide the selected spoken language
            # when known. Auto-detection is used otherwise.
            with st.spinner(
                "Loading AI model and processing audio..."
            ):
                result = transcribe(
                    audio_path,
                    language=language_code,
                    task=task,
                )

            detected_code = result.get("language")

            detected_name = next(
                (
                    name
                    for name, code in LANGUAGES.items()
                    if code == detected_code
                ),
                detected_code or "Unknown",
            )

            st.success(
                f"Detected spoken language: {detected_name}"
            )

            st.subheader("Transcription / Translation")
            st.write(result["text"])

            # Step 3: Generate SRT
            st.info("Step 3/4: Generating subtitle file...")

            srt_content = convert_to_srt(result)

            output_srt_path = os.path.join(
                "captions", "output.srt"
            )

            with open(
                output_srt_path,
                "w",
                encoding="utf-8-sig",
                newline="",
            ) as file:
                file.write(srt_content)

            st.download_button(
                label="Download SRT Subtitles",
                data=srt_content.encode("utf-8-sig"),
                file_name="captions.srt",
                mime="application/x-subrip",
            )

            # Step 4: Burn subtitles into video
            st.info("Step 4/4: Rendering captioned video...")

            output_video_path = os.path.join(
                "videos", "captioned_output.mp4"
            )

            with st.spinner(
                "Burning subtitles into video. This may take a while..."
            ):
                burn_subtitles(
                    input_video_path,
                    output_srt_path,
                    output_video_path,
                )

            st.success("Captioned video generated successfully!")

            st.subheader("Preview")
            st.video(output_video_path)

            with open(output_video_path, "rb") as file:
                st.download_button(
                    label="Download Captioned Video",
                    data=file,
                    file_name="captioned_video.mp4",
                    mime="video/mp4",
                )

        except subprocess.CalledProcessError as error:
            st.error(
                "FFmpeg failed while rendering the video. "
                "Check the error details below."
            )

            if error.stderr:
                st.code(error.stderr[-5000:])

        except Exception as error:
            st.error(
                f"Caption generation failed: {error}"
            )
