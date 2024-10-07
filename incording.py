import cv2
import numpy as np
from tqdm import tqdm
import ffmpeg
import subprocess

def full_video(video_path, output_path):
    # 변환할 원본 비디오 파일 경로
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_scale = 'scale=' + str(1920) + ':' + str(1080)
    print(fps)

    ffmpeg_command = [
        'ffmpeg',
        '-i', video_path,  # 입력 파일
        '-vf', frame_scale,  # 해상도를 4K(3840x2160)로 변경, 너무 높은 해상도 피하기(1920x2160)
        '-b:v', '5000k',  # 비트 전송률 설정 (5000 kbps)
        '-maxrate', '5000k',  # 최대 비트레이트 설정
        '-bufsize', '10000k',  # 버퍼 크기 설정
        '-r', str(int(fps)),  # 프레임 속도를 30 fps로 설정
        '-c:v', 'libx264',  # 비디오 코덱 설정 (H.264)
        '-pix_fmt', 'yuv420p',  # 픽셀 형식 설정 (yuv420p)
        '-preset', 'medium',  # 인코딩 속도와 품질의 균형을 위한 설정
        output_path  # 출력 파일
    ]
    # FFmpeg 명령어 실행
    subprocess.run(ffmpeg_command)

    print(output_path + " 생성완료.")


video_path = "D:/please.mjpeg"
output_path = "D:/please.mp4"
full_video(video_path, output_path)