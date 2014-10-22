(function AttachmentsListActions () {


    //
    // Update attachment
    //
    $('.update-action').click(function (e) {
        e.preventDefault();

        var $this = $(this);
        var updateUrl = $this.data('update-url');
        var $attachment = $this.parents('tr');

        var $form = $('form.add-attachment');
        $('.file-attachment-update').find('h4').html($attachment.data('form-update-title'));
        $form.find('input[name="attachment_file"]').prop('disabled', true);
        $form.find('input[name="title"]').val($attachment.data('title'))
                                         .prop('disabled', true);
        $form.find('select[name="filetype"]').val($attachment.data('filetype'));
        $form.find('input[name="author"]').val($attachment.data('author'));
        $form.find('input[name="legend"]').val($attachment.data('legend'));
        $form.find('input[name="starred"]').prop('checked', $attachment.data('starred'));

        return false;
    });


    //
    // Delete single attachment
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
})();



(function AttachmentsForm () {

    var $form = $('form.add-attachment');
    var validate_url = $form.data('validate-url');
    var is_form_valid = false;
    var $file_input = $form.find('input[type="file"]');

    $file_input.on('change', function (e) {
        var chosenFiles = e.currentTarget.files;
        if (chosenFiles.length === 0)
            return;
        var filename = chosenFiles[0].name;
        $form.find('input[name="title"]').val(filename);
    })

    $form.submit(function(e) {
        if (is_form_valid)
            return true;

        var form_data = $form.serialize();
        $.ajax({
            'type': 'POST',
            'url': validate_url,
            'dataType': 'JSON',
            'data': form_data,
            'success': function(errors) {
                is_form_valid = true;

                // File fields content are not sent properly in ajax
                // We make our own check client side
                if ($file_input.val())
                    delete errors[$file_input.attr('name')];

                // If there is at least one remaining error, the form is invalid
                for (var i in errors) {
                    is_form_valid = false;
                    break;
                }

                // Reset form errors
                $form.find('.control-group.error')
                    .removeClass('error')
                    .find('span.help-inline').remove();

                // Submit the form if valid
                if (is_form_valid) {
                    $form.submit();
                    return;
                }

                // Mark errors (mimic bootstrap error marking)
                $.each(errors, function(name, errors) {
                    var elem = $form.find('.controls *[name="' + name + '"]')
                      , elem_id = elem.attr('id')
                      , elem_parent = elem.parent();

                    elem.closest('.control-group').addClass('error');

                    $.each(errors, function(id, error_msg) {
                        $('<span></span>')
                            .addClass('help-inline')
                            .attr('id', 'error_' + (id + 1) + '_' + elem_id)
                            .append($('<strong></strong').text(error_msg))
                            .appendTo(elem_parent)
                    });
                });
            }
        });

        return false;
    });
})();
