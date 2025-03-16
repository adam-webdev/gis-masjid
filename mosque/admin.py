from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect

class MyAdminSite(AdminSite):
    site_header = _("My Admin Panel")  # Opsional, hanya untuk kustomisasi header

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return response

admin.site = MyAdminSite()
