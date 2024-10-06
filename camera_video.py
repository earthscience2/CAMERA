import cv2
import os
from datetime import datetime, timedelta

# 카메라 장치 번호 설정 (하나의 카메라만 사용)
camera_port = "/dev/v4l/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-video-index0"

# 이미지가 저장될 디렉토리
save_dir = "/media/pi/CAMERA_SD"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 영상을 촬영하는 함수
def capture_video(camera_port):
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
    video_filename = f"{save_dir}/camera_{timestamp}.mp4"  # MP4 형식으로 저장
    out = cv2.VideoWriter(video_filename, fourcc, 30.0, (3840, 2160))  # 4K 해상도 설정

    frame_count = 0  # 프레임 카운트
    last_check_time = datetime.now()  # 마지막 상태 확인 시간
    start_time = datetime.now()  # 시작 시간

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"카메라에서 프레임을 가져올 수 없습니다.")
            break

        # 비디오 파일로 저장
        out.write(frame)
        frame_count += 1  # 프레임 수 증가

        # 10초마다 로그 출력
        current_time = datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if current_time - last_check_time >= timedelta(seconds=10):
            print(f"카메라: {elapsed_time:.2f}초 동안 {frame_count}개의 프레임이 저장되었습니다.")
            last_check_time = current_time  # 상태 확인 시간 갱신

        # '9' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('9'):
            break

    # 카메라와 비디오 저장 객체 닫기
    cap.release()
    out.release()
    print(f"카메라에서 비디오 저장 완료: {video_filename}. 총 {frame_count} 프레임이 저장되었습니다.")

# 촬영 시작
capture_video(camera_port)

cv2.destroyAllWindows()
