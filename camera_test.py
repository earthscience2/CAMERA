import cv2

# 카메라 장치 번호 설정 (기본적으로 첫 번째 카메라를 0번으로 설정)
camera_port = 0

# VideoCapture 객체 생성
cap = cv2.VideoCapture(camera_port)

if not cap.isOpened():
    print(f"카메라 {camera_port}를 열 수 없습니다.")
else:
    print(f"카메라 {camera_port}가 정상적으로 열렸습니다.")

    # 카메라 영상 읽기
    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 가져올 수 없습니다.")
            break
        
        # 프레임을 창에 표시
        cv2.imshow("Camera", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 카메라 및 창 닫기
    cap.release()
    cv2.destroyAllWindows()