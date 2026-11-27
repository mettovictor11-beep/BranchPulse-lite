# BranchPulse Lite 📊

**Branch Performance & Target Analysis System**

BranchPulse Lite is a Python-based management dashboard designed to help organizations monitor branch performance, compare targets against actual results, and generate performance reports.

## Features

- Add, view, edit, and delete performance records.
- Track Revenue, Disbursement, and Sales.
- Calculate performance variance and achievement percentages.
- Filter records by branch and performance type.
- Filter reports by date range.
- Rank branches according to achievement percentage.
- Visualize branch performance using charts.
- Highlight branches that meet or fall below targets.
- Export performance reports to CSV.
- Store records persistently using SQLite.

## Technologies Used

- Python
- Streamlit
- Pandas
- SQLite
- Git and GitHub

## Project Structure

```text
branchpulse-lite/
├── main.py
├── database.py
├── performance.py
├── test_performance.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mettovictor11-beep/BranchPulse-lite.git
   ```

2. Navigate into the project folder:

   ```bash
   cd branchpulse-lite
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment:

   **Windows Git Bash:**

   ```bash
   source .venv/Scripts/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   streamlit run main.py
   ```

## Database

BranchPulse Lite uses SQLite to store branch performance records. The database table is created automatically when the application starts.

## Purpose

The project demonstrates Python object-oriented programming, database integration, CRUD operations, data analysis, visualization, and report generation through an interactive dashboard.

## Future Improvements

- User authentication and role-based access.
- Multi-branch organizational management.
- Automated PDF reports.
- Monthly and weekly performance summaries.
- Advanced management analytics.

---

**BranchPulse Lite | Performance made simple.**