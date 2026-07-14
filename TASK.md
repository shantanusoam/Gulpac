# Tasks

## Completed
- [x] 2026-07-14 — Display & media: accept video URL (not iframe HTML); image upload option only in Machine admin

## Discovered During Work
- Live PDP was dumping pasted YouTube URLs as plain text inside `.pdp-video-embed` (fixed by converting URL → embed iframe)
- Production already served `/media/products/`; local Machine model now matches with `image` ImageField
