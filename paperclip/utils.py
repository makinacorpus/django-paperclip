import mimetypes


def mimetype(attachment_file):
    mt = mimetypes.guess_type(attachment_file.name, strict=True)[0]
    if mt is None:
        return 'application', 'octet-stream'
    return mt.split('/')


def is_an_image(mimetype):
    return mimetype[0].startswith('image')
