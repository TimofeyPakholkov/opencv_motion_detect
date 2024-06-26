import numpy as np
import cv2


cap = cv2.VideoCapture('vtest.avi')

ret, frame2 = cap.read()
kernel = np.ones((3, 3), np.uint8)

while cap.isOpened():
    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        break

    diff = cv2.absdiff(frame1, frame2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff = cv2.erode(diff, kernel, iterations=1)
    blur = cv2.GaussianBlur(diff, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, kernel, iterations=3)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    movement_counter = 0

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour, )
        if cv2.contourArea(contour) < 500:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        movement_counter += 1

    cv2.putText(frame1, "Moving objects: " + str(movement_counter), (10, 20),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # cv2.imshow('image', frame)
    cv2.imshow('image', frame1)

    if cv2.waitKey(30) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
