import spacy
import pdfplumber
import re
import requests
import json


nlp = spacy.load("skill_ner_model")


def load_role_skills(file_path):
    try:
        with open(file_path, "r") as file:
            role_skills = json.load(file)
        return role_skills
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return {}


ROLE_SKILLS_FILE = "role_skills.json"


role_skills = load_role_skills(ROLE_SKILLS_FILE)

if not role_skills:
    print("Role skills data could not be loaded. Exiting the program.")
    exit(1)


ADZUNA_APP_ID = "03a5f8f0"
ADZUNA_API_KEY = "a2d74aac6c5e27d89a8dbe7dac582997"
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs"


def fetch_jobs_from_adzuna(role, location="in", results_per_page=5):
    role = role.replace("_", " ")
    endpoint = f"{ADZUNA_API_URL}/{location}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": results_per_page,
        "what": role,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        jobs = response.json().get("results", [])
        return jobs
    else:
        print(f"Failed to fetch jobs from Adzuna: {response.status_code}")
        return []


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\W+", " ", text)
    text = re.sub(r"\d+", "", text)
    return text


def extract_user_skills(resume_text):

    doc = nlp(resume_text)
    extracted_skills = set(
        ent.text.lower() for ent in doc.ents if ent.label_ == "SKILL"
    )
    return extracted_skills


def identify_skill_gap(extracted_skills, role):

    required_skills = set(role_skills.get(role, []))

    missing_skills = required_skills - extracted_skills
    return missing_skills


def recommend_roles(extracted_skills):
    role_recommendations = {}
    for role, skills in role_skills.items():

        matching_skills = extracted_skills.intersection(skills)
        if skills:
            match_percentage = (len(matching_skills) / len(skills)) * 100
        else:
            match_percentage = 0
        role_recommendations[role] = match_percentage

    sorted_recommendations = sorted(
        role_recommendations.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_recommendations


def main(pdf_path, target_role):
    resume_text = extract_text_from_pdf(pdf_path)
    cleaned_resume_text = clean_text(resume_text)

    user_skills = extract_user_skills(cleaned_resume_text)
    missing_skills = identify_skill_gap(user_skills, target_role)

    print("\n📝  Resume Analysis ")
    print(f"🔍  Extracted Skills from Resume:  {', '.join(sorted(user_skills))}")

    required_skills = role_skills.get(target_role, [])
    print(f"\n🛠️  Skills Required for the Role '{target_role}': ")
    print(", ".join(sorted(required_skills)))

    if missing_skills:
        print(f"\n⚠️  Missing Skills for '{target_role}': ")
        print(", ".join(sorted(missing_skills)))
        print(
            f"\n📈  Recommendation:  To improve your chances, consider working on the following skills:\n➡️  {', '.join(sorted(missing_skills))}"
        )
    else:
        print(f"\n✅ You have all the necessary skills for the role '{target_role}'!")

    print("\n🔍  Job Recommendations Based on Your Current Skill Set: ")
    recommendations = recommend_roles(user_skills)
    for role, match in recommendations:
        if match > 0:
            print(f"• {role.replace('_', ' ').title()}: {match:.2f}% match")

    print(f"\n🌐  Fetching Job Listings for '{target_role}' from Adzuna... ")
    job_listings = fetch_jobs_from_adzuna(target_role)

    if job_listings:
        print(f"\n📝  Found {len(job_listings)} Job Listings for '{target_role}': \n")
        for job in job_listings:
            print(
                f"📌  {job.get('title')}  at  {job.get('company', {}).get('display_name')} "
            )
            print(f"  📍  Location: {job.get('location', {}).get('display_name')}")
            # salary_min = job.get("salary_min")
            # salary_max = job.get("salary_max")
            # salary_info = (
            #     f"{salary_min} - {salary_max}"
            #     if salary_min and salary_max
            #     else "Not specified"
            # )
            # print(f"  💵  Salary:  {salary_info}")
            print(f"  🔗  URL:  {job.get('redirect_url')}\n")
    else:
        print(f"\n❌ No job listings found for '{target_role}'.")


if __name__ == "__main__":

    # pdf_path = "data\\data\\ENGINEERING\\50328713.pdf"
    # pdf_path = "data\\data\\ENGINEERING\\54227873.pdf"
    pdf_path = "test_data\data\Jake_s_Resume (7).pdf"


    # print("Enter Target Role: ")
    target_role = input("Enter Target Role: ")

    main(pdf_path, target_role)
