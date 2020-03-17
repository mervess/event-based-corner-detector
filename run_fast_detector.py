import numpy as np
import cv2
import time
import sys

from fast_detector import FastDetector


class CornerDetector:

    def __init__( self ):
        # statistics
        self.total_time = 0.0
        self.total_events = 0
        self.total_corners = 0

    def detect_corners( self, events_file, show_statistics ):
        events = []
        fast = FastDetector() # the corner detector to be used

        # OpenCV
        # canvas = np.zeros( ( fast.sensor_height, fast.sensor_width, 3 ), np.uint8 ) empty canvas

        # cv2.imshow( "Corners", canvas )
        # cv2.waitKey( 1 )

        if show_statistics:
            start_time = time.clock()


        # First events are stored in an array
        with open( events_file ) as input_file:
            for line in input_file:
                parts = line.split()
                ts = float(parts[0]) # timestamp in microsecond
                x = int(parts[1])
                y = int(parts[2])
                p = int(parts[3])
                events.append( ( x, y, ts, p ) )
            else:
                print("Events are stored in the list.")

        images_txt_file = "dvs/shapes_6dof/images.txt"
        image_file = "dvs/shapes_6dof/"
        # counter = 1
        idx = 0

        # show corners on images
        with open( images_txt_file ) as images_txt:
            for image_line in images_txt:
                parts = image_line.split()
                ts = float(parts[0])  # timestamp in microsecond
                image_name = parts[1] # image name

                canvas = cv2.imread( image_file + image_name ) # read the image

                eventCount = 0
                features = 0

                # if s <= 20*counter:
                while events[idx][2] <= ts:
                    x = events[idx][0]
                    y = events[idx][1]
                    s = events[idx][2]
                    p = events[idx][3]

                    if fast.is_feature( x, y, s, p ):
                        # publish feature events, use OpenCV
                        if p == 0:
                            canvas[y, x] = (255, 0, 0)
                        elif p == 1:
                            canvas[y, x] = (0, 0, 255)

                        cv2.imshow( "Corners", canvas )
                        cv2.waitKey( 1 )
                        features = features + 1

                    idx = idx + 1
                    eventCount = eventCount + 1
                else:
                    # print(counter)
                    # counter = counter + 1
                    print( 'idx: {:d}'.format(idx) )
                    print( 'For image {:s} event count is {:d}, feature count is {:d}.'.format(image_name, eventCount, features) )
                    # fast.clear()
                    # canvas = np.zeros_like( canvas )

                # self.total_events += 1
                # print ("new event %d" % self.total_events)


        if show_statistics:
            end_time = time.clock()
            self.total_time = end_time - start_time
            self.total_corners = len( features )

            if self.total_events > 0:
                reduction_rate = 100.*(1.-self.total_corners/self.total_events)
                reduction_factor = self.total_events/self.total_corners
                events_per_second = self.total_events/self.total_time

                print( 'Total number of corners: %d' % (self.total_corners) )

                if sys.version_info > (3, 0):
                    # for python 3.x
                    print( 'With {:s} reduction rate: {:.3f} ({:.0f}x). Speed: {:.0f} e/s'.format(fast.get_name(), reduction_rate, reduction_factor, events_per_second) )
                else:
                    # for python 2.x
                    print( "With %s reduction rate: %.3f (%.0fx). Speed: %.0f e/s" % (fast.get_name(), reduction_rate, reduction_factor, events_per_second) )


if __name__ == '__main__':
    events_file = "dvs/shapes_6dof/events.txt"
    corner_detector = CornerDetector()
    corner_detector.detect_corners( events_file, False )
