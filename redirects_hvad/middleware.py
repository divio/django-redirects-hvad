import operator

from django.http import HttpResponseGone
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import translation

from redirects_hvad.models import Redirect


# when true, requests for /language/some-url/ become /some-url/
IGNORE_PREFIX = getattr(settings, 'REDIRECTS_IGNORE_LANGUAGE_PREFIX', False)


class RedirectFallbackMiddleware(object):

    def process_response(self, request, response):

        if response.status_code != 404:
            return response # No need to check for a redirect for non-404 responses.

        path = request.path

        language_prefix = translation.get_language_from_path(request.path_info)

        if IGNORE_PREFIX and language_prefix:
            # strip the language prefix, by getting the length of the language
            # and adding 2 to it (initial / and trailing /),
            # we then slice the path
            path = "/" + "/".join(path.split("/")[len(language_prefix):])

        queries = [Q(old_path__iexact=path)]

        if settings.APPEND_SLASH and path.endswith('/'):
            queries.append(Q(old_path__iexact=path[:-1]))

        try:
            r = Redirect.objects.get(reduce(operator.or_, queries), site=settings.SITE_ID)
        except Redirect.DoesNotExist:
            pass
        else:
            language = language_prefix or translation.get_language_from_request(request)

            with translation.override(language):
                # give priority to the current language
                new_path = r.lazy_translation_getter('new_path')

            if new_path:
                permanent = r.lazy_translation_getter('redirect_type') == r.PERMANENT
                response = redirect(new_path, permanent=permanent)
            else:
                response = HttpResponseGone()

        return response
