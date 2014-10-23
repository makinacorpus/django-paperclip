(function () {
    //
    // Update attachment
    //
    $('.update-action').click(function (e) {
        e.preventDefault();

        var $this = $(this);
        var updateUrl = $this.data('update-url');

        var $form = $('.file-attachment-form');
        var spinner = new Spinner({length: 3, radius: 5, width: 2}).spin($form[0]);
        $.get(updateUrl, function (html) {
            $form.find('.create').hide();
            $form.find('.update').html(html);
            spinner.stop();
            // Update title on file change
            watchFileInput();
            // On cancel, restore Create form
            $('#button-id-cancel').click(function () {
                $form.find('.update').html('');
                $form.find('.create').show();
            });
        });

        return false;
    });


    //
    // Delete single attachment with confirm modal
    //
    $('.delete-action').click(function (e) {
        e.preventDefault();

        var $this = $(this);
        var deleteUrl = $this.data('delete-url');
        var $attachments = $this.parents('tbody');
        var $attachment = $this.parents('tr');

        $('.confirm-modal').confirmModal({
            heading: $attachments.data('confirm-delete-heading'),
            body: $attachments.data('confirm-delete-msg').replace('{file}', $attachment.data('title')),
            callback: function() {
                window.location = deleteUrl;
            }
        });

        return false;
    });


    //
    // Click to star/unstar attachments
    //
    $('a.star, a.unstar').click(function (e) {
        var $this = $(this);
        e.preventDefault();

        // Pass parameter to unstar (see views.py code)
        var starUrl = $this.data('star-url');
        if ($this.hasClass('unstar'))
            starUrl += '?unstar';

        // Show spinner on link while AJAX
        var spinner = new Spinner({length: 3, radius: 5, width: 2}).spin(this);
        $.getJSON(starUrl)
         .always(function () {
            spinner.stop();
         })
         .done(function (data) {
            // Replace the <img> icon after success
            var starIcon = $this.find('img').attr('src');
            starIcon = starIcon.replace(data.starred ? 'off' : 'on',
                                        data.starred ? 'on' : 'off');
            $this.find('img').attr('src', starIcon);
            $this.toggleClass('unstar star');
        });

        return false;
    });

    //
    // Attachment form
    //
    function watchFileInput () {
        var $form = $('form.attachment');
        var $file_input = $form.find('input[type="file"]');

        $file_input.on('change', function (e) {
            var chosenFiles = e.currentTarget.files;
            if (chosenFiles.length === 0)
                return;
            var filename = chosenFiles[0].name;
            // Remove extension from filename
            filename = filename.replace(/\.[^/.]+$/, "");
            $form.find('input[name="title"]').val(filename);
        });
    }

    watchFileInput();
})();
