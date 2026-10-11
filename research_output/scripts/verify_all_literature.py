import urllib.request
import urllib.error
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sources_to_verify = [
    # 1. History & Limits of GDP
    {
        "id": "Kuznets1934",
        "theme": "History and limits of GDP/national accounts",
        "type": "gov_doc",
        "url": "https://fraser.stlouisfed.org/title/national-income-1929-1932-971",
        "cite": "Kuznets (1934)"
    },
    {
        "id": "NordhausTobin1972",
        "theme": "History and limits of GDP/national accounts",
        "type": "book_chapter",
        "url": "https://www.nber.org/books-and-chapters/economic-growth/is-growth-obsolete",
        "cite": "Nordhaus & Tobin (1972)"
    },
    {
        "id": "Coyle2014",
        "theme": "History and limits of GDP/national accounts",
        "type": "book",
        "doi": "10.1515/9781400849765",
        "cite": "Coyle (2014)"
    },
    {
        "id": "StiglitzSenFitoussi2009",
        "theme": "History and limits of GDP/national accounts",
        "type": "report",
        "url": "https://ec.europa.eu/eurostat/documents/8131721/8131772/Stiglitz-Sen-Fitoussi-Commission-report.pdf",
        "cite": "Stiglitz, Sen, & Fitoussi (2009)"
    },
    {
        "id": "StiglitzFitoussiDurand2018_BeyondGDP",
        "theme": "History and limits of GDP/national accounts",
        "type": "book",
        "doi": "10.1787/9789264307292-en",
        "cite": "Stiglitz, Fitoussi, & Durand (2018)"
    },
    {
        "id": "StiglitzFitoussiDurand2018_ForGoodMeasure",
        "theme": "GDP vs alternative welfare measures",
        "type": "book",
        "doi": "10.1787/9789264307278-en",
        "cite": "Stiglitz, Fitoussi, & Durand (Eds.) (2018)"
    },
    # 2. Income & Health
    {
        "id": "Preston1975",
        "theme": "Income and health",
        "type": "journal",
        "doi": "10.2307/2173509",
        "cite": "Preston (1975)"
    },
    {
        "id": "PritchettSummers1996",
        "theme": "Income and health",
        "type": "journal",
        "doi": "10.2307/146149",
        "cite": "Pritchett & Summers (1996)"
    },
    # 3. Income & Education / Capabilities
    {
        "id": "Sen1999",
        "theme": "Income and education / capabilities",
        "type": "book",
        "url": "https://opac.sub.uni-goettingen.de/DB=1/PPN?PPN=271928066",
        "isbn": "9780198297581",
        "cite": "Sen (1999)"
    },
    # 4. HDI/IHDI Critiques & Alternatives
    {
        "id": "Hicks1997",
        "theme": "HDI/IHDI critiques and alternatives",
        "type": "journal",
        "doi": "10.1016/S0305-750X(97)00034-X",
        "cite": "Hicks (1997)"
    },
    {
        "id": "AlkireFoster2011",
        "theme": "HDI/IHDI critiques and alternatives",
        "type": "journal",
        "doi": "10.1016/j.jpubeco.2010.11.006",
        "cite": "Alkire & Foster (2011)"
    },
    {
        "id": "KlugmanRodriguezChoi2011",
        "theme": "HDI/IHDI critiques and alternatives",
        "type": "journal",
        "doi": "10.1007/s10888-011-9178-1",
        "cite": "Klugman, Rodriguez, & Choi (2011)"
    },
    {
        "id": "Ravallion2012",
        "theme": "HDI/IHDI critiques and alternatives",
        "type": "journal",
        "doi": "10.1016/j.jdeveco.2012.01.003",
        "cite": "Ravallion (2012)"
    },
    # 5. GDP vs Alternative Welfare Measures
    {
        "id": "JonesKlenow2016",
        "theme": "GDP vs alternative welfare measures",
        "type": "journal",
        "doi": "10.1257/aer.20110236",
        "cite": "Jones & Klenow (2016)"
    },
    {
        "id": "KubiszewskiEtAl2013",
        "theme": "GDP vs alternative welfare measures",
        "type": "journal",
        "doi": "10.1016/j.ecolecon.2013.04.019",
        "cite": "Kubiszewski et al. (2013)"
    },
    {
        "id": "CostanzaEtAl2009",
        "theme": "GDP vs alternative welfare measures",
        "type": "report",
        "url": "https://www.bu.edu/pardee/files/documents/PP-004-Beyond-GDP.pdf",
        "cite": "Costanza et al. (2009)"
    },
    # 6. Income & Subjective Well-being
    {
        "id": "Easterlin1974",
        "theme": "Income and subjective well-being",
        "type": "book_chapter",
        "doi": "10.1016/B978-0-12-205050-3.50008-7",
        "cite": "Easterlin (1974)"
    },
    {
        "id": "EasterlinEtAl2010",
        "theme": "Income and subjective well-being",
        "type": "journal",
        "doi": "10.1073/pnas.1015962107",
        "cite": "Easterlin et al. (2010)"
    },
    {
        "id": "StevensonWolfers2008",
        "theme": "Income and subjective well-being",
        "type": "journal",
        "doi": "10.1353/eca.0.0001",
        "cite": "Stevenson & Wolfers (2008)"
    },
    {
        "id": "KahnemanDeaton2010",
        "theme": "Income and subjective well-being",
        "type": "journal",
        "doi": "10.1073/pnas.1011492107",
        "cite": "Kahneman & Deaton (2010)"
    },
    {
        "id": "KillingsworthKahnemanMellers2023",
        "theme": "Income and subjective well-being",
        "type": "journal",
        "doi": "10.1073/pnas.2208661120",
        "cite": "Killingsworth, Kahneman, & Mellers (2023)"
    },
    # 7. Growth, Environment & Decoupling
    {
        "id": "GrossmanKrueger1995",
        "theme": "Growth, environment, decoupling",
        "type": "journal",
        "doi": "10.2307/2946693",
        "cite": "Grossman & Krueger (1995)"
    },
    {
        "id": "HaberlEtAl2020",
        "theme": "Growth, environment, decoupling",
        "type": "journal",
        "doi": "10.1088/1748-9326/ab7d7f",
        "cite": "Haberl et al. (2020)"
    },
    {
        "id": "ParriqueEtAl2019",
        "theme": "Growth, environment, decoupling",
        "type": "report",
        "url": "https://eeb.org/library/decoupling-debunked/",
        "cite": "Parrique et al. (2019)"
    },
    # 8. Distribution & Growth
    {
        "id": "Kuznets1955",
        "theme": "Distribution and growth",
        "type": "journal",
        "url": "https://www.jstor.org/stable/1811581",
        "cite": "Kuznets (1955)"
    },
    # 9. Panel-data / Fixed-effects practice
    {
        "id": "CameronMiller2015",
        "theme": "Panel-data/fixed-effects practice",
        "type": "journal",
        "doi": "10.3368/jhr.50.2.317",
        "cite": "Cameron & Miller (2015)"
    }
]

