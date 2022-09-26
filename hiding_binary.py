#
# This is the hinding_binary.py file
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
# Input Binary -> Cover Image
# ------------------------------------------------------------------------------

def input_binary_cover_image(input_binary, cover_image, output):

  # load in the cover image
  cover_image = np.asarray(Image.open(cover_image))

  # get the binary file
  with open(input_binary, "rb") as file: input_data = file.read()

  # convert input to bits
  input_data = list(map(int, "".join([f"{bin(c)[2:].zfill(8)}0" for c in input_data])[:-1]+"1"))

  # add the padding
  input_data += list(np.random.randint(2, size=cover_image.size - len(input_data)))

  # flatten the image array
  flat = cover_image.flatten()

  # encode the secret data
  flat = (flat & 254) | input_data

  # shape the array back into image format
  remade = np.reshape(flat, cover_image.shape)

  # convert output np array to int
  remade = remade.astype(np.uint8)

  # save the image
  save_image = Image.fromarray(remade)
  save_image.save(output)

# ------------------------------------------------------------------------------
# Input Binary -> Cover Video
# ------------------------------------------------------------------------------

def input_binary_cover_video(input_binary, cover_video, output):

  # load in the video
  capture = cv2.VideoCapture(cover_video)

  # variables
  video_data = []

  # get the frame rate
  frame_rate = capture.get(cv2.CAP_PROP_FPS)

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

  # get the binary file
  with open(input_binary, "rb") as file:
    input_data = file.read()

  # convert input to bits
  input_data = np.array(list(map(int, "".join([f"{bin(c)[2:].zfill(8)}0" for c in input_data])[:-1]+"1")))

  # flatten the input
  flat = video_data.flatten()

  # modify the bytes
  modified = (flat[:len(input_data)] & 254) | input_data

  # overwrite with modified bytes
  np.put(flat, [i for i in range(0, modified.size)], modified)

  # shape the array back into image format
  remade = np.reshape(flat, video_data.shape)

  # variables
  file_path = uuid.uuid4()
  dir_path = "/tmp/"

  # saving each frame to a temp image file
  for f_index, frame in enumerate(tqdm(remade)):

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








# COLOR_BGR2RGB

# COLOR_RGB2BGR















# # create VideoWriter object
# out = cv2.VideoWriter(
#   f"{dir_path}/{file_path}-vid.mp4",
#   cv2.VideoWriter_fourcc(*"mp4v"),
#   frame_rate,
#   (video_data.shape[2], video_data.shape[1]),
#   True
# )

# # save each frame to video file
# for i in range(video_data.shape[0]):
#   out.write(cv2.cvtColor(video_data[i], cv2.COLOR_RGB2BGR))
# out.release()









# # generate video from saved frames
# imageio.mimwrite(f"{dir_path}/{file_path}-vid.mp4", remade, fps=frame_rate, macro_block_size=1)







# # variables
# file_path = uuid.uuid4()
# dir_path = "/tmp/"

# # saving each frame to a temp image file
# for f_index, frame in enumerate(tqdm(remade)):

#   # generate the filepath
#   frame_path = f"{dir_path}/{file_path}-{f_index}.png"

#   # save the image
#   save_image = Image.fromarray(frame)
#   save_image.save(frame_path)

# # generating video from saved frames
# subprocess.call(
#   ["ffmpeg", "-i", f"{dir_path}/{file_path}-%d.png", "-vcodec", "png", f"{dir_path}/{file_path}-vid.mp4", "-y"],
#   stdout=open(os.devnull, "w"),
#   stderr=subprocess.STDOUT
# )

# # extracting the audio from the original file
# subprocess.call(
#   ["ffmpeg", "-i", cover_video, "-q:a", "0", "-map", "a", f"{dir_path}/{file_path}-audio.mp3", "-y"],
#   stdout=open(os.devnull, "w"),
#   stderr=subprocess.STDOUT
# )

# # adding the audio back to the video
# subprocess.call(
#   ["ffmpeg", "-i", f"{dir_path}/{file_path}-vid.mp4", "-i", f"{dir_path}/{file_path}-audio.mp3", "-codec", "copy", output, "-y"],
#   stdout=open(os.devnull, "w"),
#   stderr=subprocess.STDOUT
# )

