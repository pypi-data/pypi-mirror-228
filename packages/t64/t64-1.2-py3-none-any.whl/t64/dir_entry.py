import struct


class DirEntry:
    DTYPE_STR = ('DEL', 'SEQ', 'PRG', 'USR', 'REL', '???', '???', '???')

    def __init__(self, image, name, file_type, disk_type, start_addr, end_addr, img_start):
        self.image = image
        self.name = name
        self.file_type = file_type
        self._disk_type = disk_type
        self.start_addr = start_addr
        self.end_addr = end_addr
        self.img_start = img_start

    @property
    def disk_type(self):
        return self.DTYPE_STR[self._disk_type & 7]

    @property
    def protected(self):
        return False

    @property
    def closed(self):
        return True

    def contents(self):
        data = b''
        if self.disk_type == 'PRG':
            data = struct.pack('<H', self.start_addr)
        img_end = self.img_start+self.end_addr-self.start_addr
        data += self.image.map[self.img_start:img_end]
        return data
