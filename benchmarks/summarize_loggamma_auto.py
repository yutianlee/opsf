from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from statistics import median
from typing import Any


CaseKey = tuple[str, int]
Record = dict[str, Any]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize JSON-lines output from analyze_loggamma_auto.py."
    )
    parser.add_argument("jsonl_path", help="Path to analyze_loggamma_auto.py JSONL output.")
    args = parser.parse_args()

    records = read_records(args.jsonl_path)
    print(json.dumps(summarize(records), indent=2, sort_keys=True))


def read_records(path: str) -> list[Record]:
    records: list[Record] = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL record") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            records.append(record)
    return records


def summarize(records: list[Record]) -> dict[str, Any]:
    by_case = group_by_case(records)
    certified_counts: Counter[str] = Counter()
    non_certified_counts: Counter[str] = Counter()
    auto_selected_counts: Counter[str] = Counter({"arb": 0, "stirling": 0, "stirling_shifted": 0})
    elapsed_by_method: dict[str, list[float]] = defaultdict(list)

    for record in records:
        method = str(record.get("method_requested"))
        if record.get("certified"):
            certified_counts[method] += 1
        else:
            non_certified_counts[method] += 1

        selected = record.get("auto_selected_method")
        if method == "certified_auto" and selected in auto_selected_counts:
            auto_selected_counts[str(selected)] += 1

        elapsed = record.get("elapsed_seconds")
        if isinstance(elapsed, int | float):
            elapsed_by_method[method].append(float(elapsed))

    fastest = fastest_method_by_case(by_case)
    direct_arb_comparisons = compare_certified_auto_to_arb(by_case)

    return {
        "total_records": len(records),
        "methods_seen": sorted({str(record.get("method_requested")) for record in records}),
        "x_values_seen": sorted({str(record.get("x")) for record in records}, key=x_sort_key),
        "dps_values_seen": sorted({int(record.get("dps")) for record in records}),
        "certified_counts_by_method": dict(sorted(certified_counts.items())),
        "non_certified_counts_by_method": dict(sorted(non_certified_counts.items())),
        "certified_auto_selected_method_counts": dict(sorted(auto_selected_counts.items())),
        "fastest_method_by_case": fastest,
        "cases_certified_auto_slower_than_direct_arb": direct_arb_comparisons["slower"],
        "cases_certified_auto_faster_than_direct_arb": direct_arb_comparisons["faster"],
        "cases_stirling_failed_shifted_succeeded": cases_stirling_failed_shifted_succeeded(by_case),
        "cases_direct_arb_only_certified": cases_direct_arb_only_certified(by_case),
        "elapsed_seconds_by_method": summarize_elapsed(elapsed_by_method),
    }


def group_by_case(records: list[Record]) -> dict[CaseKey, dict[str, Record]]:
    grouped: dict[CaseKey, dict[str, Record]] = defaultdict(dict)
    for record in records:
        method = str(record.get("method_requested"))
        grouped[(str(record.get("x")), int(record.get("dps")))][method] = record
    return dict(grouped)


def fastest_method_by_case(by_case: dict[CaseKey, dict[str, Record]]) -> list[dict[str, Any]]:
    fastest: list[dict[str, Any]] = []
    for key, method_records in sorted_cases(by_case):
        certified_records = [
            record
            for record in method_records.values()
            if record.get("certified") and isinstance(record.get("elapsed_seconds"), int | float)
        ]
        if not certified_records:
            continue
        winner = min(certified_records, key=lambda record: float(record["elapsed_seconds"]))
        fastest.append(
            {
                "x": key[0],
                "dps": key[1],
                "method_requested": winner.get("method_requested"),
                "result_method": winner.get("result_method"),
                "elapsed_seconds": winner.get("elapsed_seconds"),
            }
        )
    return fastest


def compare_certified_auto_to_arb(by_case: dict[CaseKey, dict[str, Record]]) -> dict[str, list[dict[str, Any]]]:
    slower: list[dict[str, Any]] = []
    faster: list[dict[str, Any]] = []
    for key, method_records in sorted_cases(by_case):
        auto = method_records.get("certified_auto")
        arb = method_records.get("arb")
        if not is_certified_timed(auto) or not is_certified_timed(arb):
            continue

        auto_elapsed = float(auto["elapsed_seconds"])
        arb_elapsed = float(arb["elapsed_seconds"])
        entry = {
            "x": key[0],
            "dps": key[1],
            "auto_selected_method": auto.get("auto_selected_method"),
            "preselected": auto.get("preselected"),
            "can_certify": auto.get("can_certify"),
            "estimated_terms_used": auto.get("estimated_terms_used"),
            "certified_auto_elapsed_seconds": auto_elapsed,
            "arb_elapsed_seconds": arb_elapsed,
            "elapsed_ratio": auto_elapsed / arb_elapsed if arb_elapsed else None,
        }
        if auto_elapsed > arb_elapsed:
            slower.append(entry)
        elif auto_elapsed < arb_elapsed:
            faster.append(entry)
    return {"slower": slower, "faster": faster}


def cases_stirling_failed_shifted_succeeded(
    by_case: dict[CaseKey, dict[str, Record]]
) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for key, method_records in sorted_cases(by_case):
        stirling = method_records.get("stirling")
        shifted = method_records.get("stirling_shifted")
        if stirling is None or shifted is None:
            continue
        if not stirling.get("certified") and shifted.get("certified"):
            cases.append(
                {
                    "x": key[0],
                    "dps": key[1],
                    "stirling_error": stirling.get("error"),
                    "shift": shifted.get("shift"),
                    "shifted_argument": shifted.get("shifted_argument"),
                    "shift_policy": shifted.get("shift_policy"),
                }
            )
    return cases


def cases_direct_arb_only_certified(by_case: dict[CaseKey, dict[str, Record]]) -> list[dict[str, Any]]:
    concrete_methods = ("arb", "stirling", "stirling_shifted")
    cases: list[dict[str, Any]] = []
    for key, method_records in sorted_cases(by_case):
        certified_concrete = [
            method for method in concrete_methods if method_records.get(method, {}).get("certified")
        ]
        if certified_concrete == ["arb"]:
            cases.append(
                {
                    "x": key[0],
                    "dps": key[1],
                    "certified_method_requests": [
                        method
                        for method, record in sorted(method_records.items())
                        if record.get("certified")
                    ],
                }
            )
    return cases


def summarize_elapsed(elapsed_by_method: dict[str, list[float]]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = {}
    for method, values in sorted(elapsed_by_method.items()):
        if not values:
            continue
        summary[method] = {
            "min": min(values),
            "median": median(values),
            "max": max(values),
        }
    return summary


def is_certified_timed(record: Record | None) -> bool:
    return bool(
        record
        and record.get("certified")
        and isinstance(record.get("elapsed_seconds"), int | float)
    )


def sorted_cases(
    by_case: dict[CaseKey, dict[str, Record]]
) -> list[tuple[CaseKey, dict[str, Record]]]:
    return sorted(by_case.items(), key=lambda item: (x_sort_key(item[0][0]), item[0][1]))


def x_sort_key(value: str) -> tuple[int, float | str]:
    try:
        return (0, float(value))
    except ValueError:
        return (1, value)


if __name__ == "__main__":
    main()
