from flask import Flask,render_template, request
from google import genai
from pdf_reader import get_resume_text
import os

app=Flask(__name__)
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
@app.route("/",methods=["GET","POST"])
def home():
    result=""
    if request.method=="POST":
        uploaded_file=request.files["resume"]
        file_path=f"uploads/{uploaded_file.filename}"
        uploaded_file.save(file_path)
        resume_text = get_resume_text(file_path)
        prompt=f"""
        You are an expert recruiter.

        Analyze this resume.

        Return:

        1. Skills
        2. Missing Skills
        3. ATS Score out of 100
        4. Suggestions

        Resume:
        {resume_text}
        """
        response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        result=response.text
        
    return render_template("index.html",result=result)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000)

