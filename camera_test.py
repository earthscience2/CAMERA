import cv2
import os
from datetime import datetime

# 카메라 장치 번호 설정 (기본적으로 첫 번째 카메라를 0번으로 설정)
camera_port = "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-video-index1"

# 이미지가 저장될 디렉터리
save_dir = "/media/pi/CAMERA_SD"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# VideoCapture 객체 생성
cap = cv2.VideoCapture(camera_port)

if not cap.isOpened():
    print(f"카메라 {camera_port}를 열 수 없습니다.")
else:
    print(f"카메라 {camera_port}가 정상적으로 열렸습니다.")

    # 프레임 읽기
    ret, frame = cap.read()
    if ret:
        # 현재 시간을 밀리초까지 얻기
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        # 파일명에 시간 정보를 추가하여 저장
        file_name = f"{save_dir}/camera_test_{timestamp}.jpg"
        cv2.imwrite(file_name, frame)
        print(f"이미지를 '{file_name}'로 저장했습니다.")
    else:
        print("카메라에서 프레임을 가져올 수 없습니다.")

    # 카메라 닫기
    cap.release()