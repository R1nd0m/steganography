#
# This is the hiding_text.py file
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

from matplotlib import pyplot as plt
import time

# ------------------------------------------------------------------------------
# Input Text -> Cover Image
# ------------------------------------------------------------------------------

def input_text_cover_image(input_text, cover_image, output):
  
  # get the input text
  with open(input_text, "r") as file:
    input_data = file.read()

  # convert data into unicode string
  input_data = [ord(c) for c in input_data]

  # load in the cover image
  cover_image = np.asarray(Image.open(cover_image))

  # output image
  output_image = np.empty((cover_image.shape[0], cover_image.shape[1], cover_image.shape[2]))

  # variables
  current_data = bin(input_data.pop(0))[2:].zfill(8)
  modified_pixel = np.array([0, 0, 0])
  current_bit = 0

  # go through each pixel
  for r_index, row in enumerate(tqdm(cover_image)):
    for p_index, pixel in enumerate(row):
      for c_index, color in enumerate(pixel):

        # check current bit
        current_bit += 1
        if current_bit == 9:
          if not len(current_data) and not len(input_data):
            modified_pixel[c_index] = color-1 if color % 2 == 0 else color
          else:
            modified_pixel[c_index] = color if color % 2 == 0 else color-1
          current_bit = 0
          continue

        # get more input data if needed
        if not len(current_data) and len(input_data):
          current_data = bin(input_data.pop(0))[2:].zfill(8)

        # if there is input data
        if len(current_data):

          # get current character & remove
          current_char = current_data[0]
          current_data = current_data[1:]

          # check parity & set pixel value
          if int(current_char) == 0: modified_pixel[c_index] = color if color % 2 == 0 else color-1
          elif int(current_char) == 1: modified_pixel[c_index] = color-1 if color % 2 == 0 else color

        # if there is no input data
        else:
      
          # stays the same
          modified_pixel[c_index] = color

      # append the pixel
      output_image[r_index][p_index] = modified_pixel

  # convert output np array to int
  output_image = output_image.astype(np.uint8)

  # save the image
  save_image = Image.fromarray(output_image)
  save_image.save(output)

# ------------------------------------------------------------------------------
# Input Text -> Cover Audio
# ------------------------------------------------------------------------------

def input_text_cover_audio(input_text, cover_audio, output):
  
  # get the input text
  with open(input_text, "r") as file:
    input_data = file.read()

  # convert data into unicode string
  input_data = [ord(c) for c in input_data]

  # load in the sound file
  with wave.open(cover_audio, mode="rb") as cover_sound:

    # get the frames
    cover_frames = bytearray(list(cover_sound.readframes(cover_sound.getnframes())))

    # variables
    current_data = list(bin(input_data.pop(0))[2:].zfill(8))

    # loop over the frames
    for frame_index in tqdm(range(0, len(cover_frames), 9), leave=False):

      # replace the LSB of each bytes
      for byte_index in range(frame_index, frame_index+8):
        cover_frames[byte_index] = (cover_frames[byte_index] & 254) | int(current_data.pop(0))

      # check if there is more input_data
      bit = 0 if len(input_data) else 1

      # set the continuation bit
      cover_frames[frame_index+9] = (cover_frames[frame_index+9] & 254) | bit

      # check if end of input_data
      if not len(input_data): break

      # load in more data
      current_data = list(bin(input_data.pop(0))[2:].zfill(8))

    print(cover_frames)

    # save the altered audio
    with wave.open(output, "wb") as file:
      file.setparams(cover_sound.getparams())
      file.writeframes(cover_frames)

# ------------------------------------------------------------------------------
# Input Text -> Cover Video
# ------------------------------------------------------------------------------

def input_text_cover_video(input_text, cover_video, output):
  
  # get the input text
  with open(input_text, "r") as file:
    input_data = file.read()

  # convert data into unicode string
  input_data = [ord(c) for c in input_data]

  # conver unicode list to binary
  input_data = list(map(int, "".join([f"{bin(c)[2:].zfill(8)}0" for c in input_data])[:-1]+"1"))

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

  # go through each pixel in the video
  for f, frame in enumerate(video_data):
    for r, row in enumerate(frame):
      for p, pixel in enumerate(row):
        for c, color in enumerate(pixel):

          # hide the bit
          video_data[f][r][p][c] = (video_data[f][r][p][c] & 254) | input_data.pop(0)

          # check if done
          if len(input_data) == 0: break

        # break out when finished
        else:
          continue
        break
      else:
        continue
      break
    else:
      continue
    break

  # variables
  file_path = uuid.uuid4()
  dir_path = "/tmp/"

  # saving each frame to a temp image file
  for f_index, frame in enumerate(tqdm(video_data)):

    # generate the filepath
    frame_path = f"{dir_path}/{file_path}-{f_index}.png"

    # save the image
    save_image = Image.fromarray(frame)
    save_image.save(frame_path)

  # generating video from saved frames
  subprocess.call(
    ["ffmpeg", "-i", f"{dir_path}/{file_path}-%d.png", "-vcodec", "png", f"{dir_path}/{file_path}-vid.mp4", "-y"],
    stdout=open(os.devnull, "w"),
    stderr=subprocess.STDOUT
  )

  # extracting the audio from the original file
  subprocess.call(
    ["ffmpeg", "-i", cover_video, "-q:a", "0", "-map", "a", f"{dir_path}/{file_path}-audio.mp3", "-y"],
    stdout=open(os.devnull, "w"),
    stderr=subprocess.STDOUT
  )

  # adding the audio back to the video
  subprocess.call(
    ["ffmpeg", "-i", f"{dir_path}/{file_path}-vid.mp4", "-i", f"{dir_path}/{file_path}-audio.mp3", "-codec", "copy", output, "-y"],
    stdout=open(os.devnull, "w"),
    stderr=subprocess.STDOUT
  )

  # remove all of the temp files
  for file in glob.glob(f"{dir_path}/*{file_path}*"): os.remove(file)

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------







































# subprocess.call(
#   ["rm", f"./tmp/{file_path}-*"],
#   stdout=open(os.devnull, "w"),
#   stderr=subprocess.STDOUT
# )







#
