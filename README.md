🗳️ Django Polling System

A Polling Application built with Django + Django REST Framework 
Supports:

🔑 Authentication – Register / Login / Logout

📊 Voting – Active polls, choices, vote history

👤 User Dashboard – See your own votes

🛠️ Admin Dashboard – Pie chart results + CSV export

✅ Role-based UI – Admins see extra tab for results

🚀 Features
👥 Users

Register & login securely

Vote on available polls

Track past votes

👨‍💼 Admins

Create/manage polls, questions, and choices (via Django Admin)

View poll results as a pie chart (Chart.js)

Export votes to CSV (poll-wise)

🏗️ Tech Stack

Backend: Django, Django REST Framework

Frontend: HTML, CSS, Chart.js

Database: SQLite (default, can switch to PostgreSQL/MySQL)

Auth: Django’s built-in User model

📂 Project Structure
polling-system/
│── polls/                   # Main Django app
│   ├── models.py            # Polls, Questions, Choices, Votes
│   ├── views.py             # Poll APIs, CSV Export
│   ├── serializers.py       # DRF Serializers
│   ├── urls.py              # App URLs
│   └── admin.py             # Django admin customization
│
│── templates/
│   └── index.html           # Frontend (tabs + UI)
│
|
│
│── manage.py
│── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/your-username/polling-system.git
cd polling-system

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run migrations
python manage.py migrate

5️⃣ Create superuser
python manage.py createsuperuser

6️⃣ Run server
python manage.py runserver


Visit 👉 http://127.0.0.1:8000/

🖥️ Usage
For Users

Go to Register tab → create account

Login → see Active Polls → vote

Check My Votes tab

For Admins

Login as superuser

Access Django Admin (/admin/) → create polls, questions, choices

In UI, see Admin Results tab → chart + CSV download

📤 CSV Export

Votes can be exported per poll.
API:

GET /api/polls/<poll_id>/export/


Response → CSV file with:

poll_id	poll_title	question	choice	user	voted_at
📊 Example Chart

Admin sees results in Pie Chart (powered by Chart.js):



🔑 Default Credentials (Demo)

Admin → username: admin, password: admin123

User → register from UI
