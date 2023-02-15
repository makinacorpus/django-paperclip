from paperclip.forms import AttachmentForm


class TestAttachmentForm(AttachmentForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.redirect_on_error = True
