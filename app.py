from flask import Flask, render_template, abort

app = Flask(__name__)

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


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", current="404"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
