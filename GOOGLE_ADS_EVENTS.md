# Google Ads / GTM events for smotrych.digital

This build is prepared for GA4 and Google Ads conversion tracking through Google Tag Manager.

## Main conversion event

Use this as the primary Google Ads conversion:

```text
generate_lead
```

It fires only after the backend successfully saves a lead and redirects back with a success marker.

Recommended conversion action in Google Ads:

```text
Conversion name: Lead — form submit
Category: Submit lead form
Value: Use the same value for each conversion / 1 PLN, or no value
Count: One
Attribution: Data-driven if available
```

## Supporting events

These are useful as GA4 key events or Google Ads secondary conversions:

```text
lead_form_start
lead_form_submit_attempt
lead_form_success
contact_cta_click
contact_click
email_click
phone_click
whatsapp_click
newsletter_signup_attempt
outbound_click
select_service
scroll_depth
cookie_consent_granted
cookie_consent_essential
```

Recommended Google Ads secondary conversions:

```text
phone_click
email_click
whatsapp_click
contact_cta_click
```

## GTM setup

1. Keep Render configured with:

```env
SITE_URL=https://smotrych.digital
GTM_ID=GTM-MTMVQJVQ
```

2. In GTM, keep the GA4 Google tag using:

```text
G-CPKCGL6CFK
```

3. Create GA4 Event triggers in GTM for the custom event names above.
4. For Google Ads, create Conversion Linker on All Pages.
5. Add Google Ads Conversion Tracking tags using the relevant GTM triggers.
6. Publish the GTM container.

## Testing

Open the site with reset cookies:

```text
https://smotrych.digital/?cookies=reset
```

Accept analytics cookies, submit the contact form, and then check:

- GTM Preview: event timeline should show `lead_form_start`, `lead_form_submit_attempt`, `lead_form_success`, `generate_lead`.
- GA4 Realtime / DebugView: should show `generate_lead`.
- Chrome DevTools Network: filter by `collect`.
