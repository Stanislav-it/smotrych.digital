# GTM / GA4 setup

The project is prepared for Google Tag Manager and GA4 through environment variables.

## Render environment variables

Required:

```env
SITE_URL=https://smotrych.digital
GTM_ID=GTM-XXXXXXX
```

Optional direct GA4 fallback. Do not use this if GA4 is configured inside GTM:

```env
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
```

Recommended setup:

1. Add only `GTM_ID` in Render.
2. Create a Google tag in Google Tag Manager with the GA4 Measurement ID.
3. Trigger it on `Initialization - All Pages` or `All Pages`.
4. Publish the GTM container.

## Cookie consent

The cookie banner stores consent in:

```text
smotrych_cookie_consent_v1
```

For testing, open:

```text
https://smotrych.digital/?cookies=reset
```

## DataLayer events

The site pushes these events for Google Ads / GA4 configuration in GTM:

- `cookie_consent_granted`
- `cookie_consent_essential`
- `lead_form_submit`
- `generate_lead`
- `contact_click`
- `contact_cta_click`

## Checks after deployment

Open page source and search for:

```text
GTM-XXXXXXX
```

In Chrome DevTools → Network, filter by:

```text
gtm.js
```

Then filter by:

```text
collect
```
