from django.contrib import admin
from typing import *

from .models import Book, Borrow


class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
    )
    search_fields = ()
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Book, BookAdmin)
