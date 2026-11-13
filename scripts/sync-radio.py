#!/usr/bin/env python3
"""Incremental public Drive -> MP3 + playlist. No credentials, no embedded audio."""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import gdown

ROOT = Path(__file__).resolve().parents[1]
RADIO = ROOT / 'radio'
FOLDER = '1U9dLhBoj3UwKXGvL6SrDRJlKNa8NfhYS'

def metadata(name):
    name = re.sub(r'^Copy of\s+', '', Path(name).stem, flags=re.I).strip()
    name = name.replace('_', ' ')
    if name.lower().startswith('modular friends'):
        return 'Modular Friends', name
    parts = re.split(r'\s*[-–—]\s*', name, maxsplit=1)
    if len(parts) == 2:
        artist, title = parts
    elif ' morigi ' in name.lower():
        artist, title = re.split(r'\s+morigi\s+', name, maxsplit=1, flags=re.I)
        title = 'Morigi · ' + title
    else:
        artist, title = 'Modular Friends', name
    artist = re.sub(r'AGAVAxMASA', 'AGAVA × MASA TRIPPIN', artist, flags=re.I)
    artist = re.sub(r'\s+x\s+', ' × ', artist, flags=re.I)
    return artist.strip(), title.strip()

def probe(path):
    result = subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=codec_name:format=duration:format_tags=artist,title','-of','json',str(path)], capture_output=True,text=True,check=True,timeout=30)
    data = json.loads(result.stdout)
    if not data.get('streams') or float(data.get('format',{}).get('duration',0)) <= 0:
        raise ValueError('No playable audio stream')
    return data

def sync(entries=None):
    RADIO.mkdir(exist_ok=True)
    media = RADIO / 'media'; media.mkdir(exist_ok=True)
    if entries is None:
        entries = gdown.download_folder(id=FOLDER, skip_download=True, quiet=True, use_cookies=False, timeout=45)
        entries = [{'id': f.id, 'path': f.path} for f in entries]
    candidates = [f for f in entries if Path(f['path']).suffix.lower() in {'.mp3','.wav'}]
    if not candidates:
        raise RuntimeError('No public audio found; preserving the published playlist.')
    seen = set(); tracks = []; errors = []
    for item in sorted(candidates,key=lambda f:f['id']):
        fid = item['id']
        if fid in seen: continue
        if not re.fullmatch(r'[\w-]+',fid): raise ValueError('Invalid Drive ID')
        seen.add(fid)
        target = media / (fid + '.mp3')
        try:
            if not target.exists():
                with tempfile.TemporaryDirectory(prefix='mf-radio-') as tmp:
                    source = Path(tmp) / ('source' + Path(item['path']).suffix.lower())
                    gdown.download(id=fid,output=str(source),quiet=True,use_cookies=False,timeout=60,retries=1)
                    probe(source)
                    ready = Path(tmp) / 'ready.mp3'
                    if source.suffix == '.mp3':
                        shutil.copyfile(source,ready)
                    else:
                        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(source),'-map','0:a:0','-vn','-c:a','libmp3lame','-b:a','192k',str(ready)],check=True,timeout=600)
                    info = probe(ready)
                    if info['streams'][0]['codec_name'] != 'mp3' or ready.stat().st_size >= 90*1024*1024:
                        raise ValueError('MP3 exceeds web publishing limits or has incorrect format')
                    shutil.copyfile(ready,target)
                print('Prepared',fid,flush=True)
            info = probe(target)
            artist,title = metadata(item['path'])
            tags = info.get('format',{}).get('tags',{})
            tracks.append({'id':fid,'artist':tags.get('artist') or artist,'title':tags.get('title') or title,'src':'media/'+target.name,'duration':round(float(info['format']['duration']),2)})
        except Exception as error:
            errors.append(fid)
            print('Unable to prepare',fid,type(error).__name__,flush=True)
    # Fail closed: never publish an incomplete or empty replacement after a sync failure.
    if errors: raise RuntimeError(f'{len(errors)} tracks failed; previous playlist retained')
    if sum((media/(t['id']+'.mp3')).stat().st_size for t in tracks) > 850*1024*1024:
        raise RuntimeError('Radio would exceed site size budget')
    previous = json.loads((RADIO/'tracks.json').read_text()) if (RADIO/'tracks.json').exists() else {}
    if tracks != previous.get('tracks'):
        data = {'updatedAt':datetime.now(timezone.utc).isoformat(),'tracks':tracks}
        temp = RADIO/'tracks.json.tmp'; temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(RADIO/'tracks.json')
    # Remove only obsolete generated files, after a complete successful sync.
    for path in media.glob('*.mp3'):
        if path.stem not in seen: path.unlink()
    print(f'Sync verified: {len(tracks)} tracks',flush=True)

if __name__ == '__main__': sync()
