"""売上データ(CSV)から月次ビジネスレポート(Markdown)を自動生成する。"""

import csv
from collections import defaultdict
from datetime import datetime

INPUT_FILE = "sales_data.csv"
OUTPUT_FILE = "monthly_report.md"


def load_sales(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            row["units_sold"] = int(row["units_sold"])
            row["unit_price"] = int(row["unit_price"])
            row["revenue"] = row["units_sold"] * row["unit_price"]
            rows.append(row)
        return rows


def build_report(rows: list[dict]) -> str:
    total_revenue = sum(r["revenue"] for r in rows)
    total_units = sum(r["units_sold"] for r in rows)

    revenue_by_region: dict[str, int] = defaultdict(int)
    revenue_by_product: dict[str, int] = defaultdict(int)
    units_by_product: dict[str, int] = defaultdict(int)

    for r in rows:
        revenue_by_region[r["region"]] += r["revenue"]
        revenue_by_product[r["product"]] += r["revenue"]
        units_by_product[r["product"]] += r["units_sold"]

    top_product = max(revenue_by_product, key=revenue_by_product.get)
    top_region = max(revenue_by_region, key=revenue_by_region.get)

    dates = sorted(r["date"] for r in rows)
    period = f"{dates[0]} 〜 {dates[-1]}"

    lines = []
    lines.append("# 月次売上レポート")
    lines.append("")
    lines.append(f"- 対象期間: {period}")
    lines.append(f"- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("## サマリー")
    lines.append("")
    lines.append(f"- 総売上高: {total_revenue:,} 円")
    lines.append(f"- 総販売数: {total_units:,} 個")
    lines.append(f"- 最も売上が高い製品: {top_product}（{revenue_by_product[top_product]:,} 円）")
    lines.append(f"- 最も売上が高い地域: {top_region}（{revenue_by_region[top_region]:,} 円）")
    lines.append("")
    lines.append("## 地域別売上")
    lines.append("")
    lines.append("| 地域 | 売上高 | 構成比 |")
    lines.append("|---|---|---|")
    for region, revenue in sorted(revenue_by_region.items(), key=lambda x: -x[1]):
        share = revenue / total_revenue * 100
        lines.append(f"| {region} | {revenue:,} 円 | {share:.1f}% |")
    lines.append("")
    lines.append("## 製品別売上")
    lines.append("")
    lines.append("| 製品 | 販売数 | 売上高 | 構成比 |")
    lines.append("|---|---|---|---|")
    for product, revenue in sorted(revenue_by_product.items(), key=lambda x: -x[1]):
        share = revenue / total_revenue * 100
        lines.append(f"| {product} | {units_by_product[product]:,} 個 | {revenue:,} 円 | {share:.1f}% |")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    rows = load_sales(INPUT_FILE)
    report = build_report(rows)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"レポートを {OUTPUT_FILE} に出力しました。")


if __name__ == "__main__":
    main()
