#
# This is the testing.py file
#

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from tqdm import tqdm
from PIL import Image
import numpy as np
import subprocess
import imageio
import uuid
import glob
import wave
import cv2
import os

# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------

def main():
  
  # load in the video
  capture = cv2.VideoCapture("./files/endoftheworld.webm")

  # variables
  video_data_1 = []

  # read in the frames
  while capture.isOpened():
    ret, frame = capture.read()
    if not ret: break
    video_data_1.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

  # close capture
  capture.release()
  cv2.destroyAllWindows()

  # convert video frame list to numpy
  video_data_1 = np.stack(video_data_1)

  # flatten the input
  video_data_1 = video_data_1.flatten()

  # ----------------------------------------------------------------------------

  # load in the video
  capture = cv2.VideoCapture("./files/results.mp4")

  # variables
  video_data_2 = []

  # read in the frames
  while capture.isOpened():
    ret, frame = capture.read()
    if not ret: break
    video_data_2.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

  # close capture
  capture.release()
  cv2.destroyAllWindows()

  # convert video frame list to numpy
  video_data_2 = np.stack(video_data_2)

  # flatten the input
  video_data_2 = video_data_2.flatten()

  # ----------------------------------------------------------------------------

  print(video_data_1)
  print(video_data_2)

  print(video_data_1.size)
  print(video_data_2.size)


  print(video_data_1 == video_data_2)

  print(np.all(video_data_1 == video_data_2))


# ------------------------------------------------------------------------------
# What to do
# ------------------------------------------------------------------------------

if __name__ == "__main__":
  main()

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------















































