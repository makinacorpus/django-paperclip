Paperclip
=========

Add attachments to Django models, used `MapEntity <https://github.com/makinacorpus/django-mapentity>`_.

=======
INSTALL
=======

::

    pip install paperclip

=====
USAGE
=====

* Add ``paperclip`` to ``INSTALLED_APPS``

* Include urls

::

    urlpatterns = patterns(
        '',
        ...
        url(r'^paperclip/', include('paperclip.urls')),
        ...
    )

* Include scripts in template

::

    <script src="{% static "paperclip/bootstrap-confirm.js" %}" type="text/javascript"></script> 
    <script src="{% static "paperclip/spin.min.js" %}" type="text/javascript"></script> 
    <script src="{% static "paperclip/paperclip.js" %}" type="text/javascript"></script> 

If you use bootstrap 3, please include ``paperclip/bootstrap-3-confirm.js`` instead of ``paperclip/bootstrap-confirm.js``.

* Include list and form in template

::

    {% include 'paperclip/attachment_list.html' with attachment_form_next=object.get_detail_url %}

=======
AUTHORS
=======

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com


=======
LICENSE
=======

    * LGPL
