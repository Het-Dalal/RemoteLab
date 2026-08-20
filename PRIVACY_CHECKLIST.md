# PRIVACY REVIEW CHECKLIST

Before uploading this repository or screenshots:

- [ ] Remove any real public IP address.
- [ ] Blur/redact private IP addresses if you do not want your lab network structure public.
- [ ] Remove MAC addresses.
- [ ] Remove GPS coordinates or city/location information.
- [ ] Remove Cloudflare quick-tunnel URLs and tunnel IDs.
- [ ] Remove API keys, tokens, cookies, passwords and session values.
- [ ] Remove phone numbers and email addresses.
- [ ] Remove browser account/profile names and personal notifications.
- [ ] Remove terminal usernames/hostnames that identify you personally.
- [ ] Check image metadata/EXIF before uploading phone screenshots.
- [ ] Check Git history for accidentally committed secrets.
- [ ] Keep `.env` excluded via `.gitignore`.
- [ ] Run a secret scanner such as Gitleaks before making the repository public.

Note: phone screenshots can expose status-bar information, account icons, notifications, URLs, network details, or metadata even when the application itself does not.
