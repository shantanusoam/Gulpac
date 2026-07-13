from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        from django.contrib import admin

        admin.site.site_header = "Gulpac Content Manager"
        admin.site.site_title = "Gulpac Admin"
        admin.site.index_title = "Manage website content by page"
