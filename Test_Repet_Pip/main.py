import nussl
import matplotlib.pyplot as plt
import time


def main():
    start_time = time.time()

    audio_path = 'Northern_Raven_4.wav'
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
    nussl.play_utils.multitrack(estimates, ['Background', 'Foreground'])


if __name__ == '__main__':
    main()
