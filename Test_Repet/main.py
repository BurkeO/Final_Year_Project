import scipy.io.wavfile
import repet
import numpy as np
import matplotlib.pyplot as plt
import winsound


def main():
    # Import modules

    wav_file = r"D:\Users\Owen\Final_Year_Project\Dev_Test\Northern_Raven\Northern_Raven_4.wav"

    # Audio signal (normalized) and sample rate in Hz
    sample_rate, audio_signal = scipy.io.wavfile.read(wav_file)
    audio_signal = audio_signal / (2.0 ** (audio_signal.itemsize * 8 - 1))

    # Estimate the background signal and infer the foreground signal
    background_signal = repet.original(audio_signal, sample_rate)
    foreground_signal = audio_signal - background_signal

    # Write the background and foreground signals (un-normalized)
    scipy.io.wavfile.write('background_signal.wav', sample_rate, background_signal)
    scipy.io.wavfile.write('foreground_signal.wav', sample_rate, foreground_signal)

    filename = 'background_signal.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)

    filename = 'foreground_signal.wav'
    winsound.PlaySound(filename, winsound.SND_FILENAME)

    # Compute the audio, background, and foreground spectrograms
    window_length = repet.windowlength(sample_rate)
    window_function = repet.windowfunction(window_length)
    step_length = repet.steplength(window_length)
    audio_spectrogram = abs(
        repet._stft(np.mean(audio_signal, axis=1), window_function, step_length)[0:int(window_length / 2) + 1, :])
    background_spectrogram = abs(
        repet._stft(np.mean(background_signal, axis=1), window_function, step_length)[0:int(window_length / 2) + 1, :])
    foreground_spectrogram = abs(
        repet._stft(np.mean(foreground_signal, axis=1), window_function, step_length)[0:int(window_length / 2) + 1, :])

    # Display the audio, background, and foreground spectrograms (up to 5kHz)
    plt.rc('font', size=30)
    plt.subplot(3, 1, 1)
    plt.imshow(20 * np.log10(audio_spectrogram[1:int(window_length / 8), :]), aspect='auto', cmap='jet', origin='lower')
    plt.title('Audio Spectrogram (dB)')
    plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal) / sample_rate) + 1) * sample_rate / step_length),
               np.arange(1, int(np.floor(len(audio_signal) / sample_rate)) + 1))
    plt.xlabel('Time (s)')
    plt.yticks(np.round(np.arange(1e3, int(sample_rate / 8) + 1, 1e3) / sample_rate * window_length),
               np.arange(1, int(sample_rate / 8 * 1e3) + 1))
    plt.ylabel('Frequency (kHz)')
    plt.subplot(3, 1, 2)
    plt.imshow(20 * np.log10(background_spectrogram[1:int(window_length / 8), :]), aspect='auto', cmap='jet',
               origin='lower')
    plt.title('Background Spectrogram (dB)')
    plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal) / sample_rate) + 1) * sample_rate / step_length),
               np.arange(1, int(np.floor(len(audio_signal) / sample_rate)) + 1))
    plt.xlabel('Time (s)')
    plt.yticks(np.round(np.arange(1e3, int(sample_rate / 8) + 1, 1e3) / sample_rate * window_length),
               np.arange(1, int(sample_rate / 8 * 1e3) + 1))
    plt.ylabel('Frequency (kHz)')
    plt.subplot(3, 1, 3)
    plt.imshow(20 * np.log10(foreground_spectrogram[1:int(window_length / 8), :]), aspect='auto', cmap='jet',
               origin='lower')
    plt.title('Foreground Spectrogram (dB)')
    plt.xticks(np.round(np.arange(1, np.floor(len(audio_signal) / sample_rate) + 1) * sample_rate / step_length),
               np.arange(1, int(np.floor(len(audio_signal) / sample_rate)) + 1))
    plt.xlabel('Time (s)')
    plt.yticks(np.round(np.arange(1e3, int(sample_rate / 8) + 1, 1e3) / sample_rate * window_length),
               np.arange(1, int(sample_rate / 8 * 1e3) + 1))
    plt.ylabel('Frequency (kHz)')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
