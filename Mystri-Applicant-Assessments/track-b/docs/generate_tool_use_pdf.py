#!/usr/bin/env python3
"""Generate TOOL_USE_SUMMARY_Santheesh_S_TrackB.pdf (reportlab). Run from track-b/docs/."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).resolve().parent / "TOOL_USE_SUMMARY_Santheesh_S_TrackB.pdf"


def build_pdf() -> Path:
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    w = doc.width

    title = ParagraphStyle(
        "T", fontName="Helvetica-Bold", fontSize=15, spaceAfter=6, textColor=colors.HexColor("#1a1a1a")
    )
    meta = ParagraphStyle(
        "M", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#555555"), spaceAfter=10, leading=12
    )
    lead = ParagraphStyle(
        "L", fontName="Helvetica-Bold", fontSize=10, spaceBefore=12, spaceAfter=5, textColor=colors.HexColor("#222222")
    )
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=8)
    foot = ParagraphStyle("F", fontName="Helvetica", fontSize=8.5, textColor=colors.HexColor("#666666"), leading=11)
    cell = ParagraphStyle("C", fontName="Helvetica", fontSize=8.5, leading=11.5)
    cell_b = ParagraphStyle("CB", parent=cell, fontName="Helvetica-Bold")

    def P(text: str, style=cell):
        return Paragraph(text, style)

    def table3(headers, rows, col_fracs=(0.21, 0.39, 0.40)):
        cw = [w * f for f in col_fracs]
        data = [[P(f"<b>{h}</b>", cell_b) for h in headers]]
        for r in rows:
            data.append([P(r[0], cell_b), P(r[1], cell), P(r[2], cell)])
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return t

    def table2(headers, rows, col_fracs=(0.32, 0.68)):
        cw = [w * f for f in col_fracs]
        data = [[P(f"<b>{h}</b>", cell_b) for h in headers]]
        for a, b in rows:
            data.append([P(a, cell_b), P(b, cell)])
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f2f2f2")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cccccc")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return t

    story = []
    story.append(Paragraph("Tool-Use Summary", title))
    story.append(
        Paragraph(
            "Santheesh S · Mystri Track B · Product 1 · 3 h 50 min · sivasandy509@gmail.com",
            meta,
        )
    )

    story.append(
        Paragraph(
            "I used AI and local tools under Mystri’s transparency requirement. My submission stands on what "
            "a reviewer can replay: <b>python product1\\verify_product1.py</b> returning <b>PRODUCT 1 PASS</b>, "
            "39 unit tests on unchanged pack <b>data/</b>, and the narrative in <b>DECISION.md</b> and "
            "<b>SOURCES.md</b>. I treat Composer as a fast draft layer; I own the decision, the rules, and the "
            "pass/fail gate.",
            body,
        )
    )

    story.append(
        Paragraph(
            "I work with five habits on a timed build: keep the <b>human decision</b> and let AI handle drafts; "
            "<b>verify before trust</b> on every substantive code change; separate <b>file collection from follow-up "
            "policy</b>; <b>fail closed</b> on ambiguous rows such as R018; and state <b>honest limits</b> rather "
            "than overstating ROI or the owner’s eight-hour claim.",
            body,
        )
    )

    story.append(Paragraph("Tools and how I governed their output", lead))
    story.append(
        table3(
            ["Tool", "What I used it for", "How I checked / corrected / rejected"],
            [
                (
                    "Cursor — Composer",
                    "Scaffolded <b>queue_engine.py</b>, parts of <b>integrated_model.py</b>, test stubs, and doc structure. "
                    "No separate paid LLM API for graded runs.",
                    "After edits: <b>verify_product1.py</b> and full <b>unittest</b>; aligned with "
                    "<b>DATA_DICTIONARY.md</b>; conflicting fields routed to <b>uncertain</b>.",
                ),
                (
                    "Python 3.10+",
                    "Loader, <b>experiment.py</b>, verify gate, 39 tests, dry-run JSON and trace.",
                    "<b>PRODUCT 1 PASS</b>; baseline <b>13</b> vs rules <b>5</b> in "
                    "<b>test_pack_snapshot_baseline_thirteen_rules_five</b>.",
                ),
                (
                    "Manual analysis",
                    "Deduped <b>event_id</b>; naive vs rules counts for <b>DECISION.md</b>.",
                    "Cross-checked CSVs and tests; did not treat owner 8 h/week as measured.",
                ),
                (
                    "Vendor documentation",
                    "OneDrive/Dropbox file-request; Microsoft Learn share-files; Jotform for context.",
                    "Logged in <b>SOURCES.md</b> with dates, claims, and limits.",
                ),
            ],
        )
    )
    story.append(Spacer(1, 6))

    story.append(Paragraph("Division of responsibility", lead))
    story.append(
        table2(
            ["Role", "Responsibility"],
            [
                ("Composer", "Boilerplate, test skeletons, first-pass documentation."),
                ("Me", "Rule semantics, evidence, Product 1 scope, SOURCES claims, pass/fail criteria."),
                ("Reject rule", "If verify or tests fail, I fix or revert — I do not ship failing AI output."),
            ],
        )
    )
    story.append(Spacer(1, 6))

    story.append(Paragraph("Excluded from this submission", lead))
    story.append(
        table2(
            ["Category", "Reason"],
            [
                ("Paid LLM APIs", "Graded proof uses stdlib and local verify only."),
                ("Deployment / hosting", "Dry-run assessment scope."),
                ("Live messaging", "Simulated in trace and JSON only."),
                ("Editing pack data/", "Verify assumes original Mystri CSVs."),
            ],
        )
    )
    story.append(Spacer(1, 6))

    story.append(PageBreak())
    story.append(Paragraph("Example I caught during implementation", lead))
    story.append(
        Paragraph(
            "Composer once emitted an invalid dataclass update in queue code. Unit tests failed immediately. "
            "I rejected that version, rewrote with <b>dataclasses.replace</b>, and re-ran the full suite and verify "
            "until <b>PRODUCT 1 PASS</b>. That is the standard I apply to any AI-generated change.",
            body,
        )
    )
    story.append(
        table2(
            ["Step", "Outcome"],
            [
                ("Problem", "Invalid dataclass update in generated code."),
                ("Signal", "Unit tests failed."),
                ("Action", "Rejected assistant output; fixed with dataclasses.replace."),
                ("Proof", "Full unittest + verify → PRODUCT 1 PASS."),
            ],
        )
    )
    story.append(Spacer(1, 6))

    story.append(Paragraph("Where this lives in the repo", lead))
    story.append(
        table2(
            ["Artifact", "Role"],
            [
                ("DECISION.md", "Decision note with claim, alternatives, counterargument."),
                ("HANDOVER.md", "Run steps, evidence, tool judgment."),
                ("SOURCES.md", "External references and limitations."),
                ("product1/verify_product1.py", "Single reviewer gate."),
            ],
        )
    )

    story.append(Spacer(1, 14))
    story.append(
        Paragraph(
            "github.com/santheesh15/.-mystri-assessment · branch cursor/track-b-submission-edb7 · "
            "track-b/docs/TOOL_USE_SUMMARY.md",
            foot,
        )
    )

    doc.build(story)
    return OUT


if __name__ == "__main__":
    p = build_pdf()
    print(f"Wrote {p} ({p.stat().st_size} bytes)")
