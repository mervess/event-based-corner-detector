# Event-based FAST Corner Detector
Python implementation of FAST (**F**eatures from **A**ccelerated **S**egment **T**est) Event-based Corner Detector.

The [original project](https://github.com/uzh-rpg/rpg_corner_events) was implemented in C++ by the Robotics and Perception Group of ETH Zurich.

This was a side project of mine to be used in my early research.

## File descriptions

❶ [run_fast_detector.py](https://github.com/mervess/event-based-corner-detector/blob/master/run_fast_detector.py) is the (main) runnable file. In the *main* part of the code, it requires the path of the events file (*.txt*). Currently, it is hard-coded and set to "dvs/shapes_6dof/events.txt". You can find various event camera datasets [here](https://rpg.ifi.uzh.ch/software_datasets.html).

❷ [fast_detector.py](https://github.com/mervess/event-based-corner-detector/blob/master/fast_detector.py) aids to detect the corners in an image via FAST algorithm. 

❸ [detect_features_traditionally.py](https://github.com/mervess/event-based-corner-detector/blob/master/detect_features_traditionally.py) was my playground in this project regarding to try and observe the performance of the other corner detectors in image processing.

## Requirements

To run the project, you need files ❶ and ❷ above.

❶ requires OpenCV (cv2) and numpy.

❷ only requires numpy.

❸ requires OpenCV (cv2), numpy, sci-kit (skimage) and matplotlib.
