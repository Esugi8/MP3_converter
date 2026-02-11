import streamlit as st
from moviepy import VideoFileClip
import os
import tempfile

st.title("MKV to MP3 高機能トリマー")

uploaded_file = st.file_uploader("動画ファイルを選択してください", type=["mkv", "mp4", "avi", "mov"])

if uploaded_file:
    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mkv") as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

    with VideoFileClip(video_path) as clip:
        duration = clip.duration
        st.write(f"動画の長さ: {int(duration)} 秒")

        # トリミング範囲の指定
        start_time = st.number_input("開始(秒)", min_value=0.0, max_value=duration, value=0.0)
        end_time = st.number_input("終了(秒)", min_value=0.0, max_value=duration, value=duration)

        if st.button("変換実行"):
            output_path = "output.mp3"
            subclip = clip.subclipped(start_time, end_time) if hasattr(clip, "subclipped") else clip.subclip(start_time, end_time)
            subclip.audio.write_audiofile(output_path)
            
            with open(output_path, "rb") as f:
                st.download_button("MP3をダウンロード", f, file_name="converted.mp3")