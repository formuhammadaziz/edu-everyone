# EduEveryone — IELTS Practice Platform

A full-featured IELTS preparation platform built with Django. Practice all four IELTS sections with auto-grading, AI-powered essay feedback, and reading articles.

## Features

- **Listening Tests** — Full 40-question practice tests with auto-grading and band score calculation
- **Reading Tests** — 3-passage academic reading tests with T/F/NG, MCQ, matching, and fill-in-the-blank questions
- **Writing Tests** — Task 1 & Task 2 with word counter and AI-powered essay checking via Gemini API
- **Speaking** — Coming soon
- **AI Assistant** — Chat with an IELTS tutor powered by Google Gemini API
- **Articles** — Read real-world articles to build reading skills
- **Performance Dashboard** — Track band scores, view trends, and monitor progress
- **User Profiles** — Set target band scores and exam dates

## Setup

### 1. Clone and install

```bash
git clone <repo-url>
cd BDI
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key-here
```

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Run migrations and start

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

## Project Structure

```
EduEveryone/
├── accounts/          # User auth, registration, profile
├── dashboard/         # Performance dashboard
├── exams/             # Core app — tests, articles, AI
│   └── views.py       # All exam views + Gemini API proxy
├── results/           # Exam results and scoring
├── ielts_platform/    # Django settings and root URLs
├── static/css/        # Global styles (style.css, exam.css)
├── templates/
│   ├── base.html      # Sidebar layout
│   ├── exam_base.html # Exam-specific layout
│   ├── accounts/      # Login, register, profile
│   ├── dashboard/     # Performance page
│   ├── exams/
│   │   ├── listening/ # Listening test list + practice
│   │   ├── reading/   # Reading test list + practice
│   │   ├── writing/   # Writing test list + practice
│   │   ├── speaking/  # Speaking (coming soon)
│   │   ├── articles/  # Article list + detail
│   │   └── ai/        # AI Assistant chat
│   └── results/       # Results list + detail
├── .env               # Environment variables (not in git)
├── .env.example       # Template for .env
├── requirements.txt
└── manage.py
```

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No (default: True) |
| `GEMINI_API_KEY` | Google Gemini API key for AI features | No (AI features disabled without it) |

## Tech Stack

- **Backend:** Django
- **Frontend:** Bootstrap 5, Font Awesome 6, Chart.js
- **AI:** Google Gemini API (gemini-2.0-flash)
- **Database:** SQLite (default)
- **Font:** Inter (Google Fonts)
