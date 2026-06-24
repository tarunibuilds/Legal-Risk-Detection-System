from src.clause_splitter import extract_clauses
from src.predict import predict_clause
from collections import Counter

def analyze_agreement(text):
    clauses = extract_clauses(text)

    high = medium = low = 0
    category_counts = Counter()
    risk_counts = Counter()

    print("\n========== AGREEMENT ANALYSIS ==========\n")

    for idx, clause in enumerate(clauses, 1):

        category, risk, rule_score, cat_conf, risk_conf, source, explanation = predict_clause(clause)

        print(f"Clause {idx}: {clause[:150]}...")
        print(f"  → Category: {category} ({cat_conf}%)")
        print(f"  → Risk Level: {risk} ({risk_conf}%)")
        print(f"  → Rule Score: {rule_score}")
        print(f"  → Risk Source: {source}")
        print(f"  → Explanation: {explanation}")
        print("-" * 60)

        category_counts[category] += 1
        risk_counts[risk] += 1

        if risk == "High":
            high += 1
        elif risk == "Medium":
            medium += 1
        else:
            low += 1

    total = len(clauses)

    if total == 0:
        print("No clauses detected")
        return

    risk_score = ((high * 2) + medium) / (total * 2) * 100
    risk_score = round(risk_score, 2)

    if risk_score >= 70:
        overall = "HIGH"
    elif risk_score >= 40:
        overall = "MEDIUM"
    else:
        overall = "LOW"

    print("\n========== AGREEMENT SUMMARY ==========")
    print(f"Total Clauses: {total}")
    print(f"High: {high}, Medium: {medium}, Low: {low}")
    print(f"Risk Score: {risk_score}%")
    print(f"Overall Risk: {overall}")
    print("\nRisk Distribution:", risk_counts)
    print("Category Distribution:", category_counts)


if __name__ == "__main__":
    sample = """
    The tenant shall pay rent on time.
    Failure to pay will result in penalty.
    The landlord may terminate without notice.
    Security deposit will be refunded.
    """

    analyze_agreement(sample)
