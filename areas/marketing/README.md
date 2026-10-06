# areas/marketing/ - CompanyOS outputs

Everything marketing skills produce lands here. CompanyOS skills already
know where to save - you rarely need to create folders manually.

## Standard structure

```
areas/marketing/
|-- content/                    outputs from /carousel and /publish-topic
|   `-- <type>-<topic>-<YYYY-MM-DD>/
|       |-- carousel.html
|       |-- render.js
|       |-- instagram/slide-XX.png
|       |-- caption.md
|       `-- caption-linkedin.md
|
|-- seo/                        outputs from /seo (8 steps)
|   |-- 01-demand-research.md
|   |-- 02-competition-analysis.md
|   |-- 03-google-business-profile.md
|   |-- 04-on-page-optimization.md
|   |-- 05-content-strategy.md
|   |-- 06-google-ads.md
|   |-- 07-monitoring-checklist.md
|   `-- 08-ai-geo-optimization.md
|
|-- campaigns/                  outputs from /google-ad and /ads-report
|   |-- google-ads-<YYYY-MM-DD>/ CSVs ready to import
|   `-- reports/                weekly reports
|
`-- google-reviews/             history from /reply-reviews (optional)
```

## How it works

- **`/carousel` or `/publish-topic`** -> creates a folder in `content/<type>-<topic>-<date>/`
- **`/seo`** -> fills the 8 numbered files in `seo/`
- **`/google-ad`** -> creates a folder in `campaigns/google-ads-<date>/` with CSVs
- **`/ads-report`** -> creates a file in `campaigns/reports/<date>-report.md`
- **`/reply-reviews`** -> optionally saves history in `google-reviews/`

## Versioning

Everything here is versioned in git through `/save`. Useful for
comparing SEO progress between months, reviewing old copy, or recovering
a piece after changing it on Instagram.
