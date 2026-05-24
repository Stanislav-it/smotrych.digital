# Smotrych Digital — Flask site

Aktualizacja:
- stały (`fixed`) transparentny header;
- działające menu mobilne;
- logo użyte w headerze, footerze i faviconie;
- po hero/headerze dodana płynna sekcja portfolio z trzema telefonami z dostarczonego ZIP-a;
- animacje reveal-on-scroll oraz delikatne unoszenie telefonów.

## Start

```bash
pip install -r requirements.txt
python app.py
```

Strona działa na:

```text
http://127.0.0.1:5001
```

## Render deployment

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```

## Contact form logic

The contact form posts to `/lead`. Every valid lead is saved to SQLite and archived as JSON/JSONL. If SMTP variables are configured, the lead is also emailed.

Recommended Render environment variables:

```text
SECRET_KEY=your-long-random-secret
DATA_DIR=/var/data
MAIL_TO=your-email@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-smtp-login@example.com
SMTP_PASS=your-smtp-app-password
SMTP_FROM=your-smtp-login@example.com
SMTP_TLS=1
ADMIN_PASSWORD=your-admin-password
```

Optional variables:

```text
DB_PATH=/var/data/smotrych_leads.sqlite3
LEADS_DIR=/var/data/leads
LEADS_JSONL_PATH=/var/data/leads/leads.jsonl
MAIL_ARCHIVE_DIR=/var/data/mail_archive
CONTACT_EMAIL=kontakt@smotrych.com
CONTACT_PHONE=+48 723 698 910
```

Admin lead list:

```text
/admin/notifications
```

If `ADMIN_PASSWORD` is not set, the admin panel is disabled.
