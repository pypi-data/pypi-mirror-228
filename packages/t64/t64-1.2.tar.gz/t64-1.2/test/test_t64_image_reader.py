import unittest
from pathlib import Path
from unittest.mock import patch, mock_open, Mock

from t64.t64_image_reader import T64ImageReader


@patch('t64.t64_image_reader.is_valid_image')
class TestT64ImageReader(unittest.TestCase):

    def setUp(self):
        self.map = bytearray(b'C64 tape image file'.ljust(32, b'\x00'))
        self.map += b'\x01\x01\x02\x00\x01\x00\x00\x00'
        self.map += b'tape name'.ljust(24, b' ')
        self.map += b'\x00'*32
        with patch.object(Path, 'open', mock_open(read_data=bytes(self.map))):
            self.image = T64ImageReader(Path())
        self.image.filepath = Mock()

    def test_header(self, mock_valid):
        mock_valid.return_value = True
        self.map += b'\x00'*32
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.open()
        self.assertEqual(self.image.tape_name, b'tape name'.ljust(24, b' '))
        self.assertEqual(self.image.max_entries, 2)
        self.assertEqual(self.image.used_entries, 1)

    def test_entries(self, mock_valid):
        mock_valid.return_value = True
        self.map += b'\x01\x82\x00\x10\x00\x20'.ljust(16, b'\x00')
        self.map += b'file name'.ljust(16, b' ')
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.open()
        self.assertEqual(len(self.image.entries), 1)
        self.assertIsNotNone(self.image.entry(b'file name'))
        self.assertIsNone(self.image.entry(b'not found'))

    def test_directory(self, mock_valid):
        mock_valid.return_value = True
        self.map += b'\x01\x82\x00\x10\x00\x20'.ljust(16, b'\x00')
        self.map += b'file name'.ljust(16, b' ')
        with patch('t64.t64_image_reader.mmap.mmap') as mock_mmap:
            mock_mmap.return_value = self.map
            self.image.open()
        dir_list = [l for l in self.image.directory(encoding='ascii')]
        self.assertEqual(dir_list, ['0 "tape name               "', '17   "file name"        PRG'])
