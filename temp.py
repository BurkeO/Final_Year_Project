import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cv2

y, sr = librosa.load(r"D:\Users\Owen\Final_Year_Project\Recordings\Ireland\Common_Wood_Pigeon\372363\XC372363-Columba"
                     r"_palumbus_Dublin_1518.mp3")
# S = np.abs(librosa.stft(y))
# chroma = librosa.feature.chroma_stft(S=S, sr=sr)
# fig, ax = plt.subplots()
# img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
# fig.colorbar(img, ax=ax)
# ax.set(title='Chromagram of a Common Wood Pigeon')
# plt.show()


# for window_size in [128, 512, 2048]:
#     S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, win_length=window_size)
#
#     S_dB = librosa.power_to_db(S, ref=np.max)
#     fig, ax = plt.subplots()
#     img = librosa.display.specshow(S_dB)
#     fig.savefig(f'{window_size}_spec.png')

shape = cv2.imread("128_spec.png", cv2.IMREAD_GRAYSCALE)[57:429, 79: 578].shape
final_img = np.zeros((shape[0], shape[1], 3), np.uint8)

for file_path_str, channel_index, win_size in [("128_spec.png", 2, 128), ("512_spec.png", 1, 512),
                                               ("2048_spec.png", 0, 2048)]:
    img = cv2.imread(file_path_str, cv2.IMREAD_GRAYSCALE)
    img = img[57:429, 79: 578]

    coloured_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    coloured_img[:, :, channel_index] = img

    channel_name = {2: "red",
                    1: "green",
                    0: "blue"}[channel_index]

    cv2.imwrite(f"{channel_name}_{win_size}_spec.png", coloured_img)
    final_img[:, :, channel_index] = img

cv2.imwrite("combined_spec_colour.png", final_img)
