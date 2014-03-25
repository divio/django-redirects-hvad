from django.contrib import admin
from redirects_hvad.models import Redirect
from nani.admin import TranslatableAdmin

class RedirectAdmin(TranslatableAdmin):
    list_display = ('old_path',)
    list_filter = ('site',)
    search_fields = ('old_path', 'translations__new_path')
    radio_fields = {'site': admin.VERTICAL}


admin.site.register(Redirect, RedirectAdmin)
