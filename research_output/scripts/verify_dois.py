import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# List of DOIs and URLs to verify
test_items = [
    ("Preston 1975", "10.2307/2173509"),
    ("Pritchett & Summers 1996", "10.2307/2137666"),
    ("Jones & Klenow 2016", "10.1257/aer.20110236"),
    ("Kubiszewski et al. 2013", "10.1016/j.ecolecon.2013.04.019"),
    ("Ravallion 2012", "10.1016/j.jdeveco.2011.05.008"),
    ("Klugman Rodriguez Choi 2011", "10.1007/s10888-011-9189-y"),
    ("Easterlin et al. 2010", "10.1073/pnas.1015962107"),
    ("Stevenson & Wolfers 2008", "10.1353/eca.0.0001"),
    ("Kahneman & Deaton 2010", "10.1073/pnas.1011492107"),
    ("Killingsworth et al. 2023", "10.1073/pnas.2208661120"),
    ("Kuznets 1955", "10.2307/1811581"),
    ("Grossman & Krueger 1995", "10.2307/2946695"),
    ("Haberl et al. 2020", "10.1088/1748-9326/ab7d82"),
    ("Cameron & Miller 2015", "10.3368/jhr.50.2.317"),
    ("Alkire & Foster 2011", "10.1016/j.jpubeco.2011.01.009"),
    ("OECD 2018 For Good Measure", "10.1787/9789264307278-en"),
    ("OECD 2018 Beyond GDP", "10.1787/9789264307292-en")
]

for label, doi in test_items:
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResearchAssistant/1.0 (mailto:academic@research.org)'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))['message']
            title = data.get('title', [''])[0]
            authors = [f"{a.get('family', '')}, {a.get('given', '')[:1]}." for a in data.get('author', [])]
            container = data.get('container-title', [''])[0]
            year = data.get('issued', {}).get('date-parts', [[None]])[0][0]
            vol = data.get('volume', '')
            issue = data.get('issue', '')
            page = data.get('page', '')
            print(f"VERIFIED: {label} -> {', '.join(authors[:3])} ({year}). {title}. {container}, {vol}({issue}), {page}. https://doi.org/{doi}")
    except Exception as e:
        print(f"FAILED: {label} ({doi}) -> {e}")
    time.sleep(0.2)
