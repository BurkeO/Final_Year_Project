# import librosa.display
# import matplotlib.pyplot as plt
# import numpy as np
# import cv2
#
# y, sr = librosa.load(r"D:\Users\Owen\Final_Year_Project\Recordings\Ireland\Common_Wood_Pigeon\372363\XC372363-Columba"
#                      r"_palumbus_Dublin_1518.mp3")
# # S = np.abs(librosa.stft(y))
# # chroma = librosa.feature.chroma_stft(S=S, sr=sr)
# # fig, ax = plt.subplots()
# # img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
# # fig.colorbar(img, ax=ax)
# # ax.set(title='Chromagram of a Common Wood Pigeon')
# # plt.show()
#
#
# fig, ax = plt.subplots()
# s_db = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
# img = librosa.display.specshow(s_db, y_axis='linear', x_axis='time', sr=sr, ax=ax)
# ax.set(title='Spectrogram of a Common Wood Pigeon')
# fig.colorbar(img, ax=ax, format="%+2.f dB")
# fig.savefig(f'pigeon_spec.png')
#
#
# # for window_size in [128, 512, 2048]:
# #     S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, win_length=window_size)
# #
# #     S_dB = librosa.power_to_db(S, ref=np.max)
# #     fig, ax = plt.subplots()
# #     img = librosa.display.specshow(S_dB)
# #     fig.savefig(f'{window_size}_spec.png')
# #
# # shape = cv2.imread("128_spec.png", cv2.IMREAD_GRAYSCALE)[57:429, 79: 578].shape
# # final_img = np.zeros((shape[0], shape[1], 3), np.uint8)
# #
# # for file_path_str, channel_index, win_size in [("128_spec.png", 2, 128), ("512_spec.png", 1, 512),
# #                                                ("2048_spec.png", 0, 2048)]:
# #     img = cv2.imread(file_path_str, cv2.IMREAD_GRAYSCALE)
# #     img = img[57:429, 79: 578]
# #
# #     coloured_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
# #     coloured_img[:, :, channel_index] = img
# #
# #     channel_name = {2: "red",
# #                     1: "green",
# #                     0: "blue"}[channel_index]
# #
# #     cv2.imwrite(f"{channel_name}_{win_size}_spec.png", coloured_img)
# #     final_img[:, :, channel_index] = img
# #
# # cv2.imwrite("combined_spec_colour.png", final_img)
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas

for filename, dataset_title in [("cleaning.csv", "6 Species (Audio Cleaning & Splitting)"),
                                ("no_preprocessing.csv", "6 Species (No pre-processing)"),
                                ("top_seven_no_preprocessing.csv", "7 Species (No pre-processing)")]:
    results_df = pandas.read_csv(filename)

    runs = [str(run + 1) for run in list(results_df.Run)]
    training_accuracies = [round(accuracy * 100, 2) for accuracy in list(results_df.Max_Training_In_Run_Fine)]
    validation_accuracies = [round(accuracy * 100, 2) for accuracy in list(results_df.Max_Validation_In_Run_Fine)]

    x = np.arange(len(runs))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, training_accuracies, width, label='Training')
    rects2 = ax.bar(x + width / 2, validation_accuracies, width, label='Validation')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Classification Accuracy %')
    ax.set_xlabel('Model Run Number')
    ax.set_title(f'Classification Accuracies in Training and Validation for {dataset_title}')
    ax.set_xticks(x)
    ax.set_xticklabels(runs)

    # ax.axhline(max(validation_accuracies), color="red", label="Max")
    # ax.axhline(min(validation_accuracies), color="Green", label="Min")
    ax.axhline(mean(validation_accuracies), color="Purple", label="Mean Validation Accuracy %")
    ax.text(1.02, mean(validation_accuracies), str(mean(validation_accuracies)), va='center', ha="left",
            bbox=dict(facecolor="w", alpha=0.5), transform=ax.get_yaxis_transform())

    ax.axhline(mean(training_accuracies), color="Green", label="Mean Training Accuracy %")
    ax.text(1.02, mean(training_accuracies), str(mean(training_accuracies)), va='center', ha="left",
            bbox=dict(facecolor="w", alpha=0.5), transform=ax.get_yaxis_transform())

    # plt.plot([], [], ' ', label=f"Min Validation Accuracy = {min(validation_accuracies)}%")
    # plt.plot([], [], ' ', label=f"Max Validation Accuracy = {max(validation_accuracies)}%")
    ax.legend(bbox_to_anchor=(1.08, 1), loc=0, borderaxespad=0.)
    plt.subplots_adjust(right=0.75)
    plt.yticks(np.arange(0, 102, 5))
    plt.text(0.802, 0.722, f"Minimum validation accuracy = {min(validation_accuracies)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.6952, f"Maximum validation accuracy = {max(validation_accuracies)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.6684, f"Validation accuracy range = "
                            f"{round(max(validation_accuracies) - min(validation_accuracies), 2)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.6416, f"-----------------------------------------------------", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.6148, f"Minimum training accuracy = {min(training_accuracies)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.588, f"Maximum training accuracy = {max(training_accuracies)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.text(0.802, 0.5612, f"Training accuracy range = "
                            f"{round(max(training_accuracies) - min(training_accuracies), 2)}%", fontsize=10,
             transform=plt.gcf().transFigure)
    plt.show()
