# SWP-BUDJET Email OTP

The app is hosted as a static GitHub Pages site, so real email delivery is handled by the separate Cloudflare Worker in worker/otp-worker.js.

## One-time setup
1. In Cloudflare, create a Workers KV namespace named SWP_BUDJET_AUTH.
2. Replace REPLACE_WITH_KV_NAMESPACE_ID in wrangler.toml with the namespace ID and bind it to the Worker as AUTH_KV.
3. Deploy worker/otp-worker.js as a Worker named swp-budjet-auth.
4. Add Worker secrets RESEND_API_KEY and SESSION_SECRET. SESSION_SECRET must be a long random secret (at least 32 random bytes).
5. Set MAIL_FROM to a sender address verified in Resend. The default onboarding@resend.dev is for limited testing; production sending should use a verified domain.
6. The Worker permits the fixed administrator mailbox cpaswp@gmail.com and the GitHub Pages origin https://cpaswp.github.io.
7. Copy the deployed Worker URL. Open the SWP-BUDJET sign-in page, expand إعداد خدمة التحقق (للمسؤول), paste the Worker URL, and save it.

## OTP behavior
Six-digit random code, five-minute expiry, one-time use, maximum five verification attempts, request throttling by IP and mailbox, and an eight-hour signed session token. The code is stored as a hash in KV.

## Important limitation
SWP-BUDJET currently keeps business data in browser localStorage. The OTP screen is a genuine email challenge once the Worker and Resend credentials are configured, but it is not server-side data isolation or encryption. Protecting all business records against browser/device access requires moving records to an authenticated server-side API and database.
