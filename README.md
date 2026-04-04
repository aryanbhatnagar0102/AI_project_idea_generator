# AI Project Idea Generator

A web application that generates unique software project ideas using AI based on user skill level and domain interest.

Live Demo: [https://ai-project-idea-generator.vercel.app](https://ai-project-idea-generator.vercel.app/)

---

## Overview

This application allows users to input their technical skill and preferred difficulty level, and receive structured project ideas including:

* Project name
* Difficulty level
* Estimated build time
* Recommended tech stack
* Key features
* Step-by-step implementation plan

The goal is to help developers discover meaningful and practical project ideas tailored to their experience level.

---

## Features

* AI-powered project idea generation
* Structured output for easy understanding
* Multiple unique ideas per request
* Responsive design for desktop and mobile
* Copy-to-clipboard functionality
* Regenerate ideas feature

---

## Technology Stack

* Frontend: HTML, CSS
* Backend: Python (Flask)
* AI Integration: Groq API
* Deployment: Vercel
* Version Control: GitHub

---

## Project Structure

```
AI_project_idea_generator
│
├── api/
│   └── index.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── app.py
├── wsgi.py
├── requirements.txt
└── vercel.json
```

---

## Installation and Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/AI_project_idea_generator.git
cd AI_project_idea_generator
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Configure environment variables

Set your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the application

```
python app.py
```

---

## Environment Variables

| Variable     | Description                 |
| ------------ | --------------------------- |
| GROQ_API_KEY | Groq API authentication key |

---

## Deployment

The application is deployed on Vercel using Python serverless functions.

---

## Future Enhancements

* Improved diversity in generated ideas
* Enhanced UI and user experience
* Export or share project ideas
* Advanced prompt engineering
* User customization features

---

## Acknowledgements

* Groq for providing the AI API
* Flask for backend development
* Vercel for hosting and deployment

---

## Author

Aryan Bhatnagar
