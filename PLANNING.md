# Gulpac Planning

## Stack

Django 5.2 + Tailwind CSS marketing site for Glupac packaging machinery.

## Architecture

- `website/` — models, views, templates, admin
- `config/` — Django project settings and URLs
- `tests/` — Pytest suite mirroring app structure

## Product content

Products (`Machine` model, admin label **Products**) are CMS-managed with rich-text fields, image/brochure uploads, SEO meta, and `ProductCategory` FK — aligned with the IWS product admin reference.
