from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.forms import ModelForm

from user.models import Categories, User


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ("id", "email", "is_staff")
    ordering = ("id", "email")
    list_filter = ("is_staff",)
    search_fields = ("email",)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'balance', 'categories')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}
         ),
    )

    filter_horizontal = ()


class CustomCategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    ordering = ("id", "name")
    search_fields = ("id", "name")
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Categories, CustomCategoryAdmin)
admin.site.unregister(Group)
