<h1 align="center">﷽</h1>

# InstaClone

A full-stack Instagram-like application built using **FastAPI**, **MongoDB**, and **Next.js**.
Designed with modularity, clarity, and scalability in mind.

---

## Getting Started

### 1. Clone the Repository
 
```bash
git clone https://github.com/hellmakima/instagram.git
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r instagram/backend/devdocs/requirements.txt
```

or
install from [pips.txt](https://github.com/hellmakima/instagram/blob/main/devdocs/pips.txt) one by one.

### 4. Run the Backend Server

```bash
(venv) ~/instagram/backend/gate$ uvicorn main:app --reload --port 5000
(venv) ~/instagram/backend/auth-server$ uvicorn app.main:app --reload --port 5001
(venv) ~/instagram/backend/resource-server$ uvicorn app.main:app --reload --port 5002
```

Each server has its swagger docs at `http://localhost:5000/docs`.

### 5. Setup and Run Frontend

```bash
~/instagram/frontend$ npm i && npm run dev
```

---

## References

- [Akamai Developer on YouTube](https://www.youtube.com/embed/5GxQ1rLTwaU)
- [Udemy - REST APIs with Flask and Python (2025)](https://www.udemy.com/course/rest-api-flask-and-python/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [CSRF Protection](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.md#token-based-mitigation)
  - [python package](https://pypi.org/project/fastapi-csrf-protect/) python package

---

## Contributors & Tools

- [Supermaven VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Supermaven.supermaven) - Massive shoutout to for unlimited free fancy auto-completions.
- [Gemini](https://gemini.google.com/app?hl=en-IN) - Great teacher after some tweaking.
- [ChatGPT](https://chatgpt.com/?temporary-chat=true) - For any small tasks and questions.

---

## Author

Developed by [@hellmakima](https://github.com/hellmakima)

> "If you find a bug, it's either a feature or a reminder that we're always learning."

---

Pull requests, suggestions, and collaborations are welcome.
