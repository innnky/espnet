import os
from collections import defaultdict

if not os.path.exists("data"):
  os.mkdir("data")
  os.mkdir("data/train")
wavscp = open("data/train/wav.scp","w")
spk2utt = open("data/train/spk2utt","w")
utt2spk = open("data/train/utt2spk","w")
textout = open("data/train/text","w")


speaker_utt_dict = defaultdict(list)
utt_speaker_dict = {}
for speaker in sorted(os.listdir("raw")):
  if speaker.startswith("."):
    continue
  transcript_file = open(f"raw/{speaker}/transcription.txt")
  for line in transcript_file.readlines():
    wavpath, text = line.strip().split("|")
    uttname = wavpath
    utt_speaker_dict[uttname] = speaker
    speaker_utt_dict[speaker].append(uttname)
    wavscp.write(f"{uttname} {wavpath}\n")
    utt2spk.write(f"{uttname} {speaker}\n")
    textout.write(f"{uttname} {text}\n")

for speaker, uttlist in speaker_utt_dict.items():
  utts = " ".join(uttlist)
  spk2utt.write(f"{speaker} {utts}\n")
wavscp.close()
spk2utt.close()
utt2spk.close()
textout.close()
