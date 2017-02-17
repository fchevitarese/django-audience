from django.contrib import admin

from .models import Video, Theme, Comment, Thumb


class ThemeAdminInline(admin.TabularInline):
    model = Video.theme.through
    verbose_name = 'Theme'
    verbose_name_plural = 'Themes'


def thumbs_up(modeladmin, request, queryset):
    for video in queryset:
        video.thumbs.create(is_positive=True)


thumbs_up.short_description = 'Give a thumb up'


def thumbs_down(modeladmin, request, queryset):
    for video in queryset:
        video.thumbs.create()


thumbs_down.short_description = 'Give a thumb down'


class VideoAdmin(admin.ModelAdmin):
    exclude = ('theme', )
    list_display = ('title', 'date_uploaded', 'views', 'get_thumbs_up',
                    'get_thumbs_down', 'get_comments', )
    list_filter = ('theme', 'date_uploaded', )
    inlines = (
        ThemeAdminInline,
    )
    actions = [thumbs_up, thumbs_down]


admin.site.register(Video, VideoAdmin)
admin.site.register(Theme)
admin.site.register(Comment)
admin.site.register(Thumb)
