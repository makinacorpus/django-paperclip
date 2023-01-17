import magic


def mimetype(attachment_file):
    attachment_file.file.seek(0)
    mt = magic.from_buffer(attachment_file.file.read(2048), mime=True)
    return mt


def is_an_image(mimetype):
    return False if not mimetype else mimetype.split('/')[0].startswith('image')

