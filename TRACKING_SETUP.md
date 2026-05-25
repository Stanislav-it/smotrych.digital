# GTM / GA4 / Google Ads setup

The project is prepared for Google Tag Manager, GA4 and Google Ads conversion tracking through environment variables and dataLayer events.

## Render environment variables

Required:

```env
SITE_URL=https://smotrych.digital
GTM_ID=GTM-MTMVQJVQ
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

The site pushes these events for GA4 and Google Ads configuration in GTM:

Primary conversion:

```text
generate_lead
```

Lead funnel:

```text
lead_form_start
lead_form_submit_attempt
lead_form_error
lead_form_success
generate_lead
newsletter_signup_attempt
```

Contact micro-conversions:

```text
contact_cta_click
contact_click
email_click
phone_click
whatsapp_click
```

Engagement and navigation:

```text
select_service
outbound_click
scroll_depth
```

Consent:

```text
cookie_consent_granted
cookie_consent_essential
```

## Google Ads recommended configuration

In GTM add:

1. **Conversion Linker** tag on `All Pages`.
2. **Google Ads Conversion Tracking** tag for the primary lead conversion.
3. Trigger for the primary conversion:

```text
Custom Event = generate_lead
```

Secondary conversion triggers can be created for:

```text
phone_click
email_click
whatsapp_click
contact_cta_click
```

## Checks after deployment

Open page source and search for:

```text
GTM-MTMVQJVQ
```

In Chrome DevTools → Network, filter by:

```text
gtm.js
```

Then filter by:

```text
collect
```

After submitting a form, GA4 Realtime / DebugView should show:

```text
generate_lead
```
