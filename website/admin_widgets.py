import json

from django import forms
from django.forms import Textarea
from tinymce.widgets import AdminTinyMCE


class RichTextEditorWidget(AdminTinyMCE):
    """TinyMCE editor used across Gulpac admin rich-text fields."""

    def __init__(self, attrs=None, mce_attrs=None):
        attrs = attrs or {}
        attrs.setdefault("rows", 12)
        attrs.setdefault("cols", 80)
        super().__init__(attrs=attrs, mce_attrs=mce_attrs)


class StringListWidget(Textarea):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.setdefault("rows", 6)
        attrs.setdefault("placeholder", "One item per line")
        super().__init__(attrs)

    def format_value(self, value):
        if isinstance(value, list):
            return "\n".join(str(item) for item in value)
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return "\n".join(str(item) for item in parsed)
            except (json.JSONDecodeError, TypeError):
                return value
        return ""


class StringListField(forms.CharField):
    widget = StringListWidget

    def prepare_value(self, value):
        if isinstance(value, list):
            return "\n".join(str(item) for item in value)
        return value or ""

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return [line.strip() for line in str(value).splitlines() if line.strip()]
