# Figma → Django Reference

## MCP tool parameters

### get_design_context

```json
{
  "fileKey": "30wFXcjLKoMceO8TvkuMw3",
  "nodeId": "105:784",
  "clientFrameworks": "django,tailwind",
  "clientLanguages": "html,css"
}
```

Returns: React+Tailwind reference (adapt, don't copy), asset URL map, screenshot, node metadata.

### download_assets

```json
{
  "fileKey": "30wFXcjLKoMceO8TvkuMw3",
  "nodeId": "105:784",
  "defaultFormat": "png",
  "defaultScale": 2
}
```

Returns: `export.url` (full node render) + `rawImages[]` with `{ url, format }`.

### get_variable_defs

Returns design tokens, e.g.:

```json
{
  "Color": "#2d388c",
  "Color 2": "#47a33d",
  "heading": "Font(family: \"Hatsch Sans PERSONAL USE ONLY\", style: Italic, size: 40, ...)"
}
```

---

## Font resolution guide

| Figma family | Action |
|--------------|--------|
| Inter | Already loaded in `base.html` — use `font-inter` |
| Plus Jakarta Sans | Already in `base.html` |
| Hatsch Sans PERSONAL USE ONLY | Download WOFF from CDNFonts or designer files → `website/static/fonts/` |
| Lucide icons | Use `<i data-lucide="name">` — icons init in base template |
| Custom SVG icons | Download from Figma asset URL → `images/<section>/icon.svg` |

### Finding WOFF URLs

```bash
curl -sL "https://fonts.cdnfonts.com/css/<family-slug>" | head -20
```

Download both regular and italic if design uses both. Match `font-style` in `@font-face` to the file.

---

## Color extraction

From Figma node fills:

- Solid: `rgb(45, 56, 140)` → `#2d388c`
- CSS variable: `var(--Color, #2D388C)` → use fallback `#2d388c`
- Gradient: copy full `linear-gradient(...)` with all stops

---

## Layout translation table

| Figma | CSS / Tailwind |
|-------|----------------|
| `pt-[80px]` | `pt-20 lg:pt-[80px]` |
| `px-[64px]` + inner `px-[24px]` | outer `lg:px-[64px]` + inner `px-6` (= 88px total) |
| `absolute left-[644px] top-[9px]` | scoped CSS at `@media (min-width: 1280px)` |
| `rounded-[14px]` | `rounded-[14px]` |
| `shadow-[0px_10px_15px...]` | exact `box-shadow` in CSS |
| `w-[584px]` text column | `max-w-[584px]` |
| `size-[64px]` icon box | `width: 64px; height: 64px` |
| `object-cover` on image | `object-fit: cover` |
| `bg-contain bg-right bg-bottom` | hero background pattern |

---

## Background image patterns

### Full-section background (hero)

```html
<div
  class="absolute inset-0 bg-contain bg-no-repeat bg-right bg-bottom"
  style="background-image: url('{% static 'images/hero/hero-machine.png' %}');"
></div>
```

### CMS-driven background

```html
<div style="background-image: url('{{ hero.background_image_url }}');"></div>
```

### Gradient overlay (when Figma has one)

```html
<div class="absolute inset-0 bg-gradient-to-r from-[rgba(255,255,255,0.92)] via-[rgba(255,255,255,0.62)] to-[rgba(255,255,255,0.12)]"></div>
```

---

## Dynamic model patterns (Gulpac)

### HeroSection

```python
def build_hero_context(page_key, defaults):
    hero = HeroSection.objects.filter(page_key=page_key, is_active=True).first()
    # merges DB fields with defaults dict
```

Fields: `page_key`, `title`, `description`, `background_image`, `back_link_*`, `is_active`

### CardGridSection + CardGridItem

```python
def build_card_grid_context(page_key, section_key, defaults):
    section = CardGridSection.objects.filter(...).prefetch_related("cards").first()
```

Use for: advantages cards, feature grids, any repeating card layout from Figma.

### When to create a new model

Create when **any** of:
- Marketing will edit copy/images without deploys
- Content repeats across pages with same structure
- List items have order, active flag, or images

Keep static when:
- Section is unique to one page and rarely changes
- Prototyping first pass (add model in follow-up PR)

### Suggested model for About-style section

```python
class AboutSection(models.Model):
    page_key = models.CharField(max_length=100, unique=True)
    eyebrow = models.CharField(max_length=100)
    heading_prefix = models.CharField(max_length=200)
    heading_accent = models.CharField(max_length=200)
    paragraph_1 = models.TextField()
    paragraph_2 = models.TextField()
    image_1 = models.ImageField(upload_to="about/")
    image_2 = models.ImageField(upload_to="about/")
    is_active = models.BooleanField(default=True)

class AboutStat(models.Model):
    section = models.ForeignKey(AboutSection, related_name="stats", on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="about/icons/")
    label = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
```

---

## Responsive strategy

| Viewport | Behavior |
|----------|----------|
| `< 1280px` | Stack columns; images in relative container with % widths + overlap |
| `≥ 1280px` | Apply exact Figma absolute positions |
| Mobile | Reduce font sizes only if Figma has mobile frame; otherwise keep typography |

Always test at 1440px (common Figma frame width) and 375px mobile.

---

## QA checklist

- [ ] Typography matches Figma inspect (family, size, weight, line-height, letter-spacing)
- [ ] Colors are exact hex, not Tailwind approximations (`text-slate-600` ≠ `#4a5565`)
- [ ] Images served from `{% static %}` not Figma URLs
- [ ] Overlapping images use correct z-index
- [ ] `npm run build` run after Tailwind class changes
- [ ] GSAP targets listed in `animatedTargets`
- [ ] `prefers-reduced-motion` respected
- [ ] Alt text on meaningful images; `aria-hidden` on decorative icons
