#
# This is the main.py file
#

import matplotlib.pyplot as plt

from tqdm import tqdm
from PIL import Image
import numpy as np
import argparse
import wave

from hiding_text import input_text_cover_image, input_text_cover_audio, input_text_cover_video
from finding_text import cover_image_secret_text, cover_audio_secret_text, cover_video_secret_text

from hiding_binary import input_binary_cover_image, input_binary_cover_video
from finding_binary import cover_image_secret_binary, cover_video_secret_binary

# ------------------------------------------------------------------------------
# Hiding
# ------------------------------------------------------------------------------

def hiding(args):

  # text input
  if args.input_text != "":

    # image cover
    if args.cover_image != "":
      
      input_text_cover_image(args.input_text, args.cover_image, args.output)

    # audio cover
    elif args.cover_audio != "":
      
      input_text_cover_audio(args.input_text, args.cover_audio, args.output)

    # video cover
    elif args.cover_video != "":
      
      input_text_cover_video(args.input_text, args.cover_video, args.output)

  # ----------------------------------------------------------------------------

  # image input
  elif args.input_binary != "":

    # image cover
    if args.cover_image != "":
      
      input_binary_cover_image(args.input_binary, args.cover_image, args.output)

    # video cover
    elif args.cover_video != "":
      
      input_binary_cover_video(args.input_binary, args.cover_video, args.output)

# ------------------------------------------------------------------------------
# Finding
# ------------------------------------------------------------------------------

def finding(args):

  # secret text
  if args.secret_text != False:

    # image input
    if args.cover_image != "":
      
      cover_image_secret_text(args.cover_image, args.output)

    # audio input
    if args.cover_audio != "":
      
      cover_audio_secret_text(args.cover_audio, args.output)

    # video input
    if args.cover_video != "":
      
      cover_video_secret_text(args.cover_video, args.output)

  # ----------------------------------------------------------------------------

  # secret binary
  if args.secret_binary != False:

    # --------------------------------------------------------------------------

    # image input
    if args.cover_image != "":
      
      cover_image_secret_binary(args.cover_image, args.output)

    # --------------------------------------------------------------------------

    # video input
    if args.cover_video != "":
      
      cover_video_secret_binary(args.cover_video, args.output)

# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------

def main():
  
  # ----------------------------------------------------------------------------

  # argument parsing
  parser = argparse.ArgumentParser(description="Steganography Tool")

  parser.add_argument("--hide", "-hh", action="store_true", help="hide data")
  parser.add_argument("--find", "-ff", action="store_true", help="find data")

  parser.add_argument("--input_text", "-it", default="", help="input text file (data to hide)")
  parser.add_argument("--input_binary", "-ib", default="", help="input binary file (data to hide)")

  parser.add_argument("--cover_image", "-ci", default="", help="image to hide data in")
  parser.add_argument("--cover_audio", "-ca", default="", help="audio to hide data in")
  parser.add_argument("--cover_video", "-cv", default="", help="video to hide data in")

  parser.add_argument("--secret_text", "-st", action="store_true", help="if there is secret text")
  parser.add_argument("--secret_binary", "-sb", action="store_true", help="if there is secret binary")

  parser.add_argument("--output", "-o", default="", help="output file")

  args = parser.parse_args()

  # ----------------------------------------------------------------------------

  # check if hiding
  if args.hide:

    # do the hiding
    hiding(args)

  # check if finding
  elif args.find:

    # do the finding
    finding(args)

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














# # load in the sound file
# with wave.open(args.cover_audio, mode="rb") as cover_sound:

#   # get the frames
#   cover_frames = bytearray(list(cover_sound.readframes(cover_sound.getnframes())))

#   # make the padding
#   padding = [ord(c) for c in int((len(cover_frames)-(len(input_data)*8*8))/8)*"@"]

#   # turn input_data & padding into bits
#   input_bits = list(map(int, "".join([bin(c)[2:].zfill(8) for c in (input_data + padding)])))

#   # replace the LSB of each byte of cover audio with one bit from input_bits
#   for index, bit in enumerate(tqdm(input_bits)):
#     cover_frames[index] = (cover_frames[index] & 254) | bit

#   # convert result to frames (bytes)
#   result = bytes(cover_frames)

#   # save the altered audio
#   with wave.open(args.output, "wb") as file:
#     file.setparams(cover_sound.getparams())
#     file.writeframes(result)





# # load in the sound file
# with wave.open(args.input_audio, mode="rb") as input_sound:

#   # get the frames
#   input_frames = bytearray(list(input_sound.readframes(input_sound.getnframes())))

#   # extract the LSB from each input byte
#   secret_data = [input_frames[i] & 1 for i in range(0, len(input_frames))]

#   # format the secret data
#   secret_data = "".join(chr(int("".join(map(str, secret_data[i:i+8])), 2)) for i in range(0, len(secret_data), 8)).split("@@@@@")[0]

#   # save the secret data
#   with open(args.output, "w") as file:
#     file.write(secret_data)





# IMAGE = np.array([
#   [
#     [23, 56, 75],
#     [42, 87, 34],
#     [73, 78, 12],
#     [24, 89, 32],
#     [98, 11, 22],
#     [78, 81, 69],
#     [83, 44, 32],
#     [42, 89, 43],
#     [56, 31, 21],
#     [87, 65, 10],
#   ],
#   [
#     [23, 56, 75],
#     [42, 87, 34],
#     [73, 78, 12],
#     [24, 89, 32],
#     [98, 11, 22],
#     [78, 81, 69],
#     [83, 44, 32],
#     [42, 89, 43],
#     [56, 31, 21],
#     [87, 65, 10],
#   ],
#   [
#     [23, 56, 75],
#     [42, 87, 34],
#     [73, 78, 12],
#     [24, 89, 32],
#     [98, 11, 22],
#     [78, 81, 69],
#     [83, 44, 32],
#     [42, 89, 43],
#     [56, 31, 21],
#     [87, 65, 10],
#   ],
#   [
#     [23, 56, 75],
#     [42, 87, 34],
#     [73, 78, 12],
#     [24, 89, 32],
#     [98, 11, 22],
#     [78, 81, 69],
#     [83, 44, 32],
#     [42, 89, 43],
#     [56, 31, 21],
#     [87, 65, 10],
#   ],
#   [
#     [23, 56, 75],
#     [42, 87, 34],
#     [73, 78, 12],
#     [24, 89, 32],
#     [98, 11, 22],
#     [78, 81, 69],
#     [83, 44, 32],
#     [42, 89, 43],
#     [56, 31, 21],
#     [87, 65, 10],
#   ]
# ])






# """
# Temp Override
# """
# cover_image = IMAGE






