import os
from collections import defaultdict

language = "[JA]"
if not os.path.exists("data"):
  os.mkdir("data")
  os.mkdir("data/train")
wavscp = open("data/train/wav.scp","w")
spk2utt = open("data/train/spk2utt","w")
utt2spk = open("data/train/utt2spk","w")
textout = open("data/train/text","w")
utt2spk_list = []
n = 0
speaker_utt_dict = defaultdict(list)
utt_speaker_dict = {}



def zh_ja_mixture_cleaner(text):
    import re
    from japanese import japanese_to_romaji_with_accent
    from mandarin import chinese_to_romaji

    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_romaji(chinese_text[4:-4])
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = japanese_to_romaji_with_accent(
            japanese_text[4:-4]).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match('[A-Za-zɯɹəɥ→↓↑]', text[-1]):
        text += '.'
    print(text)
    return text

for speaker in sorted(os.listdir("raw")):
  if speaker.endswith("_JA"):
    language = "[JA]"
  elif speaker.endswith("_ZH"):
    language = "[ZH]"
  else:
    print("不支持的语言,或未指定语言后缀")
    continue
  speaker = speaker[:-3]
  uttid = 0
  if speaker.startswith("."):
    continue
  transcript_file = open(f"raw/{speaker}/transcription.txt")
  for line in transcript_file.readlines():
    wavpath, text = line.strip().split("|")
    text = language + text + language
    text = zh_ja_mixture_cleaner(text)

    uttname = speaker + "%06d" % uttid
    utt_speaker_dict[uttname] = speaker
    speaker_utt_dict[speaker].append(uttname)
    wavscp.write(f"{uttname} {wavpath}\n")
    utt2spk_list.append(f"{uttname} {speaker}\n")
    textout.write(f"{uttname} {text}\n")
    n += 1
    uttid += 1


for speaker, uttlist in speaker_utt_dict.items():
  utts = " ".join(uttlist)
  spk2utt.write(f"{speaker} {utts}\n")

for item in sorted(utt2spk_list):
  utt2spk.write(item)


wavscp.close()
spk2utt.close()
utt2spk.close()
textout.close()


os.system(f"utils/subset_data_dir.sh --first data/train {n} data/tr_no_dev")
os.system(f"utils/subset_data_dir.sh --first data/train 5 data/deveval")
os.system(f"utils/subset_data_dir.sh --first data/train 5 data/dev")
os.system(f"utils/subset_data_dir.sh --first data/train 5 data/eval1")
