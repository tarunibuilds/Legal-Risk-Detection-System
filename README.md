# Legal Risk Detection & Clause Classification System ⚖️🧠

An NLP-powered legal agreement analysis system that automatically extracts clauses, classifies clause types, detects risk levels, and generates explainable insights using Machine Learning and rule-based NLP techniques.

The system simplifies complex legal agreements by helping users identify risky clauses related to liabilities, penalties, termination conditions, confidentiality, and payment terms.

---

## 🚀 Features

* 📄 PDF & TXT legal document support
* ✂️ Automated clause extraction
* 🧹 NLP-based text preprocessing
* 🧠 TF-IDF feature extraction with n-grams
* 🏷️ Clause classification
* ⚠️ Risk detection (High / Medium / Low)
* 🔍 Keyword-driven rule enhancement
* 💡 Explainable AI outputs
* 📊 Agreement-level risk scoring
* 🌐 Interactive Streamlit dashboard
* 🔎 Search & filter functionality

---

## 🛠️ Tech Stack

### Languages & Frameworks

* Python
* Streamlit

### NLP & Machine Learning

* TF-IDF Vectorization
* N-grams
* Clause Classification
* Risk Prediction
* Rule-based NLP

### Libraries

* Scikit-learn
* NLTK
* Pandas
* NumPy
* PDFPlumber
* Matplotlib
* Plotly

---

## 🧩 System Workflow

Legal Document → Text Extraction → Clause Segmentation → NLP Preprocessing → TF-IDF Vectorization → Clause Classification → Risk Prediction → Explainable Insights → Dashboard Visualization

---

## 📂 Project Structure

```bash id="hlxzj9"
Legal-Risk-Detection-System/
│── app.py                     # Main Streamlit application
│── legal_report.html          # Generated legal report
│── report.html                # Additional report output
│── requirements.txt           # Project dependencies
│── README.md                  # Project documentation
│── .gitignore
│── LICENSE
│
├── data/                      # Dataset files
│
├── models/                    # Trained ML models
│   ├── category_model.pkl
│   ├── risk_model.pkl
│   └── vectorizer.pkl
│
├── src/                       # Core source code
│   ├── __init__.py
│   ├── agreement_analyzer.py  # Legal agreement analysis logic
│   ├── clause_splitter.py     # Splits agreements into clauses
│   ├── generate_dataset.py    # Dataset generation script
│   ├── merge_dataset.py       # Dataset merging script
│   ├── predict.py             # Risk/category prediction logic
│   ├── preprocess.py          # Text preprocessing
│   └── train_model.py         # Model training pipeline
│
└── venv/                      # Virtual environment (not uploaded to GitHub)
```

---

## 📸 Screenshots
## Homepage
<img width="1903" height="1004" alt="homepage_Legal" src="https://github.com/user-attachments/assets/4d9f9e6d-b344-486b-9d25-759fb1edfb15" />

## Risk analysis
<img width="1919" height="882" alt="risk_analysis" src="https://github.com/user-attachments/assets/f6e0cc8c-eb60-4af7-8a2a-cae253ded6e3" />

## Risky clauses
<img width="1360" height="926" alt="risky_clauses" src="https://github.com/user-attachments/assets/68240a6a-849e-4dcf-94e9-2ea4418b0a99" />

## Dashboard
<img width="1360" height="926" alt="risky_clauses" src="https://github.com/user-attachments/assets/e5d33bb5-bc1e-4513-a9a0-75a43dd6fe48" />


## category table
<img width="1899" height="991" alt="category_table" src="https://github.com/user-attachments/assets/d5d39217-e5db-49f8-bfbd-d2826ed89e4a" />








---

## ⚙️ Installation

Clone the repository:

```bash id="sm98m5"
git clone https://github.com/your-username/Legal-Risk-Detection-System.git
cd Legal-Risk-Detection-System
```

Install dependencies:

```bash id="m89v9x"
pip install -r requirements.txt
```

Run the application:

```bash id="6qavxl"
streamlit run app.py
```

---

## 🧠 NLP Techniques Used

* Tokenization
* Text Cleaning
* Stopword Removal
* N-gram Analysis
* TF-IDF Vectorization
* Rule-based NLP
* Explainable AI

---

## 📈 Machine Learning Tasks

* Clause Classification
* Risk Prediction
* Hybrid Rule + ML Decision Making

---

## 🎯 Future Enhancements

* BERT-based legal understanding
* Multilingual legal document support
* Legal chatbot integration
* Deep learning-based semantic analysis
* Cloud deployment

---

## 👩‍💻 Author

**Taruni Middela**

AI & Machine Learning Enthusiast passionate about NLP, Information Retrieval, Explainable AI, and Generative AI systems.

---

## ⭐ Acknowledgements

Built using:

* Streamlit
* Scikit-learn
* NLTK
* PDFPlumber
* Plotly

