"""当前来源接口的核心和错误路径。"""
import unittest,tempfile
from pathlib import Path
from common import read,Releases,money,digest

class CommonTests(unittest.TestCase):
    def test_snapshot_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            store=Releases(d);raw={'value':'20.10'};key=store.publish(raw)
            self.assertEqual(store.open(key),raw);self.assertEqual(store.publish(raw),key)
            Path(d,key).write_bytes(b'changed')
            with self.assertRaises(ValueError):store.open(key)
    def test_exact_money(self):
        self.assertEqual(str(money('0.1')+money('0.2')),'0.3')
        with self.assertRaises(ValueError):money(float('nan'))

from design import validate,draw,local_space
from network import exposure
class DomainTests(unittest.TestCase):
    def test_design_and_neighbor(self):
        d=read();self.assertEqual(exposure(d)['b'],[0,1]);self.assertEqual(exposure(d)['f'],[0,0])
        self.assertEqual(draw(d,42),draw(d,42));self.assertAlmostEqual(sum(p for _,p in local_space(d['groups'][0])),1)
    def test_cross_group_and_incomplete(self):
        d=read();d['edges'].append(['a','d'])
        with self.assertRaises(ValueError):exposure(d)
        d=read();del d['outcomes']['a']
        with self.assertRaises(ValueError):validate(d)
