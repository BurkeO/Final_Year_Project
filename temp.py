from pathlib import Path
import os
import cv2
import numpy


def main():
    # os.system(f"ffmpeg -i D:/Users/Owen/Final_Year_Project/Dev_Recordings_Full_Wav/Common_Chaffinch/Common_Chaffinch_0.wav -af loudnorm temp.wav -y")
    # os.system(f'ffmpeg -i temp.wav -af \"highpass=f=20, lowpass=f=9500\" temp1.wav -y')
    # os.system(f"ffmpeg -i temp1.wav -af afftdn temp2.wav -y")
    # os.system(f"ffmpeg -i temp2.wav -af silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-46dB temp3.wav -y")
    # os.system(f"ffmpeg -i temp3.wav -lavfi showspectrumpic=stop=10000 temp.png -y")
    # os.remove("temp.wav")
    # os.remove("temp1.wav")
    # os.remove("temp2.wav")
    # os.remove("temp3.wav")

    # image = cv2.imread("temp.png")
    # image = image[60:-60, 156:-156]
    # cv2.imwrite("crop_temp.png", image)
    image = cv2.imread("crop_temp.png")
    # print(image.shape)
    # print(image.dtype)
    # temp = image.astype('float64')
    # temp = numpy.log(temp + 1e-9)
    # temp -= numpy.mean(temp)
    # temp /= numpy.std(temp)
    # # temp = cv2.normalize(temp, None, 0, 255)

    # temp = image.astype('float64')

    temp = cv2.normalize(temp, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    cv2.imwrite("norm_temp.png", temp)

    # src_dir = Path("D:/Users/Owen/Final_Year_Project/Dev_Test")
    # dst_dir = Path("D:/Users/Owen/Final_Year_Project/Dev_Test_10_min_split")
    # for wav_file in src_dir.glob('**/*.wav'):
    #     species = str(wav_file.parents[0]).split('\\')[-1]
    #     dst_folder = Path(f"{str(dst_dir)}/{species}")
    #     dst_folder.mkdir(parents=True, exist_ok=True)
    #     os.system(f"ffmpeg -i {wav_file.absolute()} -f segment -segment_time 600 -c copy "
    #               f"{str(dst_folder)}/{wav_file.stem}%03d.wav")


if __name__ == '__main__':
    main()
