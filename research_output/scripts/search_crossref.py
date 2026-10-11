import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queries = [
    "Grossman Krueger 1995 Economic Growth and the Environment Quarterly Journal of Economics",
    "Klugman Rodriguez Choi 2011 The HDI 2010 New controversies old critiques Journal of Economic Inequality",
    "Haberl 2020 systematic review evidence decoupling GDP resource use GHG emissions Environmental Research Letters",
    "Costanza 2014 Development Time to leave GDP behind Nature",
    "O'Neill 2018 A good life for all within planetary boundaries Nature Sustainability",
    "Fanning 2022 The social shortfall and ecological overshoot of nations Nature Sustainability",
    "Hickel 2020 The sustainable development index Ecological Economics",
    "Sarracino O'Connor 2023 Neo-humanism and the wellbeing economy",
    "Vogel 2021 Socio-economic conditions for satisfying human needs at low energy use Global Environmental Change",
    "Tim Callen Gross Domestic Product An Economy's All Finance Development IMF"
]

for q in queries:
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&rows=2"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ResearchAssistant/1.0 (mailto:academic@research.org)'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))['message']['items']
            if data:
                top = data[0]
                title = top.get('title', [''])[0]
                doi = top.get('DOI', '')
                container = top.get('container-title', [''])[0]
                year = top.get('issued', {}).get('date-parts', [[None]])[0][0]
                authors = [f"{a.get('family', '')}, {a.get('given', '')[:1]}." for a in top.get('author', [])]
                print(f"QUERY: {q[:30]}...")
                print(f"  MATCH: {', '.join(authors[:3])} ({year}). {title}. {container}. https://doi.org/{doi}\n")
    except Exception as e:
        print(f"FAILED {q}: {e}")
    time.sleep(0.3)
