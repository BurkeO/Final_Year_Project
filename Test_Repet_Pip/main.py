import nussl
import matplotlib.pyplot as plt
import time

from nussl.core.utils import audio_signals_to_musdb_track

import scipy


def main():
    start_time = time.time()

    audio_path = 'Northern_Raven_4.wav'
    sample_rate, _ = scipy.io.wavfile.read(audio_path)
    audio_signal = nussl.AudioSignal(audio_path)
    separator = nussl.separation.primitive.Repet(
        audio_signal, mask_type='binary')
    estimates = separator()

    plt.figure(figsize=(10, 6))
    plt.subplot(211)
    nussl.utils.visualize_sources_as_masks({
        'Background': estimates[0], 'Foreground': estimates[1]}, y_axis='mel', alpha_amount=2.0)

    plt.subplot(212)
    nussl.utils.visualize_sources_as_waveform({
        'Background': estimates[0], 'Foreground': estimates[1]},
        show_legend=False)
    plt.show()
    # nussl.play_utils.multitrack(estimates, ['Background', 'Foreground'])

    estimates[0].write_audio_to_file("background.wav")
    estimates[1].write_audio_to_file("foreground.wav")

    # scipy.io.wavfile.write('background_signal.wav', sample_rate, estimates[0])
    # scipy.io.wavfile.write('foreground_signal.wav', sample_rate, estimates[1])


if __name__ == '__main__':
    main()
