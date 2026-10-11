import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls_to_test = [
    ("Kuznets 1934 (FRASER)", "https://fraser.stlouisfed.org/title/national-income-1929-1932-971"),
    ("Nordhaus & Tobin 1972 (NBER PDF)", "https://www.nber.org/system/files/chapters/c7620/c7620.pdf"),
    ("Stiglitz Sen Fitoussi 2009 (Eurostat)", "https://ec.europa.eu/eurostat/documents/8131721/8131772/Stiglitz-Sen-Fitoussi-Commission-report.pdf"),
    ("OECD 2018 Beyond GDP (DOI)", "https://doi.org/10.1787/9789264307292-en"),
    ("OECD 2018 For Good Measure (DOI)", "https://doi.org/10.1787/9789264307278-en"),
    ("UNDP 1990 (Official)", "https://hdr.undp.org/content/human-development-report-1990"),
    ("UNDP 2025 (Official)", "https://hdr.undp.org/content/human-development-report-2025"),
    ("UNDP Data Center Downloads", "https://hdr.undp.org/data-center/documentation-and-downloads"),
    ("WB NY.GDP.PCAP.KD", "https://data.worldbank.org/indicator/NY.GDP.PCAP.KD"),
    ("WB NY.GDP.PCAP.KD.ZG", "https://data.worldbank.org/indicator/NY.GDP.PCAP.KD.ZG"),
    ("WB NY.GDP.PCAP.PP.KD", "https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD"),
    ("WB SI.POV.GINI", "https://data.worldbank.org/indicator/SI.POV.GINI"),
    ("WB SP.DYN.LE00.IN", "https://data.worldbank.org/indicator/SP.DYN.LE00.IN"),
    ("IMF Callen GDP", "https://www.imf.org/en/Publications/fandd/issues/Series/Back-to-Basics/gross-domestic-product-GDP"),
    ("Grossman & Krueger 1995 (DOI)", "https://doi.org/10.2307/2118443"),
    ("Klugman Rodriguez Choi 2011 (DOI)", "https://doi.org/10.1007/s10888-011-9178-z"),
    ("Haberl et al. 2020 (DOI)", "https://doi.org/10.1088/1748-9326/ab7d7f"),
    ("Pritchett & Summers 1996 (DOI)", "https://doi.org/10.2307/146149"),
    ("Ravallion 2012 (DOI)", "https://doi.org/10.1016/j.jdeveco.2012.01.003"),
    ("Hicks 1997 (DOI)", "https://doi.org/10.1016/S0305-750X(97)00034-X"),
    ("Alkire & Foster 2011 (DOI)", "https://doi.org/10.1016/j.jpubeco.2010.11.006"),
    ("Jones & Klenow 2016 (DOI)", "https://doi.org/10.1257/aer.20110236"),
    ("Kubiszewski et al. 2013 (DOI)", "https://doi.org/10.1016/j.ecolecon.2013.04.019"),
    ("Costanza et al. 2014 (DOI)", "https://doi.org/10.1038/505283a"),
    ("Easterlin et al. 2010 (DOI)", "https://doi.org/10.1073/pnas.1015962107"),
    ("Stevenson & Wolfers 2008 (DOI)", "https://doi.org/10.1353/eca.0.0001"),
    ("Kahneman & Deaton 2010 (DOI)", "https://doi.org/10.1073/pnas.1011492107"),
    ("Killingsworth et al. 2023 (DOI)", "https://doi.org/10.1073/pnas.2208661120"),
    ("Hickel 2020 (DOI)", "https://doi.org/10.1016/j.ecolecon.2019.05.011"),
    ("O'Neill et al. 2018 (DOI)", "https://doi.org/10.1038/s41893-018-0021-4"),
    ("Fanning et al. 2022 (DOI)", "https://doi.org/10.1038/s41893-021-00799-z"),
    ("Vogel et al. 2021 (DOI)", "https://doi.org/10.1016/j.gloenvcha.2021.102287"),
    ("Cameron & Miller 2015 (DOI)", "https://doi.org/10.3368/jhr.50.2.317")
]

print(f"Testing {len(urls_to_test)} URLs/DOIs...")
for label, url in urls_to_test:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            print(f"SUCCESS {resp.status}: {label} -> {url}")
    except urllib.error.HTTPError as e:
        # Note: 403 Forbidden is common when scrapers hit JSTOR or PNAS directly, but the DOI itself resolves
        print(f"HTTP {e.code}: {label} -> {url}")
    except Exception as e:
        print(f"FAILED: {label} -> {e}")
