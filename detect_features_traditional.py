# sci-kit imports
from skimage import io, feature, filters

# openCV imports
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt



def opencv_test(im_file):
    img = cv.imread(im_file)

    # Initiate FAST object with default values
    fast = cv.FastFeatureDetector_create()

    # find and draw the keypoints
    kp = fast.detect(img,None)
    img2 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
    cv.imshow('FAST corners', img2)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Print all default params
    # print( "Threshold: {}".format(fast.getThreshold()) )
    # print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
    # print( "neighborhood: {}".format(fast.getType()) )
    # print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )
    # cv.imwrite('fast_true.png',img2)

    # # Disable nonmaxSuppression
    # fast.setNonmaxSuppression(0)
    # kp = fast.detect(img,None)
    # print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
    # img3 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
    # cv.imwrite('fast_false.png',img3)


def scikit_test(im_file):
    im = io.imread(im_file)
    # edges = feature.canny(im)
    # io.imshow(edges)
    # io.show()

    edges = filters.sobel(im)
    io.imshow(edges)


# Harris Corner Detector
def harris_test(im_file):
    img = cv.imread(im_file)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]
    cv.imshow('dst',img)
    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


event_im_shapes = "images/canvas_shapes_frame_00000000.png"
im_shapes = "images/shapes_im.png"
harris_test(im_shapes)
