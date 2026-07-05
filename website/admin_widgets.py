from django.forms import Textarea


class RichTextEditorWidget(Textarea):
    class Media:
        css = {"all": ("website/admin_rich_text_editor.css",)}
        js = ("website/admin_rich_text_editor.js",)

    def __init__(self, attrs=None):
        attrs = attrs or {}
        existing_class = attrs.get("class", "")
        attrs["class"] = f"{existing_class} rich-text-source".strip()
        super().__init__(attrs)
