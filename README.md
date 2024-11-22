# AIES_Project
# Strategic Workforce Planning using Artificial Intelligence

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Project Setup](#project-setup)
4. [Execution Steps](#execution-steps)

## Overview
This project enhances strategic workforce planning (SWP) by utilizing AI for resume classification and skill extraction, focusing on analyzing employee resumes to predict job titles and recommend skills. It automates the identification of relevant job titles and extracts skills using Named Entity Recognition (NER). Additionally, it offers predictive analytics to suggest future skill needs based on current trends, facilitating proactive skill gap planning.

## Features
- **AI-Powered Resume Analysis**: Utilizes a pre-trained `spaCy` model for skill extraction. Classifies job titles using Random Forest, XGBoost, and spaCy models, with spaCy offering superior performance.
- **Skill Gap Identification**: Compares extracted skills to role-specific requirements and provides personalized skill recommendations for development.
- **Dashboard for HR Managers**: Enables data-driven insights for proactive workforce planning and strategic decision-making.

## Project Setup

### Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **Python Libraries**: Install required libraries, including `PyPDF2`, `pdfplumber`, `NLTK`, `spaCy`, and `scikit-learn`.
- **Optional Software**: Jupyter Notebook, PyCharm, or VS Code for development.

### Installation Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SShetty2003/AIES_Project.git
   cd AIES_Project

2. **Install Dependencies**:
   pip install PyPDF2 pdfplumber nltk spacy scikit-learn
   
3. **Download spaCy Model**:
   python -m spacy download en_core_web_sm

4. **Prepare Dataset**: Organize PDF resumes in folders, each representing a job category.

5. **Data Link**: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

### Execution Steps
1. Data Preprocessing:
Extract resume text using extract_text_from_pdf, clean it with clean_text, and identify skills through extract_user_skills. This step also identifies skill gaps with identify_skill_gap, recommends roles based on skill matches using recommend_roles, and fetches job listings through fetch_jobs_from_adzuna.

2. Training the Models:
Train Random Forest, XGBoost, and spaCy models on labeled resumes. Execute my_train_model.py to train models and evaluate their performance. This loads a pre-trained spaCy NER model (skill_ner_model) to detect skills from resumes and role-specific skills from a role_skills.json file, which must be correctly formatted to avoid errors.

3. Testing:
Execute my_test.py to perform the following: load a sample PDF resume, process it, and extract skills. It also accepts a target_role input to match extracted skills against role-specific requirements.

4. Output:
Displays extracted, required, and missing skills, and recommends suitable roles based on skill overlap. It retrieves relevant job listings from Adzuna for the target role, if available.

