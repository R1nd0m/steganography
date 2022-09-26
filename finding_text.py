#
# This is the finding_text.py file
#

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from tqdm import tqdm
from PIL import Image
import numpy as np
import subprocess
import uuid
import glob
import wave
import cv2
import os

# ------------------------------------------------------------------------------
# Cover Image -> Secret Text
# ------------------------------------------------------------------------------

def cover_image_secret_text(cover_image, output):
  
  # load in the image
  input_data = np.asarray(Image.open(cover_image))

  # variables
  secret_data = []
  buffer = ""

  # go through each pixel color
  for r_index, row in enumerate(input_data):
    for p_index, pixel in enumerate(row):
      for c_index, color in enumerate(pixel):

        # check if full buffer
        if len(buffer) == 9:
          secret_data.append(chr(int(buffer[:8], 2)))
          if int(buffer[8]) == 1: break
          buffer = ""

        # append to the buffer
        buffer += "0" if int(color) % 2 == 0 else "1"

      # end of secret
      else:
        continue
      break
    else:
      continue
    break

  # check if full buffer
  if len(buffer) == 9: secret_data.append(chr(int(buffer[:8], 2)))

  # merge the list into a string
  secret_data = "".join(secret_data)

  # save the secret data
  with open(output, "w") as file:
    file.write(secret_data)

# ------------------------------------------------------------------------------
# Cover Audio -> Secret Text
# ------------------------------------------------------------------------------

def cover_audio_secret_text(cover_audio, output):
  
  # load in the sound file
  with wave.open(cover_audio, mode="rb") as input_sound:

    # get the frames
    input_frames = bytearray(list(input_sound.readframes(input_sound.getnframes())))

    # variables
    secret_data = []

    # loop over the frames
    for frame_index in tqdm(range(0, len(input_frames), 9), leave=False):

      # loop through the first 8 bytes
      for byte_index in range(frame_index, frame_index+8):
        secret_data.append(input_frames[byte_index] & 1)

      # check if end of secret data
      if input_frames[frame_index+9] & 1 == 1: break

    # format the secret data
    secret_data = "".join(chr(int("".join(map(str, secret_data[i:i+8])), 2)) for i in range(0, len(secret_data), 8))

    # save the secret data
    with open(output, "w") as file:
      file.write(secret_data)

# ------------------------------------------------------------------------------
# Cover Video -> Secret Text
# ------------------------------------------------------------------------------

def cover_video_secret_text(cover_video, output):
  
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

  # variables
  secret_data = []
  buffer = ""

  # go through each pixel in the video
  for f, frame in enumerate(video_data):
    for r, row in enumerate(frame):
      for p, pixel in enumerate(row):
        for c, color in enumerate(pixel):
          
          # check if full buffer
          if len(buffer) == 9:
            secret_data.append(chr(int(buffer[:8], 2)))
            if int(buffer[8]) == 1: break
            buffer = ""

          # append to the buffer
          buffer += str(color & 1)

        # end of secret
        else:
          continue
        break
      else:
        continue
      break
    else:
      continue
    break

  # check if full buffer
  if len(buffer) == 9: secret_data.append(chr(int(buffer[:8], 2)))

  # merge the list into a string
  secret_data = "".join(secret_data)

  # save the secret data
  with open(output, "w") as file:
    file.write(secret_data)

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------







































#
