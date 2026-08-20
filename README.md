## Project Walkthrough

For a complete screenshot-by-screenshot demonstration of the project:

[View the RemoteLab Walkthrough](RemoteLab_walkthrough.pdf)# RemoteLab - Mobile Kali Administration PoC

RemoteLab is a portfolio project that demonstrates a browser-based command interface for an **authorized Kali Linux lab environment**.

## Architecture

`QR Code -> Mobile Browser -> Cloudflare Tunnel -> Flask App -> Controlled Kali Lab`

The original proof of concept demonstrated mobile access to a Kali-hosted web interface and execution of commands from the phone. The portfolio version is intentionally hardened and privacy-conscious.

## What the project demonstrates

- Flask-based web interface
- Remote access to a controlled lab environment
- QR-assisted access workflow
- Cloudflare Tunnel integration
- Linux command execution with an allow-list
- Basic authentication using an environment-provided access token
- Security hardening from an early proof of concept

## Security changes made before publishing

The first proof of concept used unrestricted command execution via `subprocess.run(..., shell=True)` and also collected client metadata including IP-based location and browser GPS when permission was granted.

Those behaviors are **not included in this public portfolio version**.

The published version:

- does not collect GPS coordinates
- does not perform IP geolocation
- does not display or store phone/device identifiers
- does not require root
- requires an access token
- uses an allow-list of commands
- executes commands with `shell=False`
- binds locally by default so a tunnel or reverse proxy can be added deliberately

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export REMOTE_LAB_TOKEN="replace-with-a-long-random-token"
python app.py
```

The application listens on `127.0.0.1:8080`.

If you expose it through a tunnel, keep authentication enabled and use it only with systems you own or are authorized to administer.

## Allowed commands

The example build allows:

- `whoami`
- `hostname`
- `pwd`
- `date`
- `ip addr`
- `uname -a`

Change the allow-list in `app.py` if you want to customize the lab.

## Screenshots

Screenshots from the original lab demonstration can be placed under `screenshots/`.

Before publishing screenshots, verify that they do not reveal:

- public or private IP addresses you do not want shared
- Cloudflare tunnel URLs
- GPS coordinates
- usernames containing personal information
- MAC addresses
- tokens, passwords, API keys or cookies
- browser/account notifications or personal tabs
- filenames containing private information

## Threat model

This project is intentionally a lab tool, not a production remote-management platform.

Anyone who can reach a remote command endpoint should be treated as potentially hostile. The public version therefore avoids arbitrary shell execution and uses explicit command authorization.

For a production-grade system, add stronger identity controls, TLS termination, CSRF protections where relevant, audit logging, rate limiting, session management, and isolation.

## Ethical use

Use RemoteLab only on devices and networks you own or have explicit authorization to administer.

## Project history

The project began as a proof of concept for accessing a Kali lab from a mobile browser through a QR-assisted workflow and a Cloudflare tunnel. During review, the unrestricted command endpoint and privacy-sensitive telemetry were identified as risks. The portfolio version documents and fixes those issues rather than hiding them.
