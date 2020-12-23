"""
Predict an image
accepts image grid
return predicted grid
"""
import cv2
import numpy as np
from tensorflow.python.keras.models import load_model
import matplotlib.pyplot as plt
import dill as pickle
from extractSudoku import extract, scale_and_centre, order_corner_points
model = load_model('model.h5')

def display_image(img):
    cv2.imshow('image', img)  # Display the image
    cv2.waitKey(0)  # Wait for any key to be pressed (with the image window active)
    cv2.destroyAllWindows()  # Close all windows


def extract_number_image(img_grid):
    tmp_sudoku = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):

            image = img_grid[i][j]
            image = cv2.resize(image, (28, 28))
            original = image.copy()

            thresh = 128  # define a threshold, 128 is the middle of black and white in grey scale
            # threshold the image
            gray = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
            if not(255 in gray[6:20,6:20]):
                continue
            gray[:, 0:3] = 0
            gray[0:3, :] = 0
            gray[:, 25:28] = 0
            gray[25:28, :] = 0
            # Find contours
            cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)

                if ((h >= 25) or (w >= 25) or (h<=3) or (w <= 3)):
                    # Note the number is always placed in the center
                    # Since image is 28x28
                    # the number will be in the center thus x >3 and y>3
                    # Additionally any of the external lines of the sudoku will not be thicker than 3
                    continue
                ROI = gray[y:y + h, x:x + w]
                ROI = scale_and_centre(ROI, 120)
                # display_image(ROI)

                # Writing the cleaned cells
                # cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite("./CheckBoardCells/cell{}{}.png".format(i, j), gray)
                cv2.imwrite("./CleanedBoardCells/cell{}{}.png".format(i, j), ROI)
                tmp_sudoku[i][j] = predict(ROI)
                # print(i, j, x, y, w, h)

    return tmp_sudoku


def predict(img_grid):
    image = img_grid.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (28, 28))
    # display_image(image)
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    image /= 255

    # plt.imshow(image.reshape(28, 28), cmap='Greys')
    # plt.show()

    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)
    # print(pred)
    # print(pred.argmax())

    return pred.argmax()

# extract_number_image(extract())
