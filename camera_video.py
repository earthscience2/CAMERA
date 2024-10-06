import cv2
import os
from datetime import datetime
import threading

# 카메라별 장치 번호 설정 (각각 다른 경로)
camera_ports = [
    "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-video-index0",
    "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0",
    "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0-video-index0"
]

# 이미지가 저장될 디렉토리
save_dir = "/media/pi/CAMERA_SD"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 종료 플래그 설정
stop_threads = False

# 카메라별로 영상을 촬영하는 함수
def capture_video(camera_port, camera_id):
    global stop_threads
    # VideoCapture 객체 생성
    cap = cv2.VideoCapture(camera_port)

    if not cap.isOpened():
        print(f"카메라 {camera_port}를 열 수 없습니다.")
        return

    # 카메라 해상도 및 MJPG 포맷 설정
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # MJPG 포맷
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  # 4K 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_FPS, 30)  # 30 fps 설정

    print(f"카메라 {camera_port}가 정상적으로 열렸습니다. 해상도: 3840x2160, 30fps")

    # 비디오 코덱 설정 및 비디오 파일 저장 (mp4v 코덱 사용)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4v 코덱 사용
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"{save_dir}/camera_{camera_id}_{timestamp}.mp4"  # MP4 형식으로 저장
    out = cv2.VideoWriter(video_filename, fourcc, 30.0, (3840, 2160))  # 4K 해상도 설정

    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            print(f"카메라 {camera_id}에서 프레임을 가져올 수 없습니다.")
            break
        
        # 비디오 파일로 저장
        out.write(frame)

    # 카메라와 비디오 저장 객체 닫기
    cap.release()
    out.release()
    print(f"카메라 {camera_id}에서 비디오 저장 완료: {video_filename}")

# 각 카메라를 쓰레드로 실행
threads = []
for i, camera_port in enumerate(camera_ports):
    thread = threading.Thread(target=capture_video, args=(camera_port, i+1))
    threads.append(thread)
    thread.start()

try:
    # 메인 스레드는 사용자로부터 종료 신호를 기다림
    while True:
        if input("종료하려면 숫자 '9'를 입력하세요: ").strip() == '9':
            stop_threads = True
            break
except KeyboardInterrupt:
    print("사용자가 프로그램을 중단했습니다.")
    stop_threads = True

# 모든 쓰레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

cv2.destroyAllWindows()