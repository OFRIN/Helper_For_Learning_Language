import cv2

image = cv2.imread("./data/images/infectious.png")

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        _image = image.copy()

        cv2.circle(_image, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('show', _image)
        cv2.waitKey(1)

    elif event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

cv2.imshow('show', image)
cv2.setMouseCallback('show', mouse_callback)

cv2.waitKey(0)

# st = 460 242
# end = 1150 242

