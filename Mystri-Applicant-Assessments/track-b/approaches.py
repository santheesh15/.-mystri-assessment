"""Blend out-of-box ideas with proven patterns (buy + build + process)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ApproachScore:
    name: str
    idea: str
    feasibility: int  # 1-5
    uniqueness: int  # 1-5
    fit_daybreak: int  # 1-5
    incorporated_as: str


APPROACH_CATALOG = (
    ApproachScore(
        'Spreadsheet + shared inbox (status quo)',
        'Coordinator list; no automation',
        5,
        1,
        4,
        'Baseline comparison in experiment.py',
    ),
    ApproachScore(
        'OneDrive / Dropbox file request (buy)',
        'Upload link reduces “how do I send photo?” friction',
        5,
        2,
        4,
        'Link snippet appended to AI draft emails in hybrid model',
    ),
    ApproachScore(
        'Jotform Approvals (buy)',
        'Quote approval workflow',
        4,
        2,
        3,
        'Compared in DECISION.md; not primary for missing-photo chase',
    ),
    ApproachScore(
        'Rules + tiered technicians (build)',
        'Skill hierarchy + load balancing',
        5,
        3,
        5,
        'team_workboard.py',
    ),
    ApproachScore(
        'Human-in-loop AI assist (build/buy API)',
        'Drafts and inbox labels only',
        4,
        3,
        5,
        'ai_assist.py',
    ),
    ApproachScore(
        'Three-speed lanes (out-of-box process)',
        'Express / Standard / Park instead of one list',
        5,
        4,
        5,
        'lane_model.classify_case_lane',
    ),
    ApproachScore(
        'Departure-board priority (out-of-box UX)',
        'Sort open work by wait + value like an airport board',
        5,
        4,
        4,
        'lane_model.prioritized_board',
    ),
    ApproachScore(
        'Rotating duty lead (out-of-box ops)',
        'T1 lead role rotates weekly so one person is not permanent bottleneck',
        5,
        4,
        4,
        'lane_model.duty_lead_for_snapshot',
    ),
    ApproachScore(
        '15-minute daily triage huddle (process)',
        'Coordinator + duty lead review uncertain queue',
        5,
        2,
        5,
        'OPERATING_REPORT.md ritual section',
    ),
)


def hybrid_incorporation_summary() -> list[dict]:
    """What we adopted from existing vs invented."""
    return [
        {
            'layer': 'Keep (existing shop habit)',
            'items': ['Shared email inbox', 'Spreadsheet export', 'Saved reply templates'],
        },
        {
            'layer': 'Buy (lightweight)',
            'items': ['File-request link in reminder (OneDrive/Dropbox pattern)', 'Optional capped LLM API'],
        },
        {
            'layer': 'Build (our prototype)',
            'items': ['Rules engine', 'Tiered technician board', 'AI draft assist (mock)'],
        },
        {
            'layer': 'Out-of-box process',
            'items': ['Three-speed lanes', 'Departure-board sort', 'Weekly rotating duty lead', 'Daily 15-min huddle'],
        },
    ]


def rank_approaches_for_daybreak() -> list[dict]:
    ranked = sorted(
        APPROACH_CATALOG,
        key=lambda a: (a.fit_daybreak + a.uniqueness + a.feasibility, a.fit_daybreak),
        reverse=True,
    )
    return [
        {
            'name': a.name,
            'idea': a.idea,
            'scores': {
                'feasibility': a.feasibility,
                'uniqueness': a.uniqueness,
                'fit': a.fit_daybreak,
            },
            'incorporated_as': a.incorporated_as,
        }
        for a in ranked
    ]
