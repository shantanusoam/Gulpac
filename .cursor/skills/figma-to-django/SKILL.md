---
name: figma-to-django
description: >-
  Converts Figma designs into Gulpac Django templates with exact fonts, colors,
  images, layout, backgrounds, and GSAP animations. Uses Figma MCP tools, downloads
  assets locally, and wires CMS models when content should be dynamic. Use when
  implementing Figma screens, node URLs, design-to-code, or matching Figma typography
  and spacing in Django/Tailwind.
---

# Figma → Django (Gulpac)

Convert Figma nodes into production Django templates for this project. **Read this skill fully before calling Figma MCP tools.**

## Stack (do not change)

| Layer | Location |
|-------|----------|
| Templates | `website/templates/website/` |
| Components | `website/templates/website/components/` |
| Static assets | `website/static/` |
| Fonts | `website/static/fonts/` |
| Images | `website/static/images/<section>/` |
| CSS source | `website/static/src/styles.css` → `npm run build` → `site.css` |
| Animations | `initGulpacAnimations()` in page `{% block scripts %}` |
| Models | `website/models.py` + `build_*_context()` in `website/views.py` |

Always extend `website/base.html`. Use `{% load static %}` and `{% static '...' %}`.

---

## Workflow checklist

Copy and track progress:

```
- [ ] 1. Parse Figma URL → fileKey + nodeId (105-784 → 105:784)
- [ ] 2. get_design_context (primary) + get_variable_defs (colors/fonts)
- [ ] 3. get_screenshot if layout is ambiguous
- [ ] 4. download_assets → save under website/static/images/<section>/
- [ ] 5. Resolve fonts → self-host in website/static/fonts/
- [ ] 6. Decide static vs dynamic (see reference.md)
- [ ] 7. Build template HTML + scoped CSS in {% block scripts %}
- [ ] 8. Add GSAP scroll/entrance animations
- [ ] 9. npm run build (Tailwind)
- [ ] 10. Verify in browser at 127.0.0.1:8007
```

---

## Step 1 — Figma MCP (mandatory order)

**Always read tool schemas** in `mcps/plugin-figma-figma/tools/` before calling.

### Parse URL

```
https://figma.com/design/:fileKey/:fileName?node-id=105-784
→ fileKey = :fileKey, nodeId = "105:784"
```

Branch URLs: use `branchKey` as `fileKey`.

### Tools

| Tool | When |
|------|------|
| `get_design_context` | **First.** Reference layout, typography, asset URLs, screenshot |
| `get_variable_defs` | Figma color/font variables (`#2d388c`, heading tokens) |
| `download_assets` | Export node + raw image fills (JPEG/PNG/SVG) |
| `get_screenshot` | Visual QA, overlap/alignment disputes |
| `get_motion_context` | Prototype motion (often empty — use GSAP defaults) |

Pass `clientFrameworks: "django,tailwind"` and `clientLanguages: "html,css"`.

**Do not** paste Figma React output verbatim. Adapt to Django templates + project patterns.

---

## Step 2 — Fonts

### Priority order

1. **Already in project** — check `base.html` Google Fonts + `website/static/fonts/`
2. **Google Fonts** — add `<link>` in `base.html` if available
3. **Custom / personal fonts** — download WOFF/WOFF2, self-host

### Self-host pattern

```css
@font-face {
  font-family: "Hatsch Sans PERSONAL USE ONLY";
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url("{% static 'fonts/HatschSans-Italic.woff' %}") format("woff");
}
```

Put section-specific `@font-face` in the page `{% block scripts %}` `<style>` block, or in `base.html` if reused site-wide.

### Match Figma typography exactly

Copy all five properties from Figma inspect / `get_variable_defs`:

```css
.about-heading {
  color: #2d388c;
  font-family: "Hatsch Sans PERSONAL USE ONLY", sans-serif;
  font-size: 40px;
  font-style: italic;
  font-weight: 400;
  line-height: 48px;
  letter-spacing: 0.369px;
}
```

| Figma field | CSS property |
|-------------|--------------|
| Font family | `font-family` |
| Size | `font-size` (px) |
| Style | `font-style` |
| Weight | `font-weight` |
| Line height | `line-height` (px, not unitless, when Figma gives px) |
| Letter spacing | `letter-spacing` (px) |
| Fill color | `color` or `background-color` |

**Inter** is the project body font (`font-inter` class or `font-family: "Inter", sans-serif`).

### License

Note personal-use fonts (e.g. Hatsch Sans) in comments. Commercial sites need a paid license.

---

## Step 3 — Colors

Use exact hex from Figma — never approximate.

| Token | Gulpac value |
|-------|--------------|
| Primary navy | `#2d388c` |
| Accent green | `#47a33d` |
| Body gray | `#4a5565` |
| Label gray | `#364153` |
| Section bg | `#f3f5f9` |

Gradients: copy stop list from Figma `backgroundImage` linear-gradient verbatim.

---

## Step 4 — Images & backgrounds

### Download

```bash
mkdir -p website/static/images/<section>
curl -sL "<figma-asset-url>" -o website/static/images/<section>/file.jpg
file website/static/images/<section>/*   # verify type; rename .svg if needed
```

Prefer `download_assets` raw images for photos; use asset URLs from `get_design_context` for icons.

### `<img>` vs CSS background

| Figma pattern | Django approach |
|---------------|-----------------|
| Image layer with `object-cover` | `<img src="{% static '...' %}" class="...">` |
| Fill on frame / hero | `style="background-image: url('{% static '...' %}')"` + `bg-cover` / `bg-contain` |
| Overlapping absolute images | Parent `position: relative`, children `position: absolute` with Figma `left`/`top`/`width`/`height` |

### Figma absolute positions → CSS

From `get_design_context`, extract pixel coords for desktop:

```css
@media (min-width: 1280px) {
  .about-image-1 { left: 644px; top: 9px; width: 341px; height: 338px; }
  .about-image-2 { left: 862px; top: 178px; width: 370px; height: 339px; z-index: 2; }
}
```

Use `xl` (1280px) breakpoint when total layout width ≈ 1232px. Below that: stack with simplified overlap.

Shadows: `box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);`

---

## Step 5 — Layout rules

1. **Figma frame padding** → section `pt-[80px] px-[64px]` etc.
2. **Auto-layout** → flexbox/grid; don't use absolute for flowing text columns
3. **Fixed-size stage** → wrapper `max-w-[1232px] min-h-[516.75px] relative`
4. **Text column** → `max-w-[584px]` when Figma shows 584px width
5. **Scoped BEM classes** → `.about-section`, `.about-heading` in page `<style>` for pixel-perfect sections
6. **Tailwind** for spacing utilities; **scoped CSS** for exact Figma typography and absolute coords

After template edits: `npm run build`

---

## Step 6 — Dynamic vs static

| Content type | Approach |
|--------------|----------|
| Hero, page headers | `HeroSection` model + `build_hero_context()` → `page_hero.html` |
| Card grids | `CardGridSection` + `CardGridItem` + `build_card_grid_context()` |
| CTA blocks | `CTASection` model |
| Contact copy | `ContactSection` model |
| Repeating lists (machines, testimonials) | Existing models + `{% for %}` |
| One-off marketing section | Static template + hardcoded defaults; extract model later if CMS needed |

**Pattern for new dynamic section:**

1. Add model in `website/models.py`
2. Register in `website/admin.py`
3. Add `build_<section>_context(page_key, defaults)` in `views.py`
4. Create `website/templates/website/components/<section>.html`
5. `{% include %}` with `with section=section`

Template fallbacks: `{{ section.title|default:"Figma default text" }}`

---

## Step 7 — Animations (GSAP)

Use existing `initGulpacAnimations()` in `{% block scripts %}`.

### Entrance (hero, above fold)

```javascript
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 1 } });
tl.fromTo(".hero-text", { autoAlpha: 0, x: -50 }, { autoAlpha: 1, x: 0 });
```

### Scroll sections

```javascript
gsap.fromTo(".adv-header",
  { autoAlpha: 0, y: 30 },
  { autoAlpha: 1, y: 0, duration: 0.7, ease: "power2.out",
    scrollTrigger: { trigger: ".adv-header", start: "top 88%", once: true } }
);
```

### Staggered section (text → stats → images)

```javascript
const aboutTl = gsap.timeline({
  scrollTrigger: { trigger: ".about-section__stage", start: "top 85%", once: true },
});
aboutTl
  .fromTo(".about-eyebrow", { autoAlpha: 0, y: 18 }, { autoAlpha: 1, y: 0, duration: 0.55 })
  .fromTo(".about-heading", { autoAlpha: 0, y: 28 }, { autoAlpha: 1, y: 0, duration: 0.7 }, "-=0.3")
  .fromTo(".about-para", { autoAlpha: 0, y: 22 }, { autoAlpha: 1, y: 0, stagger: 0.12 }, "-=0.35")
  .fromTo(".about-image-1", { autoAlpha: 0, x: 70, y: 18 }, { autoAlpha: 1, x: 0, y: 0, duration: 0.95 }, "-=0.45")
  .fromTo(".about-image-2", { autoAlpha: 0, x: 90, y: 36 }, { autoAlpha: 1, x: 0, y: 0, duration: 1.05 }, "-=0.7");
```

Register all animated selectors in `animatedTargets` for `prefers-reduced-motion` cleanup.

Icons: use Lucide (`data-lucide="shield-check"`) when Figma shows generic icons; download SVG from Figma when custom.

---

## Step 8 — File placement

```
website/templates/website/home.html          # page sections
website/templates/website/components/        # reusable blocks
website/static/images/about/                 # section assets
website/static/fonts/                        # self-hosted fonts
tests/website/test_<feature>.py              # if adding models/views
```

---

## Anti-patterns

- ❌ Leaving Figma MCP asset URLs in templates (expire in ~7 days)
- ❌ Using Plus Jakarta Sans when Figma specifies a different family
- ❌ `background-size: cover` when Figma says `contain`
- ❌ Grid 50/50 when Figma uses absolute overlapping images
- ❌ Skipping `npm run build` after new Tailwind classes
- ❌ Putting `@font-face` with wrong `font-style` (italic file needs `font-style: italic`)

---

## Additional resources

- [reference.md](reference.md) — MCP tool params, model patterns, responsive table
- [examples.md](examples.md) — About Glupac section (node 105:784) walkthrough
- [scripts/download-figma-assets.sh](scripts/download-figma-assets.sh) — asset download helper
