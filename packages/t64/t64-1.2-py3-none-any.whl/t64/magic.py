
T64_MAGICS = (
    b'C64 tape image file',
    b'C64S tape file',
    b'C64S tape image file'
)


def is_valid_image(file_path):
    with file_path.open('rb') as fileh:
        magic = fileh.read(32)
    magic = magic.rstrip(b'\x00')
    return any([magic.startswith(m) for m in T64_MAGICS])
