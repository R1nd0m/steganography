#
# This is the finding_binary.py file
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
# Cover Image -> Secret Binary
# ------------------------------------------------------------------------------

def cover_image_secret_binary(cover_image, output):

  # load in the image
  input_data = np.asarray(Image.open(cover_image))

  # flatten the image array
  flat = input_data.flatten()

  # extract the encoded data
  raw_data = flat & 1

  # group every 9 bits
  grouped = np.reshape(raw_data, (int(raw_data.shape[0]/9), 9))

  # find where the secret data ends
  no_padding = grouped[:np.where(grouped[:, 8] == 1)[0][0]+1]

  # remove the last column
  data = no_padding[:, :-1]

  # flatten the grouping
  data = data.flatten()

  # pack the bits into bytes
  data = np.packbits(data)

  # save the binary data
  with open(output, "wb") as file: file.write(data)

# ------------------------------------------------------------------------------
# Cover Video -> Secret Binary
# ------------------------------------------------------------------------------

def cover_video_secret_binary(cover_video, output):

  # load in the video
  capture = cv2.VideoCapture(cover_video)

  # variables
  video_data = []

  # read in the frames
  while capture.isOpened():
    ret, frame = capture.read()
    if not ret: break
    video_data.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

  # close capture
  capture.release()
  cv2.destroyAllWindows()

  # convert video frame list to numpy
  video_data = np.stack(video_data)

  # flatten the image array
  flat = video_data.flatten()

  # extract the encoded data
  raw_data = flat & 1

  # group every 9 bits
  grouped = np.reshape(raw_data, (int(raw_data.shape[0]/9), 9))

  # find where the secret data ends
  no_padding = grouped[:np.where(grouped[:, 8] == 1)[0][0]+1]

  # remove the last column
  data = no_padding[:, :-1]

  # flatten the grouping
  data = data.flatten()

  # pack the bits into bytes
  data = np.packbits(data)

  # save the binary data
  with open(output, "wb") as file:
    file.write(data)

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------




















# # cut of the end
# full_rows = raw_data[:(int(raw_data.shape[0]/9)*9)]





# # ------------------------------------------------------------------------------
# # Cover Audio -> Secret Binary
# # ------------------------------------------------------------------------------

# def cover_audio_secret_binary(cover_image, output):

#   pass




