# 🧠 LifeOS

> **An Offline Personal Productivity Management System built with Python, CustomTkinter, SQLite, Matplotlib, and Seaborn.**

LifeOS is a desktop productivity application developed as a college mini-project. It brings **task management, notes, planning, focus tracking, Pomodoro, stopwatch timing, analytics, activity history, reporting, backup/restore, and local settings** into one application.

The project is designed as a **fully offline Windows desktop application**. Core data is stored locally in SQLite, so LifeOS does not require a web browser, online account, cloud database, or internet connection for normal use.

---

## ✨ Highlights

- ✅ Task management with priorities, categories, due dates, completion tracking, and filters
- 📝 Notes with categories, search, full-note popup viewing, editing, and deletion
- 📅 Interactive monthly planner with dated activities and completion tracking
- 🎯 Focus Mode with task linking, pause/resume, partial-session saving, and navigation protection
- 🍅 Pomodoro timer with Focus, Short Break, Long Break, and custom durations
- ⏱️ Stopwatch with pause/resume, laps, saved sessions, and history
- 📊 Productivity score based on real application activity
- 📈 Analytics with Matplotlib and Seaborn visualizations
- 🕘 Categorized history for tasks, planner, focus, Pomodoro, and stopwatch records
- 📄 Daily, Weekly, and Monthly reports with TXT export
- 💾 Local SQLite database backup and restore
- 🌙 Dark, Light, and System appearance modes
- 🧭 Responsive collapsible sidebar navigation
- 🖱️ Mouse-wheel and trackpad scrolling support
- 🪟 Responsive desktop layouts across major pages
- 📦 PyInstaller-ready Windows executable packaging

---

