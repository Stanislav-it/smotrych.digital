import json
import math
import os
import sqlite3
import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from flask import (
    Flask, abort, flash, g, redirect, render_template, request, session, url_for
)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "instance"))

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-me"),
    DATA_DIR=DATA_DIR,
    DB_PATH=os.environ.get("DB_PATH", os.path.join(DATA_DIR, "smotrych_leads.sqlite3")),
    LEADS_DIR=os.environ.get("LEADS_DIR", os.path.join(DATA_DIR, "leads")),
    LEADS_JSONL_PATH=os.environ.get("LEADS_JSONL_PATH", os.path.join(DATA_DIR, "leads", "leads.jsonl")),
    MAIL_ARCHIVE_DIR=os.environ.get("MAIL_ARCHIVE_DIR", os.path.join(DATA_DIR, "mail_archive")),
    CONTACT_EMAIL=os.environ.get("CONTACT_EMAIL", "kontakt@smotrych.com"),
    CONTACT_PHONE=os.environ.get("CONTACT_PHONE", "+48 723 698 910"),
    MAIL_TO=os.environ.get("MAIL_TO", "kontakt@smotrych.com"),
    SITE_URL=os.environ.get("SITE_URL", "https://smotrych.digital").rstrip("/"),
    GTM_ID=os.environ.get("GTM_ID", "").strip(),
    GA4_MEASUREMENT_ID=os.environ.get("GA4_MEASUREMENT_ID", "").strip(),
    SMTP_HOST=os.environ.get("SMTP_HOST", ""),
    SMTP_PORT=int(os.environ.get("SMTP_PORT", "587")),
    SMTP_USER=os.environ.get("SMTP_USER", ""),
    SMTP_PASS=os.environ.get("SMTP_PASS", ""),
    SMTP_FROM=os.environ.get("SMTP_FROM", ""),
    SMTP_TLS=str(os.environ.get("SMTP_TLS", "1")).strip().lower() in {"1", "true", "yes", "on"},
    ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", ""),
)


SERVICES = [
    {
        "title": "Strony WWW",
        "text": "Nowoczesne, szybkie strony internetowe projektowane indywidualnie pod ofertę, zaufanie i zapytania od klientów.",
        "number": "01",
        "icon": "web",
        "slug": "strony-www",
    },
    {
        "title": "Sklepy online",
        "text": "Funkcjonalne sklepy internetowe z katalogiem produktów, płatnościami online i wygodną ścieżką zakupu.",
        "number": "02",
        "icon": "shop",
        "slug": "sklepy-online",
    },
    {
        "title": "Marketing",
        "text": "SEO, Google Ads i analityka połączone w jeden system, który mierzy ruch, konwersje i realny wzrost.",
        "number": "03",
        "icon": "analytics",
        "slug": "marketing",
    },
]

PROJECTS = [
    {
        "name": "Velora",
        "category": "E-commerce",
        "title": "Nowoczesny sklep dla ambitnych marek",
        "text": "Strategia, UX i wdrożenie sklepu internetowego dla brandu premium.",
        "image": "img/portfolio/velora_iphone.png",
    },
    {
        "name": "Terra",
        "category": "Branża hotelarska",
        "title": "Cyfrowa obecność dla miejsca blisko natury",
        "text": "Strona wizerunkowa z formularzem rezerwacyjnym i kampanią Google Ads.",
        "image": "img/portfolio/terra_iphone.png",
    },
    {
        "name": "Finova",
        "category": "Finanse",
        "title": "Pełna kontrola finansów. Prawdziwy wzrost.",
        "text": "Landing page, analityka konwersji i optymalizacja ścieżki leadowej.",
        "image": "img/portfolio/finova_iphone.png",
    },
]

HOME_PILLS = [
    {"label": "★ Strony WWW", "active": True},
    {"label": "SEO i Google Ads", "active": False},
    {"label": "Sklepy online", "active": False},
]

