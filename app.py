from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# -------- GROQ SETTINGS --------

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


# -------- PARSE AI RESPONSE --------

def parse_project(text):

    name = ""
    difficulty = ""
    build_time = ""
    stack = []
    features = []
    steps = []

    mode = None
    name_found = False

    for line in text.split("\n"):

        line = line.strip().replace("**","").replace("##","")

        if not line:
            continue

        lower = line.lower()

        if not name_found:
            if ":" in line:
                name = line.split(":",1)[1].strip()
            else:
                name = line
            name_found = True
            continue

        if "difficulty" in lower:
            difficulty = line.split(":",1)[-1].strip()
            continue

        if "build time" in lower:
            build_time = line.split(":",1)[-1].strip()
            continue

        if "tech stack" in lower:
            mode = "stack"
            continue

        if "features" in lower:
            mode = "features"
            continue

        if "steps" in lower:
            mode = "steps"
            continue

        clean = line.lstrip("-•* ").strip()

        if mode == "stack":
            stack.append(clean)

        elif mode == "features":
            features.append(clean)

        elif mode == "steps":
            if line[0].isdigit():
                step = line.split(".",1)[-1].strip()
                steps.append(step)

    if not name:
        name = "Untitled AI Project"

    if not difficulty:
        difficulty = "Beginner"

    if not build_time:
        build_time = "2-4 hours"

    if not stack:
        stack = ["Python"]

    if not features:
        features = ["Core functionality"]

    if not steps:
        steps = [
            "Implement core logic",
            "Add user input handling",
            "Test the application"
        ]

    return {
        "name": name,
        "difficulty": difficulty,
        "build_time": build_time,
        "stack": stack,
        "features": features,
        "steps": steps
    }


# -------- ROUTE --------

@app.route("/", methods=["GET", "POST"])
def home():

    projects = []
    names_seen = set()

    if request.method == "POST":

        skill = request.form.get("skill")
        level = request.form.get("level")

        prompt = f"""
You are an expert software architect.

Generate ONE UNIQUE and CREATIVE software project idea.

User Skill: {skill}
Difficulty Level: {level}

IMPORTANT RULES:
- The project MUST be original and unusual.
- DO NOT generate common beginner projects like:
  * To-do list
  * Calculator
  * Weather app
  * Chat app
  * Notes app
  * Blog website
  * Quiz app
- Each idea should explore a DIFFERENT domain.

Choose a RANDOM domain such as:
AI tools, developer tools, browser extensions, automation tools,
education technology, productivity tools, data visualization,
local utilities, gaming utilities, social experiments, or APIs.

Make the idea feel like something that could be a **real startup product**.

Return EXACTLY in this format:

Name: Creative Project Name

DIFFICULTY:
Beginner / Intermediate / Advanced

BUILD TIME:
Example: 3-5 hours

TECH STACK:
- tech
- tech
- tech

FEATURES:
- feature
- feature
- feature

STEPS:
1. step
2. step
3. step
4. step
"""

        try:

            for i in range(3):

                response = requests.post(
                    GROQ_URL,
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": MODEL,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.9
                    }
                )

                if response.status_code != 200:
                    print("ERROR:", response.text)
                    break

                data = response.json()

                if "choices" not in data:
                    print("API ERROR:", data)
                    continue

                text = data["choices"][0]["message"]["content"]

                project = parse_project(text)

                if project["name"] not in names_seen:
                    projects.append(project)
                    names_seen.add(project["name"])

        except Exception as e:
            print("ERROR:", e)

    return render_template("index.html", projects=projects)


# -------- RUN --------

if __name__ == "__main__":
    app.run(debug=True)