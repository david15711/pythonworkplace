import cv2

capture = cv2.VideoCapture('http://192.168.0.30/capture?_cb')
frame_size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

while True:
    ret, frame = capture.read()
    if not ret:
        break

    cv2.imshow('ESP32-CAM', frame)

    # Press 'Esc' to stop
    key = cv2.waitKey(25)
    if key == 27:
        break

if capture.isOpened():
    capture.release()

