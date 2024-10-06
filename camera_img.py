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

# 카메라별로 이미지를 촬영하고 저장하는 함수
def capture_images(camera_port, camera_id):
    # VideoCapture 객체 생성
    cap = cv2.VideoCapture(camera_port)

    if not cap.isOpened():
        print(f"카메라 {camera_port}를 열 수 없습니다.")
        return

    # 카메라 해상도를 4K로 설정 (3840x2160)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    print(f"카메라 {camera_port}가 정상적으로 4K 해상도로 설정되었습니다.")

    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print(f"카메라 {camera_id}에서 프레임을 가져올 수 없습니다.")
    else:
        # 현재 시간을 기반으로 파일명 설정
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        image_filename = f"{save_dir}/camera_{camera_id}_{timestamp}.jpg"

        # 이미지 저장
        cv2.imwrite(image_filename, frame)
        print(f"카메라 {camera_id}에서 이미지를 저장했습니다: {image_filename}")

    # 카메라 닫기
    cap.release()

# 각 카메라를 쓰레드로 실행
threads = []
for i, camera_port in enumerate(camera_ports):
    thread = threading.Thread(target=capture_images, args=(camera_port, i+1))
    threads.append(thread)
    thread.start()

# 모든 쓰레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

cv2.destroyAllWindows()

