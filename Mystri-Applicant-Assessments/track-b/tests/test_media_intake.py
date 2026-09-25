import base64
import unittest
from pathlib import Path

from media_intake import assess_attachment, assess_demo_pack


FIX = Path(__file__).resolve().parent / 'fixtures'


class MediaIntakeTests(unittest.TestCase):
    def test_png_ihdr_dimensions(self):
        raw = base64.standard_b64decode(FIX.joinpath('tiny.png.b64').read_text().strip())
        r = assess_attachment('x.png', raw)
        self.assertEqual(r.detected_format, 'png')
        self.assertEqual((r.width, r.height), (1, 1))

    def test_heic_routes_human(self):
        data = b'\x00\x00\x00\x18ftypheic\x00' + b'\x00' * 40
        r = assess_attachment('photo.heic', data)
        self.assertEqual(r.routing, 'human_review')
        self.assertEqual(r.detected_format, 'heic')

    def test_unknown_rejected(self):
        r = assess_attachment('x.bin', b'\x00\x01\x02\x03' * 50)
        self.assertEqual(r.routing, 'reject')

    def test_demo_pack_nonempty(self):
        self.assertGreaterEqual(len(assess_demo_pack()), 3)


if __name__ == '__main__':
    unittest.main()
