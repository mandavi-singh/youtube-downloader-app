import streamlit as st
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import os


FFMPEG_PATH = r"C:\Users\singh\Downloads\ffmpeg\ffmpeg\bin\ffmpeg.exe"
# -----------------------------

st.set_page_config(page_title="YouTube Downloader & Transcript", layout="centered")
st.markdown("<h1 style='text-align:center'>🎬 YouTube Downloader & Transcript App</h1>", unsafe_allow_html=True)

st.write("Enter a YouTube URL to download video, audio, or view transcript.")

url = st.text_input("YouTube Video URL:")

st.markdown("---")

# ----------------------------- VIDEO DOWNLOAD -----------------------------
st.subheader("📹 Video Download (MP4 with audio)")
if st.button("⬇️ Download Video (MP4)"):
    if url:
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'downloaded_video.mp4',
                'merge_output_format': 'mp4',
                'ffmpeg_location': FFMPEG_PATH
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("✅ Video downloaded successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL")

# Download button for saved video
if os.path.exists("downloaded_video.mp4"):
    with open("downloaded_video.mp4", "rb") as f:
        st.download_button("💾 Save Video to Device", f, file_name="video.mp4")

st.markdown("---")

# ----------------------------- AUDIO DOWNLOAD -----------------------------
st.subheader("🎵 Audio Download (MP3)")
if st.button("⬇️ Download Audio (MP3)"):
    if url:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded_audio.mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': FFMPEG_PATH
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("✅ Audio downloaded successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL")

# Download button for saved audio
if os.path.exists("downloaded_audio.mp3"):
    with open("downloaded_audio.mp3", "rb") as f:
        st.download_button("💾 Save Audio to Device", f, file_name="audio.mp3")

st.markdown("---")

# ----------------------------- TRANSCRIPT -----------------------------
st.subheader("📝 Transcript (Optional)")
if st.checkbox("Show Transcript"):
    if url:
        try:
            # extract video ID from URL
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
            st.error("❌ Transcript not available or error occurred.")
