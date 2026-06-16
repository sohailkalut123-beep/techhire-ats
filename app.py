from flask import Flask,render_template,request,send_file,redirect,url_for,session
import sqlite3
from utils.parser import extract_text_from_pdf
import os 
from openpyxl import Workbook
from openpyxl.styles import Font
from utils.matcher import (
    extract_skills,
    extract_degree,
    detect_domain,
    calculate_ats_score,
    extract_name,
    extract_phone,
    extract_email
    )
app=Flask(__name__)
app.secret_key="ats_secret_key"
all_candidates=[]

@app.route('/')
def home():
    if "user" not in session:
        return redirect (url_for("login"))
    return render_template('index.html',)
@app.route('/upload',methods=['POST'])
def upload_files():
    global all_candidates
    all_candidates.clear()
    uploaded_files = request.files.getlist("resumes")
    job_description=request.form["job_description"]
    jd_skills=extract_skills(job_description)
    print(jd_skills)
    print(job_description)
    for file in uploaded_files:
        if file.filename:
            file_path = os.path.join("uploads",file.filename)
            file.save(file_path)
            resume_text=extract_text_from_pdf(file_path)
            print(resume_text)
            name=extract_name(resume_text)
            print("Name:",name)
            phone=extract_phone(resume_text)
            print("phone:",phone)
            email=extract_email(resume_text)
            print("E-mail:",email)
            degree =extract_degree(resume_text)
            print("Degree:",degree)
            matched_skills = extract_skills(resume_text)
            print("Matched Skills",matched_skills)
            matched_jd_skills=[]
            for skill in jd_skills:
                if skill in matched_skills:
                    matched_jd_skills.append(skill)
            print("Matched 3D Skills",matched_jd_skills)
            domain=detect_domain(matched_skills)
            print("Domain:",domain)
            ats_score=calculate_ats_score(matched_skills,jd_skills)
            print("ATS Score:",ats_score)
            if ats_score>=60:
                status="Shortlisted"
            else:
                status="Rejected"
            conn=sqlite3.connect("ats.db")
            cursor=conn.cursor()
            cursor.execute(
                """
INSERT INTO candidates(
name,
phone,
email,
degree,
domain,
skills,
score,
status
)
VALUES(?,?,?,?,?,?,?,?)
""",
(
    name,
    phone,
    email,
    degree,
    domain,
    ",".join(matched_skills),
    ats_score,
    status
)
)
            candidate_id=cursor.lastrowid

            candidate_data={
                "id":candidate_id,
                "name":name,
                "phone":phone,
                "email":email,
                "degree":degree,
                "domain":domain,
                "skills":",".join(matched_skills),
                "matched_jd_skills":",".join(matched_jd_skills),
                "score":ats_score,
                "status":status
                }
            all_candidates.append(candidate_data)
            conn.commit()
            conn.close()
    all_candidates.sort(
        key=lambda x:x["score"],
        reverse=True
        )
    total_candidates=len(all_candidates)
    shortlisted_count=len([
        c for c in all_candidates
        if c["status"]=="Shortlisted"
    ])
    rejected_count=len([
        c for c in all_candidates
        if c["status"]=="Rejected"
    ])
    return render_template(
        "result.html",
        candidates=all_candidates,
        total_candidates=total_candidates,
        shortlisted_count=shortlisted_count,
        rejected_count=rejected_count
)
@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("ats.db")
        cursor=conn.cursor()

        cursor.execute(
            """
            SELECT * FROM companies
            WHERE email=? AND password=?
            """,
            (email,password)
        )

        user=cursor.fetchone()

        conn.close()

        if user:
            session["user"]=email
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Email Or Password"
        )

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))
@app.route('/download')
def download_excel():
    workbook=Workbook()
    sheet = workbook.active
    sheet.title="ATS Report"
    headings=[
            "Name",
            "Phone",
            "Email",
            "Degree",
            "Domain",
            "Skills",
            "ATS Score",
            "Status"
        ]
    sheet.append(headings)
    for cell in sheet[1]:
        cell.font=Font(bold=True)
    for candidate in all_candidates:
        sheet.append([

                candidate["name"],
                candidate["phone"],
                candidate["email"],
                candidate["degree"],
                candidate["domain"],
                candidate["skills"],
                candidate["score"],
                candidate["status"],
                ])
        row_num = sheet.max_row
        status_cell = sheet[f"H{row_num}"]

        if candidate["status"] == "Shortlisted":
            status_cell.font = Font(
                bold=True,
                color="008000"
            )
        else:
            status_cell.font = Font(
                bold=True,
                color="FF0000"
            )
    sheet.column_dimensions["A"].width = 25
    sheet.column_dimensions["B"].width = 18
    sheet.column_dimensions["C"].width = 30
    sheet.column_dimensions["D"].width = 18
    sheet.column_dimensions["E"].width = 18
    sheet.column_dimensions["F"].width = 40
    sheet.column_dimensions["G"].width = 15
    sheet.column_dimensions["H"].width = 18
    excel_path = "ATS_Report.xlsx"
    workbook.save(excel_path)
    return send_file(
        excel_path,
        as_attachment=True
    )
if __name__ == '__main__':
    app.run(debug=True)