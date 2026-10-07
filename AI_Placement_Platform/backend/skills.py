skills_db = [

    "Python",
    "Java",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "FastAPI",
    "React",
    "Docker",
    "AWS"

]

def extract_skills(text):

    found = []

    text_lower = text.lower()

    for skill in skills_db:

        if skill.lower() in text_lower:

            found.append(skill)

    return list(set(found))