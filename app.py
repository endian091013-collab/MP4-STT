import os
import streamlit as st
import whisper
from moviepy.editor import VideoFileClip

# 웹사이트 제목 설정
st.title("🎙️ MP4 음원 STT 텍스트 변환기")
st.write("MP4 파일을 올리면 인공지능이 텍스트로 변환해 줍니다!")

# AI 모델 불러오기 (가장 가벼운 tiny 모델 사용)
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

with st.spinner("AI 모델을 준비하는 중입니다. 잠시만 기다려주세요..."):
    model = load_model()

# 파일 업로드 칸 만들기
uploaded_file = st.file_uploader("MP4 파일을 선택하거나 이곳에 끌어다 놓으세요", type=["mp4", "mp3", "wav"])

if uploaded_file is not None:
    # 업로드된 영상 보여주기
    st.video(uploaded_file)
    
    if st.button("텍스트로 변환하기"):
        with st.spinner("영상의 소리를 추출하고 글자로 변환하고 있어요... (조금 걸릴 수 있어요!)"):
            # 1. 업로드된 파일을 임시로 저장
            temp_video_path = "temp_video.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. MP4에서 오디오(음성)만 추출
            video = VideoFileClip(temp_video_path)
            audio_path = "temp_audio.mp3"
            video.audio.write_audiofile(audio_path)
            video.close()
            
            # 3. Whisper AI로 STT 실행
            result = model.transcribe(audio_path)
            transcribed_text = result["text"]
            
            # 4. 임시 파일 삭제 (정리)
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
        
        st.success("변환 완료!")
        
        # 결과 텍스트 화면에 보여주기
        st.subheader("📝 변환된 텍스트 결과")
        st.text_area("내용을 복사해서 사용하세요", transcribed_text, height=250)
        
        # 다운로드 버튼 제공
        st.download_button(
            label="텍스트 파일(.txt)로 다운로드",
            data=transcribed_text,
            file_name="stt_result.txt",
            mime="text/plain"
        )
