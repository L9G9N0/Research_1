import pymupdf
import re

doc = pymupdf.open("research_output/raw_data/HDR25_Technical_Notes.pdf")
print("Total pages in HDR25_Technical_Notes.pdf:", len(doc))

full_text = []
for i, page in enumerate(doc):
    text = page.get_text()
    full_text.append((i + 1, text))

def search_keywords(keywords):
    print(f"\n--- Searching for: {keywords} ---")
    for page_num, text in full_text:
        for kw in keywords:
            if kw.lower() in text.lower():
                print(f"=== Found '{kw}' on Page {page_num} ===")
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    if kw.lower() in line.lower():
                        snippet = "\n".join(lines[max(0, j-3):min(len(lines), j+8)])
                        print(snippet)
                        print("------")
                break

search_keywords(["goalpost", "geometric mean", "atkinson", "epsilon", "phdi", "material footprint", "gni per capita", "ppp", "planetary"])
