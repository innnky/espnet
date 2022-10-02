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
for speaker in sorted(os.listdir("raw")):
  uttid = 0
  if speaker.startswith("."):
    continue
  transcript_file = open(f"raw/{speaker}/transcription.txt")
  for line in transcript_file.readlines():
    wavpath, text = line.strip().split("|")
    text = language + text + language
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
