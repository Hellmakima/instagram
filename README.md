<div style="display: flex; justify-content: center; font-size: 40px;">﷽</div>

---

# InstaClone

A full-stack Instagram-like application built using **FastAPI**, **MongoDB**, and **Next.js**.
Designed with modularity, clarity, and scalability in mind.

_This project was initially scaffolded using GPT. While care has been taken to ensure code quality, some issues may exist. Contributions and corrections are welcome._

---

## Tech Stack

| Layer    | Technology | Description                                       |
| -------- | ---------- | ------------------------------------------------- |
| Frontend | Next.js    | A modern React framework for performant UIs       |
| Backend  | FastAPI    | A fast, Pythonic API framework with type hints    |
| Database | MongoDB    | NoSQL database for flexible, document storage     |
| Auth     | TBD        | Planned: Local auth with JWT and password hashing |

---

## Project Status

- **Overall:** Under development
- **Frontend:** Basic static pages for prototyping
- **Backend:** Initial FastAPI structure implemented
- **Database:** MongoDB connected; initial schema to be refined

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hellmakima/instaclone.git
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Run the Backend Server

```bash
uvicorn app.main:app --reload --port 5000
```

Documentation: [http://localhost:5000/docs#/](http://localhost:5000/docs#/)

### 5. Setup and Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Access: [http://localhost:3000](http://localhost:3000)

---

## Authentication (Planned)

- **Local Auth:** Secure login with bcrypt-hashed passwords
- **JWT Tokens:** Stateless authentication via access tokens

**Current Status:** Authentication not yet implemented

---

## References

- [Akamai Developer on YouTube](https://www.youtube.com/embed/5GxQ1rLTwaU)
- [Udemy - REST APIs with Flask and Python (2025)](https://www.udemy.com/course/rest-api-flask-and-python/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

---

## Contributors & Tools

- [Supermaven VS Code Extension](https://marketplace.visualstudio.com/items?itemName=Supermaven.supermaven)
- [ChatGPT](https://chatgpt.com/?temporary-chat=true)
- [Gemini](https://gemini.google.com/app?hl=en-IN)
- [DeepSeek](https://chat.deepseek.com)

---

## License

**MIT License**
Feel free to use, modify, and distribute. No liability assumed by the author.

---

## Author

Developed by [@hellmakima](https://github.com/hellmakima)

> “If you find a bug, it's either a feature or a reminder that we're always learning.”

---

Pull requests, suggestions, and collaborations are welcome.
