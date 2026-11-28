"""Exercise lifecycle dates, confirmation guards and non-destructive reruns."""
import importlib.util,json,tempfile,unittest
from datetime import datetime
from pathlib import Path
spec=importlib.util.spec_from_file_location('site_updates',Path(__file__).resolve().parents[1]/'scripts/build-site-updates.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Lifecycle(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.original=module.ROOT
  (self.root/'content').mkdir()
  for name in ['index.html','shop.html','content/site-updates.json','content/event-archive.json']:(self.root/name).write_text((self.original/name).read_text())
  module.ROOT=self.root
 def tearDown(self):module.ROOT=self.original;self.temp.cleanup()
 def event(self,**changes):
  data=module.load('content/site-updates.json');data['events'][0].update(changes);module.save('content/site-updates.json',data)
 def test_before_and_exact_end(self):
  module.build(datetime.fromisoformat('2026-12-05T21:59:59+04:00'));self.assertIn('class="mf-ticket-event"',(self.root/'shop.html').read_text())
  module.build(datetime.fromisoformat('2026-12-05T22:00:00+04:00'));self.assertNotIn('class="mf-ticket-event"',(self.root/'shop.html').read_text());self.assertIn('Next announcement coming soon.',(self.root/'index.html').read_text());self.assertIn('pX8Eu15SmY8',(self.root/'index.html').read_text())
 def test_confirmation_guard(self):
  self.event(status='archived')
  with self.assertRaises(ValueError):module.build(datetime.fromisoformat('2026-12-06T10:00:00+04:00'))
  self.event(completion_confirmed=True)
  with self.assertRaises(ValueError):module.build(datetime.fromisoformat('2026-12-04T10:00:00+04:00'))
 def test_archive_once_and_preserve_credits(self):
  self.event(status='archived',completion_confirmed=True);now=datetime.fromisoformat('2026-12-06T10:00:00+04:00');module.build(now)
  data=module.load('content/event-archive.json');record=data['events'][0];self.assertEqual(record['id'],'meetup-2026-12-05');self.assertTrue(any(s['url']=='https://ra.co/events/2595834' for s in record['sources']));record['artists']='Later verified artist';module.save('content/event-archive.json',data)
  module.build(now);data=module.load('content/event-archive.json');self.assertEqual(len([x for x in data['events'] if x['id']==record['id']]),1);self.assertEqual(data['events'][0]['artists'],'Later verified artist')
 def test_new_video_keeps_previous(self):
  data=module.load('content/site-updates.json');data['current_video']=dict(data['current_video'],id='abcdefghijk',title='Verified next release');module.save('content/site-updates.json',data);module.build(datetime.fromisoformat('2026-11-28T12:00:00+04:00'));module.build(datetime.fromisoformat('2026-11-28T12:00:00+04:00'))
  data=module.load('content/site-updates.json');self.assertEqual([x['id'] for x in data['videos']],['abcdefghijk','pX8Eu15SmY8']);self.assertIn('watch?v=pX8Eu15SmY8',(self.root/'shop.html').read_text())
if __name__=='__main__':unittest.main()