# # remove all of the temp files
# for file in glob.glob(f"{dir_path}/*{file_path}*"): os.remove(file)



















  # command = [
  #   "ffmpeg",
  #   "-y",
  #   "-f", "rawvideo",
  #   "-vcodec", "rawvideo",
  #   "-s", f"{video_data.shape[2]}x{video_data.shape[1]}",
  #   "-pix_fmt", "rgb24",
  #   "-r", f"{frame_rate}",
  #   "-i", "-",
  #   "-an",
  #   "testing.mp4" 
  # ]

  # pipe = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

  # pipe.proc.stdin.write(video_data.tostring())

  # print(bytes(np.packbits(flat)))

  # print(video_data.tostring())
  
  # res = pipe.communicate(input="".join(map(str, np.packbits(flat))))

  # print(res)
















# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------



  # # do the math
  # image_total = cover_image.shape[0] * cover_image.shape[1] * cover_image.shape[2]
  # secret_total = len(input_data)
  # total_pixels = secret_total / cover_image.shape[2]
  # total_rows = total_pixels / cover_image.shape[1]





  # print(len(input_data))
  # print(cover_image.shape)
  # print(total_rows)





  # # encode the secret data
  # for i in tqdm(range(0, image_total-1, 3)):

  #   # extract 3 pixels at a time
  #   pixels = [cover_image[i], cover_image[i+1], cover_image[i+2]]

  #   print(pixels[1])

  #   # # modify the pixels
  #   # for p_index, pixel in enumerate(pixels):
  #   #   pixels[p_index] = (pixels[p_index] & 254) | input_data.pop(0)

  #   # save the pixels


  # # go through each pixel in the image
  # for r, row in enumerate(tqdm(cover_image)):
  #   for p, pixel in enumerate(row):
  #     for c, color in enumerate(pixel):

  #       # hide the bit
  #       cover_image[r][p][c] = (cover_image[r][p][c] & 254) | input_data.pop(0)

  #       # check if done
  #       if len(input_data) == 0: break

  #     # break out when finished
  #     else:
  #       continue
  #     break
  #   else:
  #     continue
  #   break

  # # convert output np array to int
  # output_image = input_data.astype(np.uint8)

  # # save the image
  # save_image = Image.fromarray(cover_image)
  # save_image.save(output)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------




# # ------------------------------------------------------------------------------
# # Input Binary -> Cover Audio
# # ------------------------------------------------------------------------------

# def input_binary_cover_audio(input_binary, cover_audio, output):

#   # load in the sound file
#   with wave.open(cover_audio, mode="rb") as cover_sound:

#     # get the sound frames
#     cover_frames = np.asarray(list(cover_sound.readframes(cover_sound.getnframes())))

#     # get the binary file
#     with open(input_binary, "rb") as file:
#       input_data = file.read()

#     # convert input to bits
#     input_data = list(map(int, "".join([f"{bin(c)[2:].zfill(8)}0" for c in input_data])[:-1]+"1"))

#     # add the padding
#     input_data += list(np.random.randint(2, size=cover_frames.size - len(input_data)))

#     # encode the secret data
#     encoded = (cover_frames & 254) | input_data

#     print(bytearray(encoded))

#     # save the altered audio
#     with wave.open(output, "wb") as file:
#       file.setparams(cover_sound.getparams())
#       file.writeframes(bytearray(encoded))




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------





  # assemble the video array
  # video = np.concatenate((encoded, flat[len(input_data):]))


  # print(video)



  # # shape the array back into image format
  # remade = np.reshape(flat, (video_data.shape[0], video_data.shape[1], video_data.shape[2], video_data[3]))

  # # convert output np array to int
  # remade = remade.astype(np.uint8)




  # # make the padding
  # padding = flat[len(input_data):] & 1

  # print(input_data.size * input_data.itemsize)

  # print(padding.size * padding.itemsize)

  # print(flat.size * flat.itemsize)



  # print(input_data)
  # print(padding)

  # print(input_data.size)
  # print(padding.size)

  # # add the padding (post secret bytes)
  # input_data = np.concatenate((input_data, flat[len(input_data):] & 1))

  # print(input_data)
  # print(input_data.size)



  # print(video_data.size)
  # print(flat.size)

  # print(len(input_data))

  # print(len(input_data))



  # # add the padding
  # input_data += list(np.random.randint(2, size=video_data.size - len(input_data)))



  # print(video_data.size)

  # print(len(input_data))

  # # encode the secret data
  # flat = (flat & 254) | input_data

  # print(flat)

  # # shape the array back into image format
  # remade = np.reshape(flat, (video_data.shape[0], video_data.shape[1], video_data.shape[2], video_data[3]))

  # # convert output np array to int
  # remade = remade.astype(np.uint8)




