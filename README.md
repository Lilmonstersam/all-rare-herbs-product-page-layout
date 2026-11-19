# All Rare Herbs: Product Page Layout Mockup

Static mockup of an All Rare Herbs product page ([Alocasia Frydek Variegated Plant](https://allrareherbs.com.au/product/alocasia-frydek-variegated-plant/)) showing a proposed **sticky add-to-cart bar** for desktop and mobile.

**Live preview:** https://lilmonstersam.github.io/all-rare-herbs-product-page-layout/

## What's being proposed

A bar that slides up from the bottom of the screen once the main Add to Cart button scrolls out of view, so shoppers can buy without scrolling back up.

| | Desktop / tablet | Mobile |
|---|---|---|
| Product name + selected size + stock | ✓ | (hidden to save space) |
| Size selector (synced with main form) | ✓ | ✓ |
| Price (updates with size) | ✓ | ✓ |
| Quantity stepper (synced with main form) | ✓ | ✓ |
| Add to Cart (triggers the real form) | ✓ | ✓ full width |
| Out-of-stock size switches CTA to **Join waitlist** | ✓ | ✓ |

The floating contact icon and reCAPTCHA badge lift above the bar while it is showing.

## Implementation notes for the developer

- All new code is self-contained in `index.html` between the `<!-- ARH MOCKUP: sticky add-to-cart bar -->` comments (one `<style>`, one markup block, one `<script>`). No dependencies.
- It reads from and writes to the existing WooCommerce variation form (`.swatch-btn`, `input.qty`, `.single_add_to_cart_button`) rather than duplicating cart logic, so it works with the current swatch script and waitlist plugin.
- Visibility uses `IntersectionObserver` on the main form's `.single_variation_wrap` (falls back to a scroll listener).
- Brand values: CTA `#6C845C`, waitlist `#58371D`, text `#293022`, Quicksand, 50px pill radius, matching the live theme.

## About this copy

- Built from a saved copy of the live page. Product images load from the live site.
- Analytics and ad tracking (GTM, GA4/Google Ads, Meta Pixel/CAPI, Mailchimp, reCAPTCHA) are **removed** so reviewing the mockup does not pollute the client's data.
- `noindex` meta + `robots.txt` keep the copy out of search results.
- The Add to Cart button submits to the live store, so a click adds the item to your real cart on allrareherbs.com.au.

## Deployment

Pushing to `main` deploys via GitHub Actions (`.github/workflows/deploy.yml`) to GitHub Pages.

```
index.html      # the mockup
assets/         # CSS, JS, fonts and images captured from the live page
robots.txt      # disallow all
.nojekyll       # serve files as-is
```

Prepared by Digilari for All Rare Herbs.
