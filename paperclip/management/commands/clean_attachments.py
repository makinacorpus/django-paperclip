import os
from itertools import chain
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.six.moves import input
from paperclip.models import Attachment


PAPERCLIP_ROOT = os.path.join(settings.MEDIA_ROOT, 'paperclip')


def splits(path):
    if path == '/':
        return []
    head, tail = os.path.split(path.rstrip('/'))
    return splits(head + '/') + [path]


def path_cmp(a, b):
    if b.startswith(a):
        return 1
    if a.startswith(b):
        return -1
    return cmp(a, b)


class Command(BaseCommand):
    help = 'Remove obsolete attached files from disk'
    option_list = BaseCommand.option_list + (
        make_option(
            '--noinput', action='store_false',
            dest='interactive', default=True,
            help="Do NOT prompt the user for input of any kind."
        ),
    )

    def handle(self, *args, **options):
        interactive = options['interactive']
        verbosity = int(options.get('verbosity', 1))
        files = Attachment.objects.order_by('attachment_file')
        files = files.values_list('attachment_file', flat=True)
        to_keep = [os.path.join(settings.MEDIA_ROOT, path)
                   for f in files for path in splits(f)]
        to_keep = list(set(to_keep))
        to_keep.sort(path_cmp)
        to_delete = []
        for root, dirs, files in os.walk(PAPERCLIP_ROOT):
            for basename in chain(files, [d + '/' for d in dirs]):
                f = os.path.join(root, basename)
                if f not in to_keep:
                    to_delete.append(f)
        to_delete.sort(path_cmp)
        if not to_delete and verbosity >= 1:
            self.stdout.write("No obsolete attached file to "
                              "remove from disk.\n")
        if to_delete and interactive:
            self.stdout.write("You have requested to remove obsolete attached "
                              "files from disk.\n\n")
            for f in to_delete:
                self .stdout.write("    {}".format(f))
            confirm = input("""
This will permanently delete these files above!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """)
            if confirm != 'yes':
                raise CommandError("Removing obsolete attached files "
                                   "cancelled.")
        for path in to_delete:
            if path.endswith('/'):
                os.rmdir(path)
            else:
                os.remove(path)
        if to_delete and verbosity >= 1:
            values = {
                'n': len(to_delete),
                's': "s" if len(to_delete) > 1 else "",
            }
            self.stdout.write("{n} obsolete attached file{s} removed from "
                              "disk.\n".format(**values))
