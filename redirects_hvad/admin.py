from django.contrib import admin

from hvad.admin import TranslatableAdmin

from .models import Redirect


class RedirectAdmin(TranslatableAdmin):
    list_display = ('old_path',)
    list_filter = ('site',)
    search_fields = ('old_path', 'translations__new_path')
    radio_fields = {'site': admin.VERTICAL}


admin.site.register(Redirect, RedirectAdmin)
