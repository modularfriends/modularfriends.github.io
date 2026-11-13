import importlib.util,json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('sync',Path(__file__).parents[1]/'scripts/sync-radio.py')
sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
class SyncTest(unittest.TestCase):
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
