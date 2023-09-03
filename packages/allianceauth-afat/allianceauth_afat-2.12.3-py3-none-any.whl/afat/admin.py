"""
Admin pages configuration
"""

# Django
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

# Alliance Auth AFAT
from afat.models import AFat, AFatLink, AFatLinkType, AFatLog


def custom_filter(title):
    """
    Defining custom filter titles
    :param title:
    :type title:
    :return:
    :rtype:
    """

    class Wrapper(admin.FieldListFilter):
        """
        Wrapper
        """

        def expected_parameters(self):
            """
            Expected parameters
            :return:
            :rtype:
            """

            pass

        def choices(self, changelist):
            """
            Choices
            :param changelist:
            :type changelist:
            :return:
            :rtype:
            """

            pass

        def __new__(cls, *args, **kwargs):
            """
            __new__
            :param args:
            :type args:
            :param kwargs:
            :type kwargs:
            """

            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


# Register your models here.
@admin.register(AFatLink)
class AFatLinkAdmin(admin.ModelAdmin):
    """
    Config for the FAT link model
    """

    list_select_related = ("link_type",)
    list_display = (
        "afattime",
        "creator",
        "fleet",
        "link_type",
        "is_esilink",
        "hash",
        "number_of_fats",
    )
    list_filter = ("is_esilink", ("link_type__name", custom_filter(title="fleet type")))
    ordering = ("-afattime",)
    search_fields = (
        "link_type__name",
        "hash",
        "fleet",
        "creator__profile__main_character__character_name",
        "creator__username",
    )

    def get_queryset(self, request):
        """
        Get the queryset
        :param request:
        :type request:
        :return:
        :rtype:
        """

        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_number_of_fats=Count("afats", distinct=True))

        return queryset

    @admin.display(ordering="_number_of_fats")
    def number_of_fats(self, obj):
        """
        Return the number of FATs per FAT Link
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj._number_of_fats


@admin.register(AFat)
class AFatAdmin(admin.ModelAdmin):
    """
    Config for fat model
    """

    list_display = ("character", "system", "shiptype", "afatlink")
    list_filter = ("character", "system", "shiptype")
    ordering = ("-character",)
    search_fields = (
        "character__character_name",
        "system",
        "shiptype",
        "afatlink__fleet",
        "afatlink__hash",
    )


@admin.register(AFatLinkType)
class AFatLinkTypeAdmin(admin.ModelAdmin):
    """
    Config for the FAT link type model
    """

    list_display = ("id", "_name", "_is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)

    @admin.display(description=_("Fleet Type"), ordering="name")
    def _name(self, obj):
        """
        Rewrite name
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @admin.display(description=_("Is enabled"), boolean=True, ordering="is_enabled")
    def _is_enabled(self, obj):
        """
        Rewrite is_enabled
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.is_enabled

    actions = ("activate", "deactivate")

    @admin.action(description=_("Activate selected fleet types"))
    def activate(self, request, queryset):
        """
        Mark fleet type as active
        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = True
                obj.save()

                notifications_count += 1
            except:  # noqa: E722
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    "Failed to activate {failed} fleet type",
                    "Failed to activate {failed} fleet types",
                    failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    "Activated {notifications_count} fleet type",
                    "Activated {notifications_count} fleet types",
                    notifications_count,
                ).format(notifications_count=notifications_count),
            )

    @admin.action(description=_("Deactivate selected fleet types"))
    def deactivate(self, request, queryset):
        """
        Mark fleet type as inactive
        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = False
                obj.save()

                notifications_count += 1
            except:  # noqa: E722
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    "Failed to deactivate {failed} fleet type",
                    "Failed to deactivate {failed} fleet types",
                    failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    "Deactivated {notifications_count} fleet type",
                    "Deactivated {notifications_count} fleet types",
                    notifications_count,
                ).format(notifications_count=notifications_count),
            )


@admin.register(AFatLog)
class AFatLogAdmin(admin.ModelAdmin):
    """
    Config for the admin log model
    """

    list_display = ("log_time", "log_event", "user", "fatlink_hash", "log_text")
    ordering = ("-log_time",)
    readonly_fields = ("log_time", "log_event", "user", "fatlink_hash", "log_text")
    list_filter = ("log_event",)
    search_fields = (
        "fatlink_hash",
        "user__profile__main_character__character_name",
        "user__username",
    )