HOME_CASES = [
    {
        "title": "X-Estetik",
        "text": "Zrealizowaliśmy trzy strony internetowe oraz prowadzimy SEO, analitykę i kampanie Google Ads, które wspierają stałe pozyskiwanie klientów.",
        "image": "img/home/x-estetik.png",
        "layout": "photo",
    },
    {
        "title": "DocuBeauty",
        "text": "Stworzyliśmy sklep internetowy z płatnościami kartą, BLIK i Apple Pay oraz wdrożyliśmy rozbudowany katalog produktów i dokumentów online.",
        "image": "img/home/docubeauty.png",
        "layout": "logo",
    },
    {
        "title": "Wezpierożki",
        "text": "Zaprojektowaliśmy sklep online z płatnościami internetowymi i dostawą kurierską, dzięki czemu marka może wygodnie przyjmować zamówienia na wynos i rozwijać sprzedaż online.",
        "image": "img/home/wezpierozki.png",
        "layout": "photo",
    },
    {
        "title": "InstaElite",
        "text": "Współpraca obejmuje tworzenie stron, sklepów internetowych, SEO i Google Ads dla klientów firmy — od projektu po wdrożenie i marketing.",
        "image": "img/home/instaelite.png",
        "layout": "logo dark",
    },
    {
        "title": "SEOMotive",
        "text": "Dla agencji partnerskiej Google realizujemy strony internetowe dla klientów, łącząc szybkie wdrożenia z czytelną strukturą i gotowością pod kampanie.",
        "image": "img/home/seomotive.png",
        "layout": "photo",
    },
    {
        "title": "Kosmetik Studio Kassel",
        "text": "Dla kosmetycznego gabinetu w Niemczech stworzyliśmy stronę z możliwością umawiania terminów oraz wdrożyliśmy SEO, analitykę i Google Ads, aby pozyskiwać nowych klientów.",
        "image": "img/home/kosmetik-studio-kassel-banner.png",
        "layout": "photo",
    },
    {
        "title": "Poniedziałek Kosmetyka",
        "text": "Stworzyliśmy estetyczną stronę usługową dla marki beauty, która porządkuje ofertę, buduje profesjonalny wizerunek i ułatwia klientkom szybki kontakt oraz poznanie zabiegów.",
        "image": "img/home/poniedzialek-kosmetyka-banner.jpg",
        "layout": "photo",
        "image_class": "is-poniedzialek-banner",
    },
]

PROCESS = [
    ("01", "Analiza", "Poznajemy Twój biznes, cele, odbiorców i wyzwania."),
    ("02", "Strategia", "Tworzymy plan działania dopasowany do Twoich potrzeb."),
    ("03", "Realizacja", "Projektujemy, rozwijamy i wdrażamy z najwyższą precyzją."),
    ("04", "Optymalizacja", "Analizujemy wyniki i stale je usprawniamy."),
]

FAQ = [
    {
        "q": "Ile trwa stworzenie strony internetowej?",
        "a": "Najczęściej od 2 do 6 tygodni. Dokładny termin zależy od zakresu, liczby podstron i materiałów wejściowych.",
    },
    {
        "q": "Czy pomagacie z tekstami i strukturą strony?",
        "a": "Tak. Pomagamy ułożyć strukturę, komunikaty, CTA oraz treści pod użytkownika i wyszukiwarki.",
    },
    {
        "q": "Czy strona będzie responsywna?",
        "a": "Tak. Projekt jest przygotowany pod desktop, tablet i telefon, z mobilnym menu oraz czytelną typografią.",
    },
    {
        "q": "Czy można podłączyć Google Analytics i piksele reklamowe?",
        "a": "Tak. Wdrażamy analitykę, zdarzenia konwersji i podstawowe narzędzia do pomiaru skuteczności kampanii.",
    },
]

PAGES = {
    "uslugi": {
        "kicker": "Nasze usługi",
        "title": "Co robimy",
        "lead": "Projektujemy strony WWW, sklepy online oraz marketing oparty na SEO, Google Ads i analityce.",
        "template": "services.html",
    },
    "strony-www": {
        "kicker": "Strony WWW",
        "title": "Strony, które sprzedają",
        "lead": "Projektujemy szybkie, wiarygodne i nastawione na konwersję strony internetowe dla firm, które chcą wyglądać profesjonalnie i pozyskiwać klientów online.",
        "template": "websites.html",
    },
    "sklepy-online": {
        "kicker": "Sklepy online",
        "title": "Sklepy, które ułatwiają zakup",
        "lead": "Tworzymy sklepy internetowe z czytelnym katalogiem, płatnościami online, wygodną ścieżką zamówienia i strukturą gotową pod sprzedaż oraz SEO.",
        "template": "shops.html",
    },
    "marketing": {
        "kicker": "Marketing",
        "title": "Marketing oparty na danych",
        "lead": "Łączymy SEO, Google Ads i analitykę, aby nie tylko sprowadzać ruch na stronę, ale mierzyć zapytania, kliknięcia i realne wyniki kampanii.",
        "template": "marketing.html",
    },
    "o-nas": {
        "kicker": "O nas",
        "title": "Skoncentrowani na Twoim rozwoju",
        "lead": "Jesteśmy zespołem ekspertów cyfrowych, którzy z pasją pomagają firmom rozwijać się dzięki nowoczesnym stronom internetowym, skutecznemu marketingowi i przemyślanej strategii.",
        "template": "about.html",
    },
    "proces": {
        "kicker": "Nasz proces",
        "title": "Jak pracujemy",
        "lead": "Przejrzysty proces, konkretne decyzje i regularna optymalizacja — od pierwszej rozmowy po wyniki.",
        "template": "process.html",
    },
    "blog": {
        "kicker": "Blog",
        "title": "Blog",
        "lead": "Miejsce na artykuły, case studies i praktyczne wskazówki. Strona zostanie uzupełniona wkrótce.",
        "template": "blog.html",
    },
    "kontakt": {
        "kicker": "Kontakt",
        "title": "Porozmawiajmy o Twoim projekcie",
        "lead": "Napisz do nas bezpośrednio lub zostaw kilka informacji o projekcie — wrócimy z konkretną odpowiedzią.",
        "template": "contact.html",
    },
    "subskrypcja": {
        "kicker": "Subskrypcja",
        "title": "Dołącz do inner circle",
        "lead": "Zapisz się po konkretne wskazówki, case studies i aktualizacje o stronach, sklepach oraz kampaniach.",
        "template": "subscribe.html",
    },
}


def redirect_with_lead_success(target_url: str, lead_id: int, source: str):
    """Append a short-lived success marker so client-side GTM can fire the confirmed lead event."""
    try:
        target_url = target_url or url_for("page", slug="kontakt")
        split = urlsplit(target_url)
        params = dict(parse_qsl(split.query, keep_blank_values=True))
        params.update({
            "lead": "success",
            "lead_id": str(lead_id),
            "lead_source": (source or "lead_form")[:80],
        })
        return urlunsplit((split.scheme, split.netloc, split.path, urlencode(params), split.fragment))
    except Exception:
        return url_for("page", slug="kontakt", lead="success", lead_id=lead_id, lead_source=(source or "lead_form")[:80])


# --- Contact form / lead capture logic -------------------------------------------------
def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db_path = app.config["DB_PATH"]
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db = sqlite3.connect(db_path, check_same_thread=False)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA journal_mode=WAL;")
            db.execute("PRAGMA synchronous=NORMAL;")
        except Exception:
            pass
        g._db = db
    return db


