"""Transparent cost / time structure for reviewer (scenario assumptions labeled)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostLine:
    category: str
    assumption: str
    inr_per_month: float
    minutes_per_week: float


def build_cost_structure(scenario: dict, metrics: dict) -> dict:
    budget = float(scenario.get('monthly_tool_budget_inr', 1500))
    coord_hourly = 400.0  # scenario assumption — not verified
    tech_hourly = 350.0

    solo = metrics['baseline_all_work_on_coordinator']
    split_coord = metrics['coordinator_tasks_after_split']
    tech_tasks = len(metrics.get('technician_tasks', []))

    # Optimistic but labeled savings from rules + split + AI assist on drafts/triage
    minutes_saved_rules = max(0, (solo - split_coord) * 4)  # 4 min per item not wrongly chased
    minutes_saved_parallel = tech_tasks * 6  # tech prep saves coordinator 6 min/case (assumption)
    minutes_saved_ai = metrics.get('ai_draft_count', 0) * 3  # 3 min per AI-drafted email edit vs write

    gross_saved = minutes_saved_rules + minutes_saved_parallel + minutes_saved_ai
    review_overhead = metrics.get('uncertain_count', 0) * 5 + split_coord * 1
    net_minutes = gross_saved - review_overhead

    tool_lines = [
        CostLine(
            'Rules workboard (self-hosted script)',
            'Python stdlib; runs on Windows/macOS/Linux',
            0,
            0,
        ),
        CostLine(
            'Lightweight LLM API (optional pilot)',
            f'Capped at ≤{budget * 0.6:.0f} INR/month of {budget:.0f} budget',
            budget * 0.6,
            -minutes_saved_ai,
        ),
        CostLine(
            'File-request link (optional)',
            'OneDrive/Dropbox free tier for uploads only',
            0,
            0,
        ),
        CostLine(
            'Human oversight (non-negotiable)',
            'Coordinator + technician review time',
            0,
            review_overhead,
        ),
    ]

    labor_value_saved = (net_minutes / 60) * coord_hourly * 4.33 / 4  # rough monthly from weekly

    return {
        'assumptions': {
            'coordinator_hourly_inr': coord_hourly,
            'technician_hourly_inr': tech_hourly,
            'monthly_tool_budget_inr': budget,
            'note': 'Labor rates are scenario placeholders, not measured Daybreak costs.',
        },
        'workload_metrics': {
            'solo_coordinator_items': solo,
            'split_coordinator_tasks': split_coord,
            'technician_parallel_tasks': tech_tasks,
            'uncertain_rows': metrics.get('uncertain_count', 0),
        },
        'time_minutes_per_week': {
            'gross_saved': gross_saved,
            'review_overhead': review_overhead,
            'net_saved': net_minutes,
            'breakdown': {
                'rules_prevent_wrong_chase': minutes_saved_rules,
                'technician_parallel_prep': minutes_saved_parallel,
                'ai_draft_and_triage_assist': minutes_saved_ai,
            },
        },
        'inr_per_month_scenario': {
            'tool_spend_cap': sum(l.inr_per_month for l in tool_lines),
            'labor_value_equivalent_saved': round(labor_value_saved, 2),
            'net_after_tools': round(labor_value_saved - budget * 0.6, 2),
        },
        'line_items': [
            {
                'category': l.category,
                'assumption': l.assumption,
                'inr_per_month': l.inr_per_month,
                'minutes_per_week': l.minutes_per_week,
            }
            for l in tool_lines
        ],
    }
