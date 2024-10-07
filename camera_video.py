import cv2
import os
from datetime import datetime
import threading

# 카메라 장치 번호 설정 (하나의 카메라만 사용)
camera_port = "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0"

# VideoCapture 객체 생성
cap = cv2.VideoCapture(camera_port)

# 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 4K 해상도
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 
cap.set(cv2.CAP_PROP_FPS, 30)  # 30fps 설정

# 비디오 코덱 설정 (MJPEG)
fourcc = cv2.VideoWriter_fourcc(*'X264')

# 비디오 파일 저장 설정
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (1920, 1080))
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽어올 수 없습니다. 종료합니다.")
        break
    
    # 프레임 저장
    out.write(frame)
    
    # 현재 시간 및 프레임 번호 출력
    frame_count += 1
    if frame_count % 10 == 0:
        print(f"{datetime.now()} - 녹화 중: {frame_count}번째 프레임")
    
    # 프레임을 화면에 표시
    cv2.imshow('Recording', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("녹화를 종료합니다.")
        break

# 모든 자원 해제
cap.release()
out.release()
cv2.destroyAllWindows()