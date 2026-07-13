from .models import PageKey

PAGE_PATHS = {
    PageKey.HOME: "/",
    PageKey.ABOUT: "/about/",
    PageKey.INDUSTRIES: "/industries/",
    PageKey.CONTACT: "/contact/",
}


class PageSectionAdminMixin:
    page_key_field = "page_key"

    def get_page_path(self, page_key):
        return PAGE_PATHS.get(page_key, "/")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == self.page_key_field:
            kwargs["choices"] = PageKey.choices
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        page_key = getattr(obj, self.page_key_field, None) if obj else None
        if page_key:
            path = self.get_page_path(page_key)
            mapping = (
                f"This content appears on {path}. "
                f"Use page key “{page_key}” so the site can find it."
            )
        else:
            mapping = (
                "Choose a page key that matches the page you are editing "
                "(home, about, industries, or contact)."
            )
        mapping_fieldset = (
            "Page mapping",
            {
                "fields": (self.page_key_field,),
                "description": mapping,
            },
        )
        if fieldsets:
            return [mapping_fieldset, *fieldsets]
        return [mapping_fieldset]


class ReadOnlyCreatedAdminMixin:
    readonly_fields = ("created_at",)
