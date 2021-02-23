from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	"""Define admin model for custom User model with no email field."""

	fieldsets = (
		(None, {'fields': ('email', 'password')}),

	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
		}),
	)
	list_filter = ('is_staff', 'is_superuser', 'is_active')
	list_display = ('email', 'is_staff')
	search_fields = ('email',)
	ordering = ('email',)