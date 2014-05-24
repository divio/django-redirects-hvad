import operator

from django.http import HttpResponseGone
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect

from redirects_hvad.models import Redirect


class RedirectFallbackMiddleware(object):

    def process_response(self, request, response):

        if response.status_code != 404:
            return response # No need to check for a redirect for non-404 responses.

        path = request.get_full_path()

        queries = [Q(old_path__iexact=path)]

        if settings.APPEND_SLASH and path.endswith('/'):
            queries.append(Q(old_path__iexact=path[:-1]))

        try:
            r = Redirect.objects.get(reduce(operator.or_, queries), site=settings.SITE_ID)
        except Redirect.DoesNotExist:
            pass
        else:
            if r.new_path == '':
                return HttpResponseGone()
            return redirect(r.new_path, permanent=True)

        # No redirect was found. Return the response.
        return response
