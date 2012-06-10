# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.redirects.models import Redirect as DjangoRedirect
from redirects_hvad.models import Redirect


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--language',
            action='store',
            dest='language',
            help='the language that translations should be created for'
        ),
        make_option('--all',
            action='store_true',
            dest='all',
            default=True,
            help='create translations for all languages'
        ),
    )

    def handle(self, *args, **options):
        if 'django.contrib.redirects' not in settings.INSTALLED_APPS:
            raise CommandError("'django.contrib.redirects' not in INSTALLED_APPS")
        if not (options.get('all') or options.get('language')):
            raise CommandError('use --language to select a single language or --all for all languages')
        if options.get('all'):
            languages = [l[0] for l in settings.LANGUAGES]
        else:
            languages = [options.get('language')]
        i = 0
        for i, django_redirect in enumerate(DjangoRedirect.objects.all()):
            redirect, created = Redirect.objects.get_or_create(
                site_id=django_redirect.site_id,
                old_path=django_redirect.old_path,
            )
            for language in languages:
                Redirect._meta.translations_model.objects.get_or_create(
                    master=redirect,
                    language_code=language,
                    new_path = django_redirect.new_path
                )
        self.stderr.write('Copied %d redirects' % i)
