from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User,Transaction
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id','username','first_name','last_name','email','is_active','is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields':('email','username','password')}),
        ('Personal info', {'fields':('first_name','last_name')}),
        ('Permisons', {'fields': ('is_active', 'is_staff','is_superuser')}),
        ('Group Permissions', {
            'classes':('collapse',),
            'fields':('groups','user_permissions',  )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','first_name','last_name','password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.register(Transaction)