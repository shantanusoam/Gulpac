# Figma → Django Examples

## Example 1: About Glupac (node 105:784)

**Figma:** `https://www.figma.com/design/30wFXcjLKoMceO8TvkuMw3/Ashwani-Tayal?node-id=105-784`

### MCP calls

```
get_design_context  fileKey=30wFXcjLKoMceO8TvkuMw3  nodeId=105:784
get_variable_defs   fileKey=30wFXcjLKoMceO8TvkuMw3  nodeId=105:784
download_assets     fileKey=30wFXcjLKoMceO8TvkuMw3  nodeId=105:784
```

### Assets saved

```
website/static/images/about/machine-1.jpg
website/static/images/about/machine-2.jpg
website/static/images/about/icon-experience.svg
website/static/images/about/icon-installations.svg
website/static/images/about/icon-customized.svg
website/static/fonts/HatschSans-Regular.woff
website/static/fonts/HatschSans-Italic.woff
```

### Typography applied

**Eyebrow**
```css
font-family: Inter; font-size: 14px; font-weight: 600;
line-height: 20px; letter-spacing: 0.1996px; color: #2d388c;
text-transform: uppercase;
```

**Heading**
```css
font-family: "Hatsch Sans PERSONAL USE ONLY";
font-size: 40px; font-style: italic; font-weight: 400;
line-height: 48px; letter-spacing: 0.369px; color: #2d388c;
/* accent span: color #47a33d */
```

**Paragraph**
```css
font-family: Inter; font-size: 18px; font-weight: 400;
line-height: 29.25px; letter-spacing: -0.439px; color: #4a5565;
```

### Layout structure

```html
<section class="about-section">
  <div class="about-section__container">
    <div class="about-section__stage">   <!-- relative, min-h 516.75px at xl -->
      <div class="about-content">        <!-- xl: absolute left 0, max-w 584px -->
        ...
      </div>
      <div class="about-images">         <!-- xl: absolute inset-0 -->
        <img class="about-image-1" />    <!-- xl: left 644px top 9px -->
        <img class="about-image-2" />    <!-- xl: left 862px top 178px, z-index 2 -->
      </div>
    </div>
  </div>
</section>
```

### Animation timeline

1. Eyebrow fade up
2. Heading fade up (overlap -0.3s)
3. Paragraphs stagger
4. Stat icons stagger with scale
5. Image 1 slide from right
6. Image 2 slide from right (staggered for overlap reveal)

Implemented in `home.html` `{% block scripts %}`.

---

## Example 2: Page hero (dynamic)

Figma hero → use existing component:

```django
{% include "website/components/page_hero.html" with hero=hero %}
```

View:

```python
hero = build_hero_context("contact", {
    "title": "Contact Us",
    "description": "...",
    "background_image_url": static("images/contact-bg.gif"),
    "centered": True,
})
```

---

## Example 3: Icon stat row from Figma gradient box

Figma gradient on 64×64 rounded-14px box:

```css
.about-stat__icon {
  width: 64px; height: 64px; border-radius: 14px;
  background: linear-gradient(
    135deg,
    rgb(44, 62, 143) 0%,
    rgb(42, 62, 148) 16.667%,
    rgb(40, 63, 154) 33.333%,
    rgb(38, 63, 159) 50%,
    rgb(35, 64, 164) 66.667%,
    rgb(33, 64, 170) 83.333%,
    rgb(30, 64, 175) 100%
  );
}
```

Icon: 32×32 SVG centered inside.

---

## Example 4: Advantages grid (existing static pattern)

Figma card grid with Lucide icons → static template loop candidate for `CardGridSection`:

```django
{% for card in advantages.cards %}
  <div class="bg-white rounded-2xl p-8 ...">
    <i data-lucide="{{ card.icon }}" class="w-7 h-7"></i>
    <h3>{{ card.title }}</h3>
    <p>{{ card.description }}</p>
  </div>
{% endfor %}
```

To make dynamic: migrate to `CardGridSection` with `section_key="advantages"`.
