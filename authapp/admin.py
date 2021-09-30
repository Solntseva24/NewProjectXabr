from django.contrib import admin
from .models import XabrUser


class XabrUserAdmin(admin.ModelAdmin):
    """переопределение модели XabrUser, отображающейся в административной панели"""

    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_editable = ('is_active',)

    def get_queryset(self, request):
        """функция, которая скрывает суперпользователя в административной панели
        для всех отсальных пользователей"""

        qs = super(XabrUserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """функция, органичивающая доступ можератора к редактированию пользователей"""

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['username'].disabled = True
            form.base_fields['password'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['avatar'].disabled = True
            form.base_fields['age'].disabled = True
            form.base_fields['email'].disabled = True
            form.base_fields['activation_key'].disabled = True
            form.base_fields['activation_key_expires'].disabled = True
            form.base_fields['like_quantity'].disabled = True
            form.base_fields['is_staff'].disabled = True
            form.base_fields['groups'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['last_login'].disabled = True
            form.base_fields['first_name'].disabled = True
            form.base_fields['last_name'].disabled = True
            form.base_fields['date_joined'].disabled = True
            form.base_fields['aboutMe'].disabled = True
        return form


admin.site.register(XabrUser, XabrUserAdmin)
