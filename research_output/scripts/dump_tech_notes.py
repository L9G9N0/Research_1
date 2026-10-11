import pymupdf

doc = pymupdf.open("research_output/raw_data/HDR25_Technical_Notes.pdf")

with open("research_output/raw_data/tech_notes_text.txt", "w") as f:
    for i, page in enumerate(doc):
        f.write(f"\n\n==================== PAGE {i+1} ====================\n\n")
        f.write(page.get_text())

print("Saved full text to research_output/raw_data/tech_notes_text.txt")