@app.teardown_appcontext
def close_db(_error=None):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(app.config["DATA_DIR"], exist_ok=True)
    os.makedirs(app.config["LEADS_DIR"], exist_ok=True)
    os.makedirs(app.config["MAIL_ARCHIVE_DIR"], exist_ok=True)
    db = sqlite3.connect(app.config["DB_PATH"])
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS leads(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                message TEXT,
                source TEXT,
                ip TEXT,
                user_agent TEXT,
                created_at TEXT NOT NULL
            )
        """)
        db.commit()
    finally:
        db.close()


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def archive_lead_to_disk(*, lead_id: int, created_at: str, name: str, email: str, phone: str, message: str, source: str, ip: str, user_agent: str) -> None:
    leads_dir = (app.config.get("LEADS_DIR") or "").strip()
    jsonl_path = (app.config.get("LEADS_JSONL_PATH") or "").strip()

    if not leads_dir and not jsonl_path:
        return

    try:
        payload = {
            "id": int(lead_id),
            "created_at_utc": created_at,
            "name": name,
            "email": email,
            "phone": phone,
            "message": message,
            "source": source,
            "ip": ip,
            "user_agent": user_agent,
        }
        safe_ts = created_at.replace(":", "").replace("-", "").replace("T", "_")

        if leads_dir:
            os.makedirs(leads_dir, exist_ok=True)
            lead_path = os.path.join(leads_dir, f"lead_{lead_id}_{safe_ts}.json")
            with open(lead_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

        if jsonl_path:
            jsonl_dir = os.path.dirname(jsonl_path)
            if jsonl_dir:
                os.makedirs(jsonl_dir, exist_ok=True)
            with open(jsonl_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False))
                f.write("\n")
    except Exception as exc:
        print(f"[WARN] Failed to archive lead to disk: {exc}")


def send_lead_email(*, name: str, email: str, phone: str, message: str, source: str, lead_id: Optional[int] = None, created_at: Optional[str] = None) -> bool:
    mail_to = (app.config.get("MAIL_TO") or "").strip()
    smtp_host = (app.config.get("SMTP_HOST") or "").strip()
    smtp_user = (app.config.get("SMTP_USER") or "").strip()
    smtp_pass = (app.config.get("SMTP_PASS") or "").strip()
    smtp_from = (app.config.get("SMTP_FROM") or "").strip() or smtp_user
    smtp_port = int(app.config.get("SMTP_PORT") or 587)
    smtp_tls = bool(app.config.get("SMTP_TLS"))

    if not (mail_to and smtp_host and smtp_from):
        return False

    try:
        msg = EmailMessage()
        msg["Subject"] = "Nowe zapytanie — Smotrych Digital"
        msg["From"] = smtp_from
        msg["To"] = mail_to
        if email:
            msg["Reply-To"] = email

        lines = [
            "Nowe zapytanie z formularza kontaktowego Smotrych Digital:",
            "",
            f"ID: {lead_id or '-'}",
            f"Czas (UTC): {created_at or datetime.utcnow().isoformat(timespec='seconds')}",
            f"Źródło: {source or '-'}",
            "",
            f"Imię i nazwisko: {name or '-'}",
            f"E-mail: {email or '-'}",
            f"Telefon: {phone or '-'}",
            "",
            "Wiadomość:",
            message or "-",
        ]
        msg.set_content("\n".join(lines))

        try:
            archive_dir = (app.config.get("MAIL_ARCHIVE_DIR") or "").strip()
            if archive_dir and lead_id is not None and created_at:
                os.makedirs(archive_dir, exist_ok=True)
                safe_ts = created_at.replace(":", "").replace("-", "").replace("T", "_")
                eml_path = os.path.join(archive_dir, f"lead_{lead_id}_{safe_ts}.eml")
                with open(eml_path, "wb") as f:
                    f.write(msg.as_bytes())
        except Exception as exc:
            print(f"[WARN] Failed to archive email: {exc}")

        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.ehlo()
            if smtp_tls:
                server.starttls()
                server.ehlo()
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as exc:
        print(f"[WARN] Failed to send lead email: {exc}")
        return False


def admin_required():
    password = (app.config.get("ADMIN_PASSWORD") or "").strip()
    if not password:
        abort(404)
    if session.get("admin_logged_in") is True:
        return None
    return redirect(url_for("admin_login", next=request.path))


@app.post("/lead")
def lead():
    # Honeypot: bots often fill hidden fields. We silently accept and drop it.
    if (request.form.get("website") or "").strip():
        flash("Dziękujemy. Skontaktujemy się wkrótce.", "success")
        return redirect(request.referrer or url_for("page", slug="kontakt"))

    name = (request.form.get("full_name") or request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    message = (request.form.get("project_description") or request.form.get("message") or "").strip()
    source = (request.form.get("source") or request.referrer or "contact").strip()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
    user_agent = request.headers.get("User-Agent", "")

    if not email and not phone:
        flash("Podaj e-mail lub telefon, abyśmy mogli się skontaktować.", "error")
        return redirect(request.referrer or url_for("page", slug="kontakt"))

    created_at = datetime.utcnow().isoformat(timespec="seconds")
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO leads(name, email, phone, message, source, ip, user_agent, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (name, email, phone, message, source, ip, user_agent, created_at),
    )
    lead_id = cur.lastrowid
    db.commit()

    archive_lead_to_disk(
        lead_id=lead_id,
        created_at=created_at,
        name=name,
        email=email,
        phone=phone,
        message=message,
        source=source,
        ip=ip,
        user_agent=user_agent,
    )

    send_lead_email(
        name=name,
        email=email,
        phone=phone,
        message=message,
        source=source,
        lead_id=lead_id,
        created_at=created_at,
    )

    flash("Dziękujemy. Skontaktujemy się wkrótce.", "success")
    return redirect(redirect_with_lead_success(request.referrer or url_for("page", slug="kontakt"), lead_id, source))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    password = (app.config.get("ADMIN_PASSWORD") or "").strip()
    if not password:
        abort(404)

    if request.method == "POST":
        if (request.form.get("password") or "") == password:
            session["admin_logged_in"] = True
            return redirect(request.args.get("next") or url_for("admin_notifications"))
        flash("Nieprawidłowe hasło.", "error")

    return render_template("admin/login.html", current="admin")


@app.get("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.get("/admin/notifications")
def admin_notifications():
    guard = admin_required()
    if guard:
        return guard

    q = (request.args.get("q", "") or "").strip()
    try:
        page = max(1, int(request.args.get("page", "1") or 1))
    except Exception:
        page = 1

    per_page = 50
    offset = (page - 1) * per_page
    where = []
    params = []
    if q:
        where.append("(name LIKE ? OR email LIKE ? OR phone LIKE ? OR message LIKE ? OR source LIKE ?)")
        qq = f"%{q}%"
        params.extend([qq, qq, qq, qq, qq])
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""

    db = get_db()
    total = db.execute(f"SELECT COUNT(1) AS c FROM leads{where_sql}", params).fetchone()["c"]
    rows = db.execute(
        f"SELECT * FROM leads{where_sql} ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?",
        params + [per_page, offset],
    ).fetchall()
    total_pages = max(1, math.ceil((total or 0) / per_page))

    return render_template(
        "admin/notifications.html",
        leads=[row_to_dict(row) for row in rows],
        q=q,
        page=page,
        total_pages=total_pages,
        total=total,
        current="admin",
    )


with app.app_context():
    init_db()



@app.route("/")
def index():
    return render_template(
        "index.html",
        services=SERVICES,
        projects=PROJECTS,
        process=PROCESS,
        faq=FAQ,
        home_pills=HOME_PILLS,
        home_cases=HOME_CASES,
        current="home",
    )


@app.route("/<slug>")
def page(slug):
    page_data = PAGES.get(slug)
    if not page_data:
        abort(404)
    return render_template(
        page_data["template"],
        page=page_data,
        services=SERVICES,
        projects=PROJECTS,
        process=PROCESS,
        faq=FAQ,
        home_cases=HOME_CASES,
        current=slug,
    )




@app.get("/robots.txt")
def robots_txt():
    site_url = app.config.get("SITE_URL", "https://smotrych.digital").rstrip("/")
    body = "\n".join([
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {site_url}/sitemap.xml",
        "",
    ])
    return app.response_class(body, mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap_xml():
    from xml.sax.saxutils import escape

    site_url = app.config.get("SITE_URL", "https://smotrych.digital").rstrip("/")
    urls = [site_url + "/"]
    urls.extend(f"{site_url}/{slug}" for slug in PAGES.keys())
    items = "".join(
        f"<url><loc>{escape(url)}</loc><changefreq>weekly</changefreq><priority>{'1.0' if url == site_url + '/' else '0.8'}</priority></url>"
        for url in urls
    )
    xml = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">{items}</urlset>"
    return app.response_class(xml, mimetype="application/xml")

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", current="404"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