# 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Productivity Score](#-productivity-score)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Building the Windows EXE](#-building-the-windows-exe)
- [Major Application Modules](#-major-application-modules)
- [Database and Local Storage](#-database-and-local-storage)
- [Reports and Exports](#-reports-and-exports)
- [Backup and Restore](#-backup-and-restore)
- [Testing Checklist](#-testing-checklist)
- [Future Improvements](#-future-improvements)
- [GitHub Setup](#-github-setup)
- [Project Status](#-project-status)
- [Author](#-author)

---

# 📖 About the Project

**LifeOS** is a Python-based personal productivity desktop application.

The application allows a user to manage:

- Tasks
- Notes
- Daily planning
- Focus sessions
- Pomodoro sessions
- Stopwatch sessions
- Productivity analytics
- Activity history
- Daily / Weekly / Monthly reports
- Local backups
- Application settings

Unlike a web application, LifeOS runs directly as a desktop interface using **CustomTkinter / Tkinter**.

All core productivity data is stored locally using **SQLite**.

---

# 🚀 Features

## ✅ Task Manager

The Task Manager supports complete task management.

### Available operations

- Add tasks
- Edit tasks
- Delete tasks
- Complete / uncomplete tasks
- Add descriptions
- Set due dates
- Assign priorities
- Assign categories
- Filter tasks by status and date

### Priorities

- Low
- Medium
- High

### Categories

- General
- Study
- College
- Personal
- Work
- Fitness
- Other

### Filters

- All Tasks
- Pending
- Completed
- Today
- Upcoming
- Overdue

Completed tasks also store completion timestamps for reporting, analytics, and history.

---

## 📝 Notes

LifeOS contains a local notes system.

### Features

- Create notes
- Edit notes
- Delete notes
- Search note titles and content
- Filter notes by category
- View note previews
- Open the complete note in a popup
- Edit the full note directly inside the popup

### Note Categories

- General
- Study
- College
- Personal
- Work
- Ideas
- Other

The note cards display a preview, while the full note can be opened in a dedicated in-app popup without leaving the Notes page.

---

## 📅 Planner

The Planner provides an interactive monthly calendar.

### Features

- Previous month
- Next month
- Jump to Today
- Select a date
- Add dated activities
- Start and end times
- Activity categories
- Completion tracking
- Activity counts on calendar dates
- Today's schedule display on Dashboard

The Planner is intended for scheduled activities, while Tasks are used for actionable work items.

---

## 🎯 Focus Mode

Focus Mode provides a dedicated deep-work timer.

### Features

- General focus sessions
- Link a session to a pending task
- Preset durations: 15, 25, 45, and 60 minutes
- Start
- Pause
- Resume
- Stop
- Completed-session tracking
- Partial-session saving
- Recent Focus history

### Navigation Protection

While a Focus session is active, LifeOS protects the session from accidental navigation or application closing.

If the user tries to leave Focus Mode, LifeOS asks whether the current focus session should be stopped and saved.

---

## 🍅 Pomodoro

The Pomodoro module includes:

- Focus
- Short Break
- Long Break
- Custom timer durations
- Start
- Pause
- Resume
- Reset
- Session history
- Today's Pomodoro statistics

Completed sessions are stored in the database.

---

## ⏱️ Stopwatch

The Stopwatch uses high-resolution timing for open-ended work sessions.

### Features

- Start
- Pause
- Resume
- Reset
- Lap recording
- Save session
- Session duration
- Lap count
- Recent stopwatch history
- Today's stopwatch statistics

The stopwatch state remains active while navigating between cached LifeOS pages.

---

## 🏠 Dashboard

The Dashboard provides a quick productivity overview.

It includes:

- Task statistics
- Pending tasks
- Completed tasks
- Focus statistics
- Pomodoro activity
- Productivity score
- Today's tasks
- Today's planner activities
- Weekly productivity chart
- Quick Focus
- Quick Note

---

## 📊 Analytics

The Analytics page visualizes real LifeOS activity.

### Current analytics include

- Productivity score
- Task completion
- Focus time
- Planner completion
- Weekly productivity trend
- Weekly focus activity
- Task completion charts

Charts are created using **Matplotlib** and **Seaborn**.

---

## 🕘 History

LifeOS maintains categorized history for:

- Focus
- Pomodoro
- Stopwatch
- Tasks
- Planner

### Filters

- All Time
- Today
- Last 7 Days
- Last 30 Days

---

## 📄 Reports

The Reports module provides:

- Daily reports
- Weekly reports
- Monthly reports
- Tasks completed
- Categories used
- Top category
- Completed-task details
- Category distribution
- TXT export

### Current reporting periods

```text
Daily   = Today
Weekly  = Monday through Today
Monthly = First day of current month through Today
```

---

## ⚙️ Settings

The Settings page includes:

- Dark, Light, and System appearance modes
- Export-folder configuration
- Local database path display
- Settings path display
- Database backup
- Database restore
- Reset settings
- About LifeOS information

---

# 🧮 Productivity Score

LifeOS uses an explainable productivity score based on actual activity.

| Component | Contribution |
|---|---:|
| Task Completion | 50% |
| Focus Time | 30% |
| Planner Completion | 20% |

The maximum score is `100`.

### Score Labels

| Score | Label |
|---|---|
| 80–100 | Excellent |
| 60–79 | Productive |
| 40–59 | Moderate |
| 1–39 | Getting Started |
| 0 | No Activity |

Stopwatch sessions do not currently affect the productivity score.

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Programming Language | Python 3 |
| Desktop UI | CustomTkinter |
| Base GUI Toolkit | Tkinter |
| Database | SQLite |
| Charts | Matplotlib |
| Visualization Styling | Seaborn |
| Image Support | Pillow |
| Configuration | JSON |
| Packaging | PyInstaller |
| Code Editor | Visual Studio Code |
| Version Control | Git |
| Repository Hosting | GitHub |
| Target Platform | Windows |

---

# 📁 Project Structure

```text
LifeOS/
│
├── main.py
├── LifeOS.spec
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── ui/
│   ├── __init__.py
│   ├── animations.py
│   ├── theme.py
│   ├── lifeos_theme.json
│   ├── components.py
│   ├── dashboard.py
│   ├── tasks.py
│   ├── notes.py
│   ├── planner.py
│   ├── focus_mode.py
│   ├── pomodoro.py
│   ├── stopwatch.py
│   ├── analytics.py
│   ├── history.py
│   ├── reports.py
│   └── settings.py
│
├── utils/
│   ├── __init__.py
│   ├── productivity.py
│   └── settings_manager.py
│
├── assets/
│   └── icons/
│
├── data/
│   ├── lifeos.db
│   └── settings.json
│
├── exports/
│
├── build/
│
└── dist/
    └── LifeOS/
        ├── LifeOS.exe
        └── _internal/
```

> `build/`, `dist/`, local databases, and environment-specific files can be excluded from Git depending on how the repository is maintained.

---

# ✅ Requirements

## Python

Recommended:

```text
Python 3.10+
```

Check installation:

```powershell
python --version
```

## Python Packages

Install the main dependencies:

```powershell
pip install customtkinter matplotlib seaborn pillow pyinstaller
```

If the project contains a `requirements.txt`, use:

```powershell
pip install -r requirements.txt
```

---

# 📥 Installation

## Step 1 — Clone the Repository

```powershell
git clone https://github.com/tushar-011/LifeOS.git
cd LifeOS
```

## Step 2 — Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## Step 3 — Install Dependencies

```powershell
pip install -r requirements.txt
```

or:

```powershell
pip install customtkinter matplotlib seaborn pillow pyinstaller
```

---

# ▶️ Running the Application

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Then run:

```powershell
python main.py
```

LifeOS opens as a native desktop application.

No browser is required.

---

# 📦 Building the Windows EXE

LifeOS can be packaged with **PyInstaller**.

A one-folder build is recommended first because it is easier to test and debug.

From the project root:

```powershell
pyinstaller --noconfirm --clean --windowed --name LifeOS --add-data "ui\lifeos_theme.json;ui" --add-data "assets;assets" --add-data "data;data" main.py
```

After a successful build, the executable is expected under:

```text
dist/
└── LifeOS/
    ├── LifeOS.exe
    └── _internal/
```

Run:

```text
dist\LifeOS\LifeOS.exe
```

> The `LifeOS.exe` file should remain with its generated `_internal` folder when using PyInstaller one-folder mode.

---

# 🧩 Major Application Modules

```text
LifeOS
│
├── Dashboard
├── Tasks
├── Notes
├── Planner
├── Focus Mode
├── Pomodoro
├── Stopwatch
├── Analytics
├── History
├── Reports
└── Settings
```

---

# 🗄️ Database and Local Storage

LifeOS stores its core application data locally using SQLite.

Examples of stored data include:

- Tasks
- Task completion timestamps
- Notes
- Planner activities
- Focus sessions
- Pomodoro sessions
- Stopwatch sessions
- History-related activity

The application also uses JSON for local configuration such as appearance mode and export-folder settings.

Typical local data files:

```text
data/lifeos.db
data/settings.json
```

LifeOS does not require an external database server.

---

# 📄 Reports and Exports

Reports can be exported as `.txt` files.

The configured export location can be changed from:

```text
Settings → Exports
```

Exports include:

- Report type
- Date range
- Generated timestamp
- Tasks completed
- Categories used
- Top category
- Completed task details
- Category summary
- Category percentages

---

# 💾 Backup and Restore

LifeOS includes database-management controls directly inside the application.

### Backup

A copy of the current SQLite database can be saved to a selected location.

### Restore

An existing `.db` backup can be restored.

Before replacing the active database, LifeOS creates a safety backup of the current database.

After restoring a database, restarting LifeOS is recommended so all cached pages reload the restored data.

---

# 🧪 Testing Checklist

Before demonstration or submission, test:

- Application launch
- Sidebar expand / collapse
- Page navigation
- Mouse-wheel scrolling
- Window resizing
- Dark mode
- Light mode
- Task CRUD
- Task filters
- Notes create / edit / delete
- Notes popup viewing
- Planner activity creation
- Focus Mode start / pause / resume / stop
- Focus navigation lock
- Pomodoro timer
- Stopwatch laps and save
- Analytics charts
- History categories and date filters
- Daily / Weekly / Monthly reports
- TXT report export
- Export-folder selection
- Database backup
- Database restore
- Settings reset
- Packaged EXE launch

---

# 🔒 Privacy Notes

LifeOS is designed as an offline-first academic desktop application.

Core productivity data is stored locally on the user's computer.

The current project does not require:

- User registration
- Online login
- Cloud database
- Remote API
- Cloud synchronization
- Subscription service

Users should still keep backups of important local data.

---

# 🔮 Future Improvements

Possible future additions include:

- Calendar notifications
- Desktop reminders
- System tray integration
- Recurring tasks
- Recurring planner activities
- PDF report export
- CSV export
- Advanced productivity goals
- Habit tracking
- Data import/export
- Custom themes
- Keyboard shortcuts
- Search across all modules
- Optional cloud sync
- Multi-device synchronization
- One-file EXE distribution
- Installer package

These are outside the current mini-project scope.

---

# 🌐 GitHub Setup

Useful Git commands:

```powershell
git status
git add .
git commit -m "Your commit message"
git push origin main
```

For the completed LifeOS project:

```powershell
git add .
git commit -m "Finalize LifeOS productivity desktop application"
git push origin main
```

Check:

```powershell
git status
```

Expected result:

```text
nothing to commit, working tree clean
```

---

# 🏁 Project Status

### ✅ Core mini-project development complete

LifeOS currently demonstrates:

- Python desktop GUI development
- Object-oriented programming
- Modular application structure
- SQLite database integration
- CRUD operations
- Date and time handling
- Timers
- Local state management
- File handling
- JSON configuration
- Data visualization
- Productivity analytics
- Reporting
- Local backup and restore
- Responsive desktop UI design

The project is now primarily in its **final testing, packaging, documentation, and submission stage**.

---

# 👨‍💻 Development Notes

LifeOS was created as an academic mini-project with emphasis on building a practical, usable Python desktop application.

It is intended for learning, demonstration, academic submission, and portfolio use.

---

<div align="center">

## 🧠 LifeOS

**Tasks • Notes • Planner • Focus • Time Tracking • Analytics • Reports**

Built with **Python + CustomTkinter + SQLite**

</div>

---

# 👨‍💻 Author

### Tushar Thakur

**MCA Data Science**  
**Chandigarh University**

[![GitHub](https://img.shields.io/badge/GitHub-tushar--011-181717?logo=github)](https://github.com/tushar-011)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Tushar%20Thakur-0A66C2?logo=linkedin)](https://www.linkedin.com/in/tushar-thakur-8848a7396)

[![Email](https://img.shields.io/badge/Email-artificial.thakur%40gmail.com-EA4335?logo=gmail)](mailto:artificial.thakur@gmail.com)
