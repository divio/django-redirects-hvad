from django.db import models
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

from hvad.models import TranslatableModel, TranslatedFields


class Redirect(TranslatableModel):
    PERMANENT = 301
    TEMPORARY = 302

    REDIRECT_TYPES = (
        (PERMANENT, _('Permanent (301)')),
        (TEMPORARY, _('Temporary (302)')),
    )

    site = models.ForeignKey(
        to=Site,
        verbose_name=_('site'),
        related_name='redirects_hvad_set'
    )
    old_path = models.CharField(
        verbose_name=_('redirect from'),
        max_length=200,
        db_index=True,
        help_text=_("This should be an absolute path, excluding the domain name. Example: '/events/search/'.")
    )
    translations = TranslatedFields(
        new_path = models.CharField(
            verbose_name=_('redirect to'),
            max_length=200,
            blank=True,
            help_text=_("This can be either an absolute path (as above) or a full URL starting with 'http://'.")
        ),
        redirect_type=models.IntegerField(
            verbose_name=_('type'),
            choices=REDIRECT_TYPES,
            default=REDIRECT_TYPES[1][0],
            help_text=mark_safe(
                '<a href="http://moz.com/learn/seo/redirection">http://moz.com/learn/seo/redirection</a>'
            ),
        ),
    )

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        unique_together=(('site', 'old_path'),)
        ordering = ('old_path',)
    
    def __unicode__(self):
        return "%s ---> %s (%s)" % (self.old_path, self.lazy_translation_getter('new_path', ugettext('None')), self.lazy_translation_getter('redirect_type', ugettext('None')))

    def get_absolute_url(self):
        return self.lazy_translation_getter('new_path', '/')
