from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"


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


        # ---- Detect project name ----
        if not name_found:
            if lower.startswith("name:") or lower.startswith("project:"):
                name = line.split(":",1)[1].strip()
            else:
                name = line
            name_found = True
            continue


        # ---- Detect difficulty ----
        if "difficulty" in lower:
            difficulty = line.split(":",1)[-1].strip()
            continue


        # ---- Detect build time ----
        if "build time" in lower:
            build_time = line.split(":",1)[-1].strip()
            continue


        # ---- Detect sections ----
        if "tech stack" in lower or "technologies" in lower or "⚙" in line:
            mode = "stack"
            continue

        if "features" in lower or "⭐" in line:
            mode = "features"
            continue

        if "steps" in lower or "implementation" in lower or "📋" in line:
            mode = "steps"
            continue


        clean = line.lstrip("-•* ").strip()


        # ---- Fill sections ----
        if mode == "stack":
            stack.append(clean)

        elif mode == "features":
            features.append(clean)

        elif mode == "steps":
            if line[0].isdigit():
                step = line.split(".",1)[-1].strip()
                steps.append(step)


    # ---- fallback values ----
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
Generate ONE UNIQUE software project idea.

Skill: {skill}
Difficulty: {level}

IMPORTANT RULES:
- ALWAYS include a project name
- The FIRST line MUST be the project name
- NEVER write "AI Project Idea"

Return format EXACTLY like this:

Name: Creative Project Name

DIFFICULTY:
Beginner / Intermediate / Advanced

BUILD TIME:
Example: 3-5 hours

TECH STACK:
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

            while len(projects) < 3:

                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.9
                        }
                    },
                    timeout=120
                )

                data = response.json()
                text = data.get("response", "")

                project = parse_project(text)

                if project and project["name"] not in names_seen:
                    projects.append(project)
                    names_seen.add(project["name"])

        except Exception as e:
            print("ERROR:", e)

    return render_template("index.html", projects=projects)


# -------- RUN SERVER --------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")