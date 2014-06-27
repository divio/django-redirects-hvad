from django.contrib import admin

from hvad.admin import TranslatableAdmin

from .models import Redirect


class RedirectAdmin(TranslatableAdmin):
    list_filter = ('site', 'translations__redirect_type')
    search_fields = ('old_path', 'translations__new_path')
    radio_fields = {'site': admin.VERTICAL}
    fieldsets = (
        (None, {
            'fields': ('site', 'old_path')
        }),
        ('Target (language dependent)', {
            'fields': (('new_path', 'redirect_type'), )
        }),
    )


admin.site.register(Redirect, RedirectAdmin)
