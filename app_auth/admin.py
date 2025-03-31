from django.contrib import admin
from .models import User,Library

admin.site.register([User,Library])
