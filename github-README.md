# Nessus Authenticated VA Scanning — Windows & Linux Servers

Authenticated Vulnerability Assessment (VA) scan configuration and setup guide for Windows and Linux servers using Tenable Nessus (Professional / Expert), from trial installation through to a tuned, production-safe Advanced Scan policy — including servers running an ELK (Elasticsearch, Logstash, Kibana) stack.

> **Educational project.** This repository documents a VA-scanning workflow for learning and for use against systems the operator owns or is explicitly authorized to test. It is not a pentest/exploitation toolkit.

---

## ⚠️ Legal & Licensing Notice

- **Authorization required.** Only run these scans against infrastructure you own or have explicit written permission to test. Unauthorized scanning may be a criminal offense in most jurisdictions, regardless of intent.
- **Legitimate trial use only.** This guide assumes a single, genuine Nessus trial signup with a real email address, per Tenable's Terms of Service. It does **not** cover, endorse, or describe methods to repeatedly re-claim trial access (e.g., temp-mail services, multiple accounts) — doing so violates Tenable's EULA.
- **VA scope only.** Everything here is detection/reporting (Vulnerability Assessment), not exploitation or penetration testing.
- **Trial → Licensed.** The trial is for evaluation. For any production or ongoing use (e.g., scheduled nightly scans), transition to a paid Nessus Professional or Nessus Expert license before the trial expires.

---

## What's in this repo

This is currently a documentation-only project (README) covering:

- Downloading and installing Nessus (Windows & Linux scanner host)
- Activating the trial and updating the plugin feed
- Building an Advanced Scan policy tuned for authenticated Windows/Linux server VA scans
- Credential setup guidance (SSH for Linux, Windows credentials for Windows)
- Scheduling nightly scans safely against production servers, including ELK-hosting servers
- Transitioning from trial to a licensed subscription

---

## Prerequisites

- Admin/SSH access to target servers (with authorization)
- A dedicated scanner host (Windows or Linux) with internet access for plugin updates
- A real email address for Nessus trial registration
- Change-management / written sign-off to scan production systems

---

## Quick Start

### 1. Install Nessus

**Linux:**
```bash
dpkg -i Nessus-<version>-debian10_amd64.deb
systemctl start nessusd.service
```

**Windows:** run the `.msi` installer as administrator.

### 2. Activate & update plugins

Browse to `https://<scanner-host>:8834`, choose your edition, enter the activation code emailed by Tenable, create your admin login, and let the initial plugin feed download complete. Keep automatic plugin updates enabled going forward.

### 3. Create the Advanced Scan

**Scans → New Scan → Advanced Scan**, then apply the settings below.

---

## Tuned Scan Policy (Windows + Linux, VA-focused)

| Setting | State | Reason |
|---|---|---|
| Safe Checks | **ON** | Prevents plugins from destabilizing live services |
| Host Discovery — Ping | OFF | Target list is known/fixed |
| Port range | 1–65535 (TCP) | Full coverage incl. non-standard ELK ports (9200/9300/5044/5601) |
| UDP scanning | **OFF** | Slow, unreliable — biggest scan-time reduction |
| Local port enumerators (SSH/WMI netstat, SNMP) | ON | Fast, accurate, authenticated port data |
| SSL/TLS discovery | All TCP ports | Correctly IDs HTTPS services (e.g. Kibana) on any port |
| Perform thorough tests | OFF | Flagged by Tenable as potentially disruptive/slow |
| Assess component installs | ON | Flags outdated Elasticsearch/Logstash/Kibana versions |
| Brute force — only use provided credentials | ON | Avoids account lockouts from guessed default creds |
| SAM Registry / ADSI / WMI Query | ON | Authenticated Windows user enumeration |
| RID Brute Forcing | **OFF** | Redundant vs. above; mimics AD-recon attack pattern |
| Malware scan | ON | Known-bad-hash / IOC detection |
| Scan file system | OFF | Performance risk on 10+ hosts (per Tenable) |
| Web Applications | **OFF** | Out of scope — run as a separate, targeted scan |

### Credentials

- **Linux:** SSH credential (key-based preferred), sudo/escalation configured as needed
- **Windows:** domain or local account with delegated rights for vulnerability scanning

Store all credentials in a vault/secrets manager — never commit them to this or any repo.

### Scheduling

- Nightly, during a low-traffic maintenance window
- Stagger hosts in batches (e.g., 5–10 at a time) rather than scanning all at once
- Enable completion notifications/reporting for morning review

---

## Trial → Licensed

Before your trial expires: choose Professional or Expert based on your needs, purchase through Tenable, and apply the new activation code under **Settings → About**. Scan policies, schedules, and credentials carry over — no rebuild needed.

---

## Roadmap

- [ ] Add sample scan-policy export (`.nessus` policy XML), credentials redacted
- [ ] Add a report-parsing script for CSV/Nessus export summarization
- [ ] Separate scoped Web Application Scan template (Kibana-specific)

---

## Author

**Amit Ambekar**
GitHub: [github.com/amitambekar510](https://github.com/amitambekar510)
Medium: [medium.com/@amitambekar510](https://medium.com/@amitambekar510)

## License

Documentation in this repository is provided for educational purposes, "as is," with no warranty. Use responsibly and only against authorized systems.
