import os

import libfmp.b
import libfmp.c4
import libfmp.c7
import librosa
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from random import shuffle
import random


def compute_cens_from_file(fn_wav, Fs=22050, N=4410, H=2205, ell=21, d=5):
    """Compute CENS features from file

    Notebook: C7/C7S2_AudioMatching.ipynb

    Args:
        fn_wav: Filename of wav file
        Fs: Feature rate of wav file
        N: Window size for STFT
        H: Hope size for STFT
        ell: Smoothing length
        d: Downsampling factor

    Returns:
        C_CENS: CENS features
        F_CENS: Feature rate of CENS features
        x_duration: Duration (seconds) of wav file
    """
    x, Fs = librosa.load(fn_wav, sr=Fs)
    x_duration = x.shape[0] / Fs
    X_chroma = librosa.feature.chroma_stft(y=x, sr=Fs, tuning=0, norm=None, hop_length=H, n_fft=N)
    X_CENS, Fs_CENS = libfmp.c7.compute_cens_from_chromagram(X_chroma, Fs=Fs / H, ell=ell, d=d)
    N = X_CENS.shape[1]
    return X_CENS, N, Fs_CENS, x_duration


def compute_matching_function_dtw(X, Y, step_size=2):
    """Compute CENS features from file

    Notebook: C7/C7S2_AudioMatching.ipynb

    Args:
        X: Query feature sequence (given as K x N matrix)
        Y: Database feature sequence (given as K x M matrix)
        step_size: Parameter for step size condition (1 or 2)

    Returns:
        Delta: DTW-based matching function
        C: Cost matrix
        D: Accumulated cost matrix
    """
    C = libfmp.c7.cost_matrix_dot(X, Y)
    if step_size == 1:
        D = libfmp.c7.compute_accumulated_cost_matrix_subsequence_dtw(C)
    if step_size == 2:
        D = libfmp.c7.compute_accumulated_cost_matrix_subsequence_dtw_21(C)
    N, M = C.shape
    Delta = D[-1, :] / N
    return Delta, C, D


def matches_dtw(pos, D, stepsize=2):
    """Derives matches from positions for DTW-based strategy

    Notebook: C7/C7S2_AudioMatching.ipynb

    Args:
        pos: End positions of matches
        D: Accumulated cost matrix

    Returns:
        matches: Array containing matches (start, end)
    """
    matches = np.zeros((len(pos), 2)).astype(int)
    for k in range(len(pos)):
        t = pos[k]
        matches[k, 1] = t
        if stepsize == 1:
            P = libfmp.c7.compute_optimal_warping_path_subsequence_dtw(D, m=t)
        if stepsize == 2:
            P = libfmp.c7.compute_optimal_warping_path_subsequence_dtw_21(D, m=t)
        s = P[0, 1]
        matches[k, 0] = s
    return matches


def compute_plot_matching_function_DTW(fn_wav_x, Y, ell=21, d=5, step_size=2, tau=0.2, num=5,
                                       y_lim=None):
    if y_lim is None:
        y_lim = [0, 0.35]
    color_ann = {'Theme': [0, 0, 1, 0.1], 'Match': [0, 0, 1, 0.2]}
    X, N, Fs_X, x_duration = compute_cens_from_file(fn_wav_x, ell=ell, d=d)
    Delta, C, D = compute_matching_function_dtw(X, Y, step_size=step_size)
    pos = libfmp.c7.mininma_from_matching_function(Delta, rho=2 * N // 3, tau=tau, num=num)
    matches = matches_dtw(pos, D, stepsize=step_size)
    return matches

    # fig, ax = plt.subplots(2, 1, gridspec_kw={'width_ratios': [1],
    #                                           'height_ratios': [1, 1]}, figsize=(8, 4))
    # cmap = libfmp.b.compressed_gray_cmap(alpha=-10, reverse=True)
    # libfmp.b.plot_matrix(C, Fs=Fs_X, ax=[ax[0]], ylabel='Time (seconds)',
    #                      title='Cost matrix $C$ with ground truth annotations (blue rectangles)',
    #                      colorbar=False, cmap=cmap)
    # libfmp.b.plot_segments_overlay([(0.2, 21.5, "Theme")], ax=ax[0], alpha=0.2, time_max=y_duration,
    #                                colors=color_ann, print_labels=False)
    #
    # title = r'Matching function $\Delta_\mathrm{DTW}$ with matches (red rectangles)'
    # libfmp.b.plot_signal(Delta, ax=ax[1], Fs=Fs_X, color='k', title=title, ylim=y_lim)
    # ax[1].grid()
    # libfmp.c7.plot_matches(ax[1], matches, Delta, Fs=Fs_X, s_marker='', t_marker='o')
    # plt.tight_layout()
    # plt.show()


def main():
    # data_dir = "D:/Users/Owen/Final_Year_Project/Dev_Test"
    data_dir = "D:/Users/Owen/Final_Year_Project/Dev_Test_10_min_split"
    # data_dir = "D:/Users/Owen/Final_Year_Project/Dev_Test_Split_wavs"
    parent_list = os.listdir(f'{data_dir}/Common_Chiffchaff')
    number_for_each = 100
    chiffchaff_list = parent_list[:number_for_each]
    for i in range(len(chiffchaff_list)):
        chiffchaff_list[i] = f'{data_dir}/Common_Chiffchaff/{chiffchaff_list[i]}'
    parent_list = os.listdir(f'{data_dir}/Northern_Raven')
    raven_list = parent_list[:number_for_each]
    for i in range(len(raven_list)):
        raven_list[i] = f'{data_dir}/Northern_Raven/{raven_list[i]}'

    fn_wav_all = chiffchaff_list + raven_list
    random.Random(4).shuffle(fn_wav_all)

    test_percentage = 0.2
    wav_test_list = fn_wav_all[:int(len(fn_wav_all) * test_percentage)]
    wav_train_list = fn_wav_all[int(len(fn_wav_all) * test_percentage):]

    number_correct = 0

    training_file_cens_list = []
    for file in wav_train_list:
        print(f'Computing cens from {Path(file).stem}')
        training_file_cens_list.append(compute_cens_from_file(file))

    for test_index, test_file in enumerate(wav_test_list):
        file_to_match_length = {}
        for train_index, f in enumerate(wav_train_list):
            # print(f'=== Query X: {Path(test_file).stem}; Database Y:{Path(f).stem}')
            print(f'Testing file {test_index+1} / {len(wav_test_list)} ({Path(wav_test_list[test_index]).stem}) - '
                  f'Comparing against {train_index+1} / {len(wav_train_list)} ({Path(wav_train_list[train_index]).stem})')
            # matches = compute_plot_matching_function_DTW(test_file, wav_train_list[train_index])
            matches = compute_plot_matching_function_DTW(test_file, training_file_cens_list[train_index][0])
            total = 0
            for (start, finish) in matches:
                total += finish - start
            file_to_match_length[Path(f).stem] = total

        file_to_match_length = {k: v for k, v in sorted(file_to_match_length.items(), key=lambda item: item[1],
                                                        reverse=True)}
        first_pair = next(iter(file_to_match_length.items()))
        path_obj = Path(test_file)
        species = str(path_obj.parents[0]).split('\\')[-1]
        if species in first_pair[0]:
            number_correct += 1

    print(f'Accuracy = {(number_correct/len(wav_test_list))*100}%')


if __name__ == '__main__':
    main()
