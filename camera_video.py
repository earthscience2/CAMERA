import cv2
import os
from datetime import datetime
import threading

# 카메라 장치 번호 설정 (하나의 카메라만 사용)
camera_port = "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0"

# 비디오가 저장될 디렉토리
save_dir = "/media/pi/CAMERA_SD"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 종료 플래그 설정
stop_recording = False

# 영상을 촬영하는 함수
def capture_video(camera_port):
    global stop_recording
    # VideoCapture 객체 생성
    cap = cv2.VideoCapture(camera_port, cv2.CAP_V4L2)  # V4L2 백엔드 사용

    if not cap.isOpened():
        print(f"카메라 {camera_port}를 열 수 없습니다.")
        return

    # 카메라 해상도 및 포맷 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  # 4K 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # MJPG 포맷
    cap.set(cv2.CAP_PROP_FPS, 30)  # 30 fps 설정

    # 실제 설정값 확인
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"실제 카메라 설정: {actual_width}x{actual_height}, {actual_fps} fps")

    # 비디오 파일 저장 설정
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # MJPG 코덱 사용
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"{save_dir}/camera_{timestamp}.avi"  # AVI 형식으로 저장
    out = cv2.VideoWriter(video_filename, fourcc, actual_fps, (int(actual_width), int(actual_height)))

    print(f"녹화를 시작합니다. 종료하려면 '9'를 입력하세요.")

    while not stop_recording:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 가져올 수 없습니다.")
            break

        # 비디오 파일로 저장
        out.write(frame)

    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"비디오 저장 완료: {video_filename}")

# 녹화를 제어하는 함수
def control_recording():
    global stop_recording
    while True:
        user_input = input()
        if user_input.strip() == '9':
            print("녹화를 종료합니다.")
            stop_recording = True
            break

# 쓰레드 생성 및 시작
video_thread = threading.Thread(target=capture_video, args=(camera_port,))
control_thread = threading.Thread(target=control_recording)

video_thread.start()
control_thread.start()

# 쓰레드 종료 대기
video_thread.join()
control_thread.join()