#!/usr/bin/env python3
"""Generate TOOL_USE_SUMMARY_Santheesh_S_TrackB.pdf (reportlab). Run from track-b/docs/."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "TOOL_USE_SUMMARY_Santheesh_S_TrackB.pdf"


def build_pdf() -> Path:
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )
    w = doc.width

    title = ParagraphStyle("T", fontName="Helvetica-Bold", fontSize=14, spaceAfter=5)
    meta = ParagraphStyle("M", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#444"), spaceAfter=6)
    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=10, spaceBefore=6, spaceAfter=3)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=9.5, leading=12, spaceAfter=5)
    cell = ParagraphStyle("C", fontName="Helvetica", fontSize=8.5, leading=11)
    cell_b = ParagraphStyle("CB", parent=cell, fontName="Helvetica-Bold")

    def P(text: str, style=cell):
        return Paragraph(text, style)

    def table3(headers, rows, col_fracs=(0.22, 0.38, 0.40)):
        cw = [w * f for f in col_fracs]
        data = [[P(f"<b>{h}</b>", cell_b) for h in headers]]
        for r in rows:
            data.append([P(r[0], cell_b), P(r[1], cell), P(r[2], cell)])
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#bbbbbb")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        return t

    def table2(headers, rows, col_fracs=(0.35, 0.65)):
        cw = [w * f for f in col_fracs]
        data = [[P(f"<b>{h}</b>", cell_b) for h in headers]]
        for a, b in rows:
            data.append([P(a, cell_b), P(b, cell)])
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e6e6")),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#bbbbbb")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        return t

    story = []
    story.append(Paragraph("Tool-Use Summary", title))
    story.append(
        Paragraph(
            "<b>Santheesh S</b> · Mystri Track B · Product 1 (DICM Core) · <b>3 h 50 min (230 min)</b>",
            meta,
        )
    )
    story.append(Paragraph("sivasandy509@gmail.com", meta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Purpose and evidence standard", h1))
    story.append(
        Paragraph(
            "I document tools because Mystri requires transparency. My <b>authoritative evidence</b> is: "
            "<b>python product1\\verify_product1.py</b> → <b>PRODUCT 1 PASS</b>, 39 unit tests, unchanged "
            "<b>data/</b>, plus <b>DECISION.md</b> and <b>SOURCES.md</b>. AI assists drafts; I own decisions.",
            body,
        )
    )

    story.append(Paragraph("2. Working principles (theory)", h1))
    principles = [
        "<b>Human decision, AI draft</b> — recommendation and rules are mine after review.",
        "<b>Verify before trust</b> — no AI code ships without verify + tests on the pack.",
        "<b>Collection ≠ policy</b> — file-request tools do not replace 48h/opt-out/reconciliation.",
        "<b>Fail closed</b> — ambiguous rows (e.g. R018) → uncertain, not auto-send.",
        "<b>Honest limits</b> — I do not claim live ROI or the owner’s 8 h/week as measured.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(p, body), leftIndent=10) for p in principles],
            bulletType="bullet",
            start="•",
        )
    )

    story.append(Paragraph("3. Tool disclosure table (mandatory)", h1))
    story.append(
        table3(
            ["Tool", "What I used it for", "How I checked / corrected / rejected"],
            [
                (
                    "Cursor — Composer",
                    "Scaffolded <b>queue_engine.py</b>, parts of <b>integrated_model.py</b>, test stubs, doc structure. "
                    "Composer in Cursor; no separate paid LLM API for graded runs.",
                    "After edits: <b>verify_product1.py</b> + full <b>unittest</b>. Compared logic to "
                    "<b>DATA_DICTIONARY.md</b>. Fixed conflicting fields → <b>uncertain</b>.",
                ),
                (
                    "Python 3.10+<br/>(stdlib)",
                    "Loader, <b>experiment.py</b>, verify gate, 39 tests, dry-run outputs.",
                    "<b>PRODUCT 1 PASS</b> on pack data. Baseline <b>13</b> vs rules <b>5</b> in "
                    "<b>test_pack_snapshot_baseline_thirteen_rules_five</b>.",
                ),
                (
                    "Manual analysis",
                    "Deduped <b>event_id</b>; counts for <b>DECISION.md</b>.",
                    "Cross-checked CSVs and tests; rejected owner 8 h/week as unmeasured.",
                ),
                (
                    "Web / vendor docs",
                    "OneDrive/Dropbox file-request; Microsoft Learn share-files; Jotform (limited).",
                    "Recorded in <b>SOURCES.md</b> with dates, claims, limits.",
                ),
            ],
        )
    )

    story.append(Paragraph("4. AI vs my responsibility", h1))
    story.append(
        table2(
            ["Role", "Responsibility"],
            [
                ("AI (Composer)", "Boilerplate code, test skeletons, first-pass documentation."),
                (
                    "Me (applicant)",
                    "Rule semantics, evidence numbers, Product 1 scope, pass/fail gate, SOURCES claims.",
                ),
                (
                    "Reject rule",
                    "If verify or tests fail → I fix or revert; I do not accept failing AI output.",
                ),
            ],
        )
    )

    story.append(Paragraph("5. What I did not use", h1))
    story.append(
        table2(
            ["Category", "Reason"],
            [
                ("Paid LLM API keys", "Track B allows free tools; graded proof uses stdlib + local verify."),
                ("Deployment / hosting", "Out of scope; dry-run only."),
                ("Live email / SMS / WhatsApp", "Not required; simulated in trace/JSON only."),
                ("Editing Mystri data/ for grades", "Verify assumes original pack CSVs."),
            ],
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("6. Concrete example (issue I caught)", h1))
    story.append(
        table2(
            ["Step", "What happened"],
            [
                ("Problem", "Composer produced an <b>invalid dataclass update</b> in queue-related code."),
                ("Signal", "<b>Unit tests failed</b> — not a cosmetic warning."),
                ("My decision", "I <b>rejected</b> the assistant’s version."),
                ("Fix", "Rewrote using <b>dataclasses.replace</b>."),
                ("Verification", "Full unittest, then verify → <b>PRODUCT 1 PASS</b>."),
                ("Lesson", "AI output is provisional until verify + tests pass on pack data."),
            ],
        )
    )

    story.append(Paragraph("7. How this links to my submission", h1))
    story.append(
        table2(
            ["Artifact", "Role"],
            [
                ("DECISION.md", "~617 words (excl. tables); problem, claim, alternatives, counterargument."),
                ("HANDOVER.md", "Run commands, evidence table, tool judgment."),
                ("SOURCES.md", "External URLs + how I used each source."),
                ("product1/verify_product1.py", "Single reviewer gate → PRODUCT 1 PASS."),
            ],
        )
    )

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "<b>Repository:</b> github.com/santheesh15/.-mystri-assessment · "
            "<b>Branch:</b> cursor/track-b-submission-edb7 · "
            "<b>Markdown source:</b> track-b/docs/TOOL_USE_SUMMARY.md",
            meta,
        )
    )

    doc.build(story)
    return OUT


if __name__ == "__main__":
    p = build_pdf()
    print(f"Wrote {p} ({p.stat().st_size} bytes)")
