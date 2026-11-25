import importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('sync',Path(__file__).parents[1]/'scripts/sync-radio.py')
sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
class SyncTest(unittest.TestCase):
 def test_canonical_artist_name(self):
  for value in ["Neroli Kid", "NEROLI KID", "nerolikid", "Nerolikid"]:
   self.assertEqual(sync.canonical_artist_name(value),"Nerolikid")
  self.assertEqual(sync.metadata("NEROLI KID - PEDALBOARD.mp3"),("Nerolikid","PEDALBOARD"))
 def test_nature_edition_filename_metadata(self):
  for name,track in [('1-m f n e 2 _ 2 -1.wav',1),('Untitled 14-m f n e 2 _ 2 -14 [2026-11-24 163448].wav',14)]:
   self.assertEqual(sync.metadata(name),('AGAVA × Spilled Ambiences × Wayward Atom',f'Nature Edition 2 · Track {track:02}'))
 def test_incremental_add_and_failure_preserves_playlist(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); fixture=root/'fixture.mp3'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=duration=0.1','-c:a','libmp3lame',str(fixture)],check=True)
   sync.RADIO=root/'radio'
   def download(**kw):Path(kw['output']).write_bytes(fixture.read_bytes())
   first=[{'id':'one','path':'Artist - First.mp3'}]
   with patch.object(sync.gdown,'download',side_effect=download) as dl:
    sync.sync(first);self.assertEqual(dl.call_count,1)
    self.assertEqual((sync.RADIO/'media/one.mp3').read_bytes(),fixture.read_bytes())
    sync.sync(first);self.assertEqual(dl.call_count,1)
    sync.sync(first+[{'id':'two','path':'Artist - Second.mp3'}]);self.assertEqual(dl.call_count,2)
   before=(sync.RADIO/'tracks.json').read_bytes()
   self.assertEqual(len(json.loads(before)['tracks']),2)
   with patch.object(sync.gdown,'download',side_effect=RuntimeError('offline')):
    with self.assertRaises(RuntimeError):sync.sync(first+[{'id':'three','path':'Artist - Third.mp3'}])
   self.assertEqual((sync.RADIO/'tracks.json').read_bytes(),before)
if __name__=='__main__':unittest.main()
