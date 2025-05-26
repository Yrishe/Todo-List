# 📝 Flask To-Do List App

A simple, full-stack to-do list web app built with **Flask**, **SQLite**, and **HTML + JavaScript**. Tasks support:

- ✅ Create, read, update, delete (CRUD)
- 🗓️ Due date and time
- 🏷️ Tags
- ⭐ Priority levels
- 🔍 Filter by done/undone
- 📄 Pagination
- 💄 Clean Bootstrap UI

This project is ideal for Flask beginners, web dev learners, or anyone needing a simple, well-structured CRUD app.

---

## 🚀 Features

- RESTful API with Flask
- SQLite database with SQLAlchemy ORM
- Front-end using HTML, Bootstrap, and JavaScript
- Icons via Bootstrap Icons
- Pagination and filters
- Docker-ready

---

## 🧱 Project Structure

todo-flask-api/


---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/flask-todo-app.git
cd flask-todo-app

### 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the app

python run.py

# Then open your browser at: http://localhost:5000/

### 5. Run with Docker

# Build the image

docker build -t flask-todo-app .

# Run the container:

docker run -p 5000:5000 flask-todo-app

### 4. Unit testing is configured for the Flask API using pytest, simply run tests:

python -m pytest
