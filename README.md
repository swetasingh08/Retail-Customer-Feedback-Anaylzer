# Retail-Customer-Feedback-Anaylzer

![GitHub stars](https://img.shields.io/github/stars/swetasingh08/Retail-Customer-Feedback-Anaylzer?style=for-the-badge&logo=github) ![GitHub forks](https://img.shields.io/github/forks/swetasingh08/Retail-Customer-Feedback-Anaylzer?style=for-the-badge&logo=github) ![GitHub issues](https://img.shields.io/github/issues/swetasingh08/Retail-Customer-Feedback-Anaylzer?style=for-the-badge&logo=github) ![Last commit](https://img.shields.io/github/last-commit/swetasingh08/Retail-Customer-Feedback-Anaylzer?style=for-the-badge&logo=github)

## 📑 Table of Contents

- [Description](#description)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Key Dependencies](#key-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributors](#contributors)
- [Contributing](#contributing)

## 📝 Description

A web-based application that collects retail customer reviews, performs NLP-based sentiment analysis, stores the feedback in MySQL, and provides analytics to understand customer satisfaction and product-category performance.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Notable libraries:** NumPy, Pandas

## ⚡ Quick Start

```bash

# 1. Clone the repository
git clone https://github.com/swetasingh08/Retail-Customer-Feedback-Anaylzer.git

# 2. Create & activate a virtualenv
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 📦 Key Dependencies

```
streamlit: latest
pandas: latest
numpy: latest
scikit-learn: latest
nltk: latest
mysql-connector-python: latest
plotly: latest
joblib: latest
```

## 📁 Project Structure

```
.
├── app.py
├── assets
│   └── logo.png
├── data
│   ├── feedback.csv
│   └── feedback_preprocessed.csv
├── database
│   ├── db.py
│   ├── import_feedback.py
│   └── schema.sql
├── nlp
│   ├── predict.py
│   ├── preprocess.py
│   └── train_model.py
├── notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_text_preprocessing.ipynb
│   └── 03_sentiment_model.ipynb
├── pages
│   ├── all_feedback.py
│   ├── analytics.py
│   ├── dashboard.py
│   ├── login.py
│   ├── products.py
│   └── submit_feedback.py
├── requirements.txt
└── utils
    ├── data.py
    ├── insights.py
    ├── queries.py
    └── ui.py
```

## 🛠️ Development Setup

### Python
1. Install Python (v3.10+ recommended)
2. `python -m venv venv && source venv/bin/activate`  (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`

## 👥 Contributors

Thanks to everyone who has contributed to this project:

<p align="left">
<a href="https://github.com/swetasingh08" title="swetasingh08"><img src="https://avatars.githubusercontent.com/u/286684407?v=4&s=64" width="64" height="64" alt="swetasingh08" style="border-radius:50%" /></a>
</p>

[See the full list of contributors →](https://github.com/swetasingh08/Retail-Customer-Feedback-Anaylzer/graphs/contributors)

## 👥 Contributing

Contributions are welcome! Here's the standard flow:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/swetasingh08/Retail-Customer-Feedback-Anaylzer.git`
3. **Branch**: `git checkout -b feature/your-feature`
4. **Commit**: `git commit -m 'feat: add some feature'`
5. **Push**: `git push origin feature/your-feature`
6. **Open** a pull request

Please follow the existing code style and include tests for new behavior where applicable.

</div>
