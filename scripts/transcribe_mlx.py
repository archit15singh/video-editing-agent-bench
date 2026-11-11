import json,time,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
os.environ['HF_HOME']=str(root/'.cache/huggingface')
import mlx_whisper
start=time.monotonic()
result=mlx_whisper.transcribe(str(root/'fixtures/generated/source.mp4'),path_or_hf_repo='mlx-community/whisper-base.en-mlx',word_timestamps=True,language='en')
result['elapsed_seconds_including_first_model_load']=time.monotonic()-start
(root/'results/asr/mlx-whisper.json').write_text(json.dumps(result,indent=2))
print(result['text'])
