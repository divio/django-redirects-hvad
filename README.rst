django-redirects-hvad
=====================

This is a modified version of Django's ``django.contrib.redirects`` app that
supports language dependant target URLs, using ``django-hvad``.

This is useful for cases in which another middleware strips the language
prefix from the URL, like django CMS.