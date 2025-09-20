import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import os

st.title("🎬 YouTube Downloader & Transcript App")

url = st.text_input("Enter YouTube Video URL:")

video_file = "downloaded_video.mp4"
audio_file = "downloaded_audio.mp3"

# --- Video Download ---
if st.button("⬇️ Download Video"):
    if url:
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': video_file
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("✅ Video downloaded successfully with audio!")
        except Exception as e:
            st.error(f" Error: {e}")
    else:
        st.warning(" Please enter a valid YouTube URL")

# --- Audio Download ---
if st.button("🎵 Download Audio"):
    if url:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': audio_file
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("✅ Audio downloaded successfully!")
        except Exception as e:
            st.error(f" Error: {e}")
    else:
        st.warning(" Please enter a valid YouTube URL")

# --- Transcript ---
if st.checkbox("Show Transcript (if available)"):
    if url:
        try:
            if "v=" in url:
                video_id = url.split("v=")[-1].split("&")[0]
            elif "shorts/" in url:
                video_id = url.split("shorts/")[-1].split("?")[0]
            else:
                video_id = url.split("/")[-1]

            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
            text = " ".join([t['text'] for t in transcript])
            st.text_area("Transcript:", text, height=300)
        except Exception:
            st.error("❌ Transcript not available.")

# --- Save Buttons ---
if os.path.exists(video_file):
    with open(video_file, "rb") as f:
        st.download_button("⬇️ Save Video to My PC", f, file_name="video.mp4")

if os.path.exists(audio_file):
    with open(audio_file, "rb") as f:
        st.download_button("⬇️ Save Audio to My PC", f, file_name="audio.mp3")
