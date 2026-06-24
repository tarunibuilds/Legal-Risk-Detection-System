import pandas as pd
import random
import os

# Ensure correct path
base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
data_path = os.path.join(base_dir, "data")

# Create folder if not exists
os.makedirs(data_path, exist_ok=True)

file_path = os.path.join(data_path, "legal_dataset_500.csv")

# Categories and templates
data_templates = {
    "Payment": [
        "The client shall pay invoices within {n} days",
        "Invoices must be cleared within {n} days",
        "All dues must be settled within {n} days",
    ],
    "Termination": [
        "The agreement may be terminated with {n} days notice",
        "Either party can terminate the contract without notice",
    ],
    "Confidentiality": [
        "All data must remain confidential",
        "The party shall not disclose confidential information",
    ],
    "Liability": [
        "The company is not liable for indirect damages",
        "The vendor shall indemnify the client",
    ],
    "Penalty": [
        "Delay will result in penalty charges",
        "Penalty of {n}% will be applied",
    ],
    "Administrative": [
        "The agreement shall remain valid for one year",
        "The vendor shall follow all guidelines",
    ],
    "Jurisdiction": [
        "This agreement is governed by Indian law",
        "All disputes shall be handled in court",
    ],
    "Security_Deposit": [
        "Security deposit shall be refunded after inspection",
        "Deposit must be paid before service begins",
    ]
}

risk_map = {
    "Payment": ["Low", "Medium"],
    "Termination": ["Medium", "High"],
    "Confidentiality": ["High"],
    "Liability": ["Medium", "High"],
    "Penalty": ["Medium", "High"],
    "Administrative": ["Low"],
    "Jurisdiction": ["Low"],
    "Security_Deposit": ["Medium"]
}

dataset = []

for _ in range(800):
    category = random.choice(list(data_templates.keys()))
    clause = random.choice(data_templates[category]).replace("{n}", str(random.randint(10, 90)))
    risk = random.choice(risk_map[category])
    dataset.append([clause, category, risk])

df = pd.DataFrame(dataset, columns=["Clause", "Category", "Risk_Level"])

# SAVE FILE
df.to_csv(file_path, index=False)

print(f"✅ Dataset saved at: {file_path}")