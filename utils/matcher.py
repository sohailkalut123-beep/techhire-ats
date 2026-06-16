import re
skills_list=[
    "html",
    "css",
    "javascript",
    "python",
    "flask",
    "sql",
    "react",
    "java"
]
def extract_skills(resume_text):
    matched_skills=[]
    resume_text = resume_text.lower()
    for skill in skills_list:
        if skill in resume_text:
            matched_skills.append(skill)
    return matched_skills

def extract_degree(resume_text):
    resume_text=resume_text.lower()
    degrees = [
        "b.tech",
        "btech",
        "mca",
        "bca",
        "be"
    ]
    for degree in degrees:
        if degree in resume_text:
            return degree
    return "Not Found"

def detect_domain(skills):
    skills_lower=[
        skill.lower()
        for skill in skills
    ]
    if(
        "html"in skills_lower or
        "css" in skills_lower or
        "javasvript" in skills_lower
    ):
        return "Frontend"
    elif(
        "python" in skills_lower or
        "fllask" in skills_lower or
        "django" in skills_lower
    ):
        return "Backend"
    elif(
        "machine learning" in skills_lower or
        "pandas" in skills_lower 
    ):
        return "Data science"
    else:
        return "Unknown"
def calculate_ats_score(
        resume_skills,
        jd_skills
):
    if len(jd_skills)==0:
        return 0
    matched_count=0
    for skill in jd_skills:
        if skill in resume_skills:
            matched_count+=1
    score=(
        matched_count/
        len(jd_skills)
        )*100
    return round(score,2)
def extract_name(resume_text):
    lines=resume_text.split("\n")
    for line in lines:
        if line.strip()!="":
            return line.strip()
    return "Not Found"


def extract_phone(resume_text):
    phone_pattern=r'\d{10}'
    match=re.search(phone_pattern,resume_text)
    if match:
        return match.group()
    return "Not Found"

def extract_email(resume_text):
    email_pattern=r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match=re.search(email_pattern,resume_text)
    if match:
        return match.group()
    return "Not Found"