import re

def extract_clauses(text):

    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)

    raw_clauses = re.split(r'\.\s+|;\s+', text)

    clauses = []

    for clause in raw_clauses:
        clause = clause.strip()

        # Remove short junk
        if len(clause.split()) < 6:
            continue

        # Remove noise
        if any(x in clause.lower() for x in [
            "signature", "date", "name", "sample", "please put"
        ]):
            continue

        clauses.append(clause)

    return clauses