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
