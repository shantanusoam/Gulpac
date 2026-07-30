# Tasks

## Completed
- [x] 2026-07-14 — Display & media: accept video URL; image upload only (`product_image`), safe SQLite rename migration
- [x] 2026-07-14 — PDP Main Features checkmark list + Technical Specs zebra key/value table (parse admin HTML)
- [x] 2026-07-30 — Home industries fallback when DB empty; industry card hover gap; contact italic font; map scroll-zoom lock

## Discovered During Work
- Production already had `0012_product_backend_fields` (HTML features/specs + `product_image`); deploying a conflicting `0012` caused SQLite remake + JSON_VALID failure
- Fixed by restoring product-backend base and adding `0013_machine_video_url` via `ALTER TABLE ... RENAME COLUMN`
- Production home showed “Add industries…” while `/industries/` used static defaults — home had no empty-DB fallback
