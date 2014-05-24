from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _, ugettext

from hvad.models import TranslatableModel, TranslatedFields


class Redirect(TranslatableModel):
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
    )

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        unique_together=(('site', 'old_path'),)
        ordering = ('old_path',)
    
    def __unicode__(self):
        return "%s ---> %s" % (self.old_path, self.lazy_translation_getter('new_path', ugettext('None')))

    def get_absolute_url(self):
        return self.lazy_translation_getter('new_path', '/')
