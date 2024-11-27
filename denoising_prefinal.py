import soundfile as sf
import numpy as np
from segment import inference
import os

def get_non_contributing_indices(arrays, top_n, index):
    cur_values = [(arrays[i][index], i) for i in range(len(arrays))]
    cur_values = sorted(cur_values, key=lambda x: x[0], reverse=True)
    print(top_n, cur_values)
    # if top_n > 1 and float(cur_values[top_n][0]) - float(cur_values[top_n + 1][0]) < 0.1 and float(cur_values[top_n + 1][0]) > 0:
    if top_n > 1:
        new_top_n = top_n
        for non_contributing in cur_values[top_n + 1:]:
            if float(non_contributing[0]) and (float(cur_values[top_n][0]) / float(non_contributing[0])) >= 0.5:
                new_top_n += 1
        return [x[1] for x in cur_values[new_top_n:]]
    return [x[1] for x in cur_values[top_n:]]

PATH_TO_AUDIO_DIR = "C:\\Users\\nickh\\Desktop\\audios\\new_test_20_11"
WINDOW_SIZE = int(0.1 * 48000)
STRIDE = int(0.1 * 48000)
RATE_ = 48000

if os.path.isfile(f"{PATH_TO_AUDIO_DIR}\\combined.wav"):
    os.remove(f"{PATH_TO_AUDIO_DIR}\\combined.wav")

audios = []
print(PATH_TO_AUDIO_DIR)
for audio_name in os.listdir(PATH_TO_AUDIO_DIR):
    if os.path.isfile(f"{PATH_TO_AUDIO_DIR}\\{audio_name}"):
        audio, rate = sf.read(f"{PATH_TO_AUDIO_DIR}\\{audio_name}")
        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)  
        audios.append((audio, rate))

combined = np.sum(np.array([x[0] for x in audios]), axis=0)
sf.write(f"{PATH_TO_AUDIO_DIR}\\combined.wav", combined, rate)
segment_data = inference(f"{PATH_TO_AUDIO_DIR}\\combined.wav")

# needed_segments = {"0": [], "1": [], "2": [], "3": []}
# start = 0
# sec_sum = 0
# prev_key, cur_key = None, None
# for chunk in segment_data:
#     for segment in chunk:
#         if not prev_key:
#             prev_key = str(segment[1].count("1"))
#             sec_sum += segment[0]
#             continue
#         cur_key = str(segment[1].count("1"))
#         if cur_key == prev_key:
#             sec_sum += segment[0]
#         else:
#             needed_segments[prev_key].append([start, start + sec_sum])
#             start += sec_sum
#             sec_sum = segment[0]
#             prev_key = cur_key


# if cur_key == prev_key:
#     needed_segments[prev_key].append([start, start + sec_sum])
# else:
#     needed_segments[str(segment[1].count("1"))].append([start, start + sec_sum])

needed_segments = []
start = 0
sec_sum = 0
prev_key, cur_key = None, None
for chunk in segment_data:
    for segment in chunk:
        if not prev_key:
            prev_key = str(segment[1].count("1"))
            sec_sum += segment[0]
            continue
        cur_key = str(segment[1].count("1"))
        if cur_key == prev_key:
            sec_sum += segment[0]
        else:
            needed_segments.append([prev_key, [start, start + sec_sum]])
            start += sec_sum
            sec_sum = segment[0]
            prev_key = cur_key

# print(segment_data)
# print("==============================================")
# print(needed_segments)

audio_windows = [[] for _ in range(len(audios))]
for i, (audio, rate) in enumerate(audios):
    for j in range(int((len(audios[0][0]) - WINDOW_SIZE) / STRIDE) + 1):
        audio_windows[i].append(np.max(audio[STRIDE * j : STRIDE * j + WINDOW_SIZE]))
    audio_windows[i] = np.array(audio_windows[i])

j = 0
for i in range(int((len(audios[0][0]) - WINDOW_SIZE) / STRIDE) + 1):
    print(j)
    print(len(needed_segments))
    if j < (len(needed_segments) - 1) and (STRIDE * i) / RATE_ > needed_segments[j][1][1]:
        j += 1
    if needed_segments[j][0] == "0":
        continue
    else:
        amount = int(needed_segments[j][0])
        indices = get_non_contributing_indices(audio_windows, amount, i)
        print(needed_segments[j])
        print(indices)
        for idx in indices:
            audios[idx][0][STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0

for i, (audio, rate) in enumerate(audios):
    sf.write(f"audio_{i}_processed.wav", audio, rate)


    # if key == "0":
    #     continue
    # elif key == "1":
    #     if diff_0[i] > 0 and diff_1[i] > 0:
    #         for i in range(1, len(audios[0])):
    #             audios[i][0][STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0
    #     elif diff_0[i] < 0 and diff_1[i] < 0 and diff_2[i] > 0:
    #         for i in range(len(audios[0])):
    #             if i == 1:
    #                 continue
    #             audios[i][0][STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0
    #     else:
    #         for i in range(len(audios[0]) - 1):
    #             audios[i][0][STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0
                
# for i in range(int((len(post_audio[0]) - WINDOW_SIZE) / STRIDE) + 1):
#     if (STRIDE * i) / rate > needed_segments[j][1]:
#         j += 1
    
    

    
   
   
# if (STRIDE * i) / rate > needed_segments[j][1]:
#     j += 1   
# if not ((STRIDE * i)  / rate >= needed_segments[j][0] and (STRIDE * i + WINDOW_SIZE) / rate <= needed_segments[j][1]):
#     continue
# if diff[i] == 0:
#     continue
# elif diff[i] > 0:
#     audio_1[STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0
# else:
#     audio_2[STRIDE * i : STRIDE * i + WINDOW_SIZE] = 0
