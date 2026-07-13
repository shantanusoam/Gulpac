# Gulpac Task Tracker

## Active

- [x] 2026-07-13 — Update product backend to match IWS reference admin (SKU, rich text description/specs/features, category FK, image upload, slug, SEO meta, product type, brochure)
- [x] 2026-07-13 — Replace custom rich-text widget with TinyMCE (django-tinymce) for product Description/Specification/Features

## Discovered During Work

- Existing machines used JSON features/specifications; migrated to rich-text HTML for admin parity with the reference CMS.
- Legacy `image_path` kept as fallback so seeded static images still work until uploads replace them.
