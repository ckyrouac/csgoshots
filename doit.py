#!/usr/bin/env python

import argparse
import cv2
import time
import datetime
# from matplotlib import pyplot as plt

args = None


def videocapture():
    cap = cv2.VideoCapture(args.input)
    while not cap.isOpened():
        cap = cv2.VideoCapture(args.input)
        cv2.waitKey(1000)
        print "Wait for the header"

    pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    is_scope_frame = False
    prev_frame_is_scope = False
    prev_frame = None
    frame = None
    while True:
        prev_frame = frame
        flag, frame = cap.read()
        if flag:
            # The frame is ready and already captured
            # cv2.imshow('video', frame)
            prev_frame_is_scope = is_scope_frame
            is_scope_frame = analyzeimage(frame)
            pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            # print str(pos_frame)+" frames"
        else:
            # The next frame is not ready, so we try to read it again
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
            print "frame is not ready"
            # It is better to wait for a while for the next frame to be ready
            cv2.waitKey(1000)

        if prev_frame_is_scope is True and is_scope_frame is False:
            exportframe(prev_frame, 'frame1')
            exportframe(frame, 'frame2')

        if cv2.waitKey(10) == 27:
            break
        if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
            # If the number of captured frames is equal to the total number of frames,
            # we stop
            break


# Returns True if scoped, False if not scoped
def analyzeimage(img):
    # img = cv2.imread(img, 0)
    template = cv2.imread('scope_still_cut.jpg', 1)
    # w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    meth = methods[0]
    method = eval(meth)
    threshold = 0

    # Apply template Matching
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # useful for defining threshold
    # print "min_val: %s" % min_val
    # print "max_val: %s" % max_val
    # print "min_loc: %s" % str(min_loc)
    # print "max_loc: %s" % str(max_loc)

    if threshold < min_val:
        return True
    else:
        return False


def exportframe(frame, filename):
    print "Shot found!"
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    cv2.imwrite('./out/' + timestamp + filename + '.png', frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    if args.input is None:
        print('Must specify input video. For example:')
        print('./shotfinder.py -i myvideo.mp4')
        exit(0)
    videocapture()
