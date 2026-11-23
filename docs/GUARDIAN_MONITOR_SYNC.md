# Guardian Monitor → Nightscout → Medtronic 780G AI

**Status:** Adapter prepared; no access to an installed Guardian Monitor app or live CareLink/Nightscout account has been verified.

## Why this route?
Guardian Monitor (third-party iOS/iPadOS app) can follow Medtronic CareLink caregiver data and optionally sync glucose, insulin and carbohydrates to Nightscout. App syncing and what data are actually available depend on the individual setup and upstream account.

## On the already signed-in Guardian Monitor device
1. Check the main glucose screen: is there a non-stale SG value with measurement timestamp?
2. In the app's settings find **Nightscout synchronization**. Feature may require a subscription and a Nightscout instance.
3. If available, configure your **own securely hosted Nightscout**, scoped to the authorized person; never mix multiple persons in one database.
4. Verify the Nightscout dashboard shows fresh CGM entries, and compare at least five readings with the Guardian Monitor display.
5. Check if insulin/carbohydrate events exist in Nightscout; do **not** assume pump events are complete or classify unlabelled correction events as SmartGuard autocorrection.

## API validation from Mac (terminal)
Use a locally created restricted **readable (read-only) Nightscout access token**, preferably with authentication required by the server. Nightscout v1 accepts `token` in a query string; keep logs and browser history free of that token.

```bash
export NIGHTSCOUT_URL='https://YOUR_PRIVATE_NIGHTSCOUT_HOST'
# Set NIGHTSCOUT_READ_TOKEN privately in your password manager or shell;
# do not paste it into chat, git, terminal screenshots, or CI logs.
python3 -m src.aid_review.nightscout
```

The script requests `/api/v1/entries.json` (CGM readings) with a read-only token, and prints an aggregate summary only. It does not use or access Mac app login state, and cannot prove that the insulin/treatment feed is complete.

## For 780G AID parameter review
CGM alone is insufficient. We need synchronized bolus, basal delivered, meal carbs, SmartGuard status, and the *actual dated historical settings* (ICR, AIT, SmartGuard Target). Inspect `/api/v1/treatments.json` and compare with CareLink reports, but never infer missing fields from CGM patterns. ISF / Manual Basal must be evaluated in the correct mode.

## Safety boundaries
No pump-control API, no real-time clinical alarms, no medication/parameter adjustment instruction; clinician review required. Never add patient data, API credentials, report PDFs or identifiable log output to the public repo.

## Official references
- https://apps.apple.com/us/app/guardian-monitor/id1546989938
- https://nightscout.github.io/uploader/setup/
- https://nightscout.github.io/nightscout/admin_tools/
- https://nightscout.github.io/nightscout/technical_info/api/
