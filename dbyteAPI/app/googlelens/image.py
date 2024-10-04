import cv2
import pytesseract
import matplotlib.pyplot as plt

filename = '/home/hidryde/dev/dbyte/dbyteAPI/app/googlelens/1.jpg'

# read the image and get the dimensions
img = cv2.imread(filename)
h, w, _ = img.shape # assumes color image

# run tesseract, returning the bounding boxes
boxes = pytesseract.image_to_boxes(img, lang='jpn')
print(pytesseract.image_to_string(img)) #print identified text

# draw the bounding boxes on the image
for b in boxes.splitlines():
    b = b.split()
    cv2.rectangle(img, ((int(b[1]), h - int(b[2]))), ((int(b[3]), h - int(b[4]))), (0, 255, 0), 2)

# save the image to disk
cv2.imwrite('output.jpg', img)