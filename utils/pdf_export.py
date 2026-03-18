"""PDF export using FPDF2."""
import re
from fpdf import FPDF


def _safe(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2012": "-",
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2022": "*", "\u2023": "*", "\u25cf": "*",
        "\u2192": "->", "\u2190": "<-", "\u2194": "<->",
        "\u2260": "!=", "\u2264": "<=", "\u2265": ">=",
        "\u2026": "...", "\u00b0": " degrees",
        "\u03b1": "alpha", "\u03b2": "beta", "\u03c0": "pi",
    }
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def export_notes_pdf(skill: str, topic: str, content: str) -> bytes:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=20, top=20, right=20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 8, _safe(f"SkillTrack AI  |  {skill}: {topic}"))
    pdf.ln(2)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(4)

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            pdf.ln(2)
            continue

        if stripped.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(80, 80, 180)
            pdf.multi_cell(0, 6, _safe(stripped[4:]))
            pdf.set_text_color(40, 40, 40)
        elif stripped.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.set_text_color(60, 60, 160)
            pdf.multi_cell(0, 7, _safe(stripped[3:]))
            pdf.set_text_color(40, 40, 40)
        elif stripped.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=13)
            pdf.set_text_color(40, 40, 140)
            pdf.multi_cell(0, 8, _safe(stripped[2:]))
            pdf.set_text_color(40, 40, 40)
        elif stripped.startswith(("- ", "* ")):
            pdf.set_font("Helvetica", size=9)
            pdf.multi_cell(0, 5, _safe("  * " + stripped[2:]))
        else:
            clean = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
            clean = re.sub(r"\*(.+?)\*",     r"\1", clean)
            clean = re.sub(r"`(.+?)`",        r"\1", clean)
            clean = re.sub(r"#{1,6}\s*",      "",    clean)
            pdf.set_font("Helvetica", size=9)
            pdf.multi_cell(0, 5, _safe(clean))

    return bytes(pdf.output())