print(f"Total sources queued: {len(sources_to_verify)}")

results = []
for s in sources_to_verify:
    item_res = dict(s)
    doi = s.get('doi')
    url = s.get('url')
    
    # Verify DOI via CrossRef
    if doi:
        cr_url = f"https://api.crossref.org/works/{doi}"
        try:
            req = urllib.request.Request(cr_url, headers={'User-Agent': 'ResearchAssistant/1.0 (mailto:academic@research.org)'})
            with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
                status = resp.status
                data = json.loads(resp.read().decode('utf-8'))['message']
                item_res['doi_http_status'] = status
                item_res['verified_title'] = data.get('title', [''])[0]
                authors_list = data.get('author', [])
                auth_str = ", ".join([f"{a.get('family', '')}, {a.get('given', '')[:1]}." for a in authors_list[:4]])
                if len(authors_list) > 4:
                    auth_str += ", et al."
                item_res['verified_authors'] = auth_str
                item_res['verified_container'] = data.get('container-title', [''])[0]
                item_res['verified_year'] = data.get('issued', {}).get('date-parts', [[None]])[0][0]
                item_res['verified_volume'] = data.get('volume', '')
                item_res['verified_issue'] = data.get('issue', '')
                item_res['verified_page'] = data.get('page', '')
                item_res['doi_link'] = f"https://doi.org/{doi}"
                print(f"[DOI 200 OK] {s['cite']}: {item_res['verified_title'][:60]}... ({item_res['verified_year']})")
        except Exception as e:
            item_res['doi_http_status'] = f"Error: {e}"
            print(f"[DOI FAILED] {s['cite']} ({doi}): {e}")
            
    # Verify URL via HTTP GET/HEAD
    target_url = item_res.get('doi_link') or url
    if target_url:
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
                item_res['url_http_status'] = resp.status
                item_res['url_final'] = resp.geturl()
                print(f"[URL 200 OK] {target_url} -> {resp.status}")
        except urllib.error.HTTPError as e:
            item_res['url_http_status'] = e.code
            print(f"[URL HTTP {e.code}] {target_url}")
        except Exception as e:
            item_res['url_http_status'] = f"Error: {e}"
            print(f"[URL FAILED] {target_url}: {e}")
            
    results.append(item_res)
    time.sleep(0.3)

with open("research_output/verified_literature_metadata.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nVerification complete! Saved to research_output/verified_literature_metadata.json")
