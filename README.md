# 🎓 CampusID — Smart Student Identity & Management System

### A smarter way to manage student identities.

**Digital ID Cards** • **QR Code Verification** • **Student Management** • **PDF Downloads**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap)

---


---

## 📌 About the Project

**CampusID** is a web-based Student Identity and Management System developed to simplify student record management and digital identity verification.

The application provides an administrator interface for managing student information and generating digital identity cards. Students can log in to their personal dashboard, view their registered information, access their digital ID card, and download their ID card as a PDF.

With QR code integration and bulk student registration through Excel files, CampusID aims to make student identity management more convenient, organized, and efficient.

## ✨ Key Features

### 👨‍💼 Administrator Dashboard

- Manage student records from a centralized interface.
- Register students and maintain their information.
- Support bulk student registration using Excel files.
- Upload student photographs through the registration workflow.
- Generate student identity cards with QR codes.

### 🪪 Digital Student ID Cards

- Generate personalized student ID cards.
- Display student photographs, names, courses, and unique student IDs.
- Include QR codes for identity verification.
- Download student ID cards as PDF files.

### 📱 Student Dashboard

- Secure student login using the application's configured credentials.
- View personal profile information.
- Access a digital ID card directly from the dashboard.
- View the associated QR code.
- Download the ID card PDF.

### 🔎 QR Code Verification

- Generate QR codes associated with student identity records.
- Provide a verification page for checking student information.
- Help simplify the process of verifying a student's identity.

### 📊 Bulk Student Registration

- Import multiple student records using an Excel spreadsheet.
- Match uploaded photographs using the provided filenames.
- Reduce repetitive manual data entry.

### 🎨 User Interface

- Responsive web interface built with HTML, CSS, and Bootstrap.
- Bootstrap Icons for a consistent visual experience.
- Separate student and administrator interfaces.

## 🛠️ Technology Stack

| Technology      | Purpose                              |
| --------------- | ------------------------------------ |
| Python          | Core application logic               |
| Flask           | Web application framework            |
| SQLite          | Student and application data storage |
| HTML5           | Webpage structure                    |
| CSS3            | Styling and responsive layouts       |
| Bootstrap 5     | UI components and responsive design  |
| Bootstrap Icons | Interface icons                      |
| QR Code library | QR code generation                   |
| Pillow (PIL)    | Image processing                     |
| Pandas          | Excel data processing                |
| OpenPyXL        | Excel workbook support               |
| ReportLab       | PDF generation                       |

## 🖥️ Application Workflow

1. The administrator registers individual students or imports multiple records.
2. Student information and photographs are stored by the application.
3. A unique student ID and associated QR code are generated.
4. Students log in to access their personal dashboard.
5. Students view their profile and digital ID card.
6. The ID card can be downloaded as a PDF.
7. The QR code directs the user to the application's verification page.

## 📸 Screenshots

Add your actual project screenshots to a `screenshots/` folder and update the filenames below.

| Administrator Dashboard           | Student Dashboard                   |
| --------------------------------- | ----------------------------------- |
| `screenshots/admin-dashboard.png` | `screenshots/student-dashboard.png` |

| Digital Student ID Card           | QR Verification Page              |
| --------------------------------- | --------------------------------- |
| `screenshots/digital-id-card.png` | `screenshots/qr-verification.png` |

> **Tip:** Screenshots make your repository more attractive to recruiters and other developers. Use dummy student information in publicly shared screenshots.

## ⚙️ Installation and Setup

Follow these steps to run CampusID locally.

### Prerequisites

Install the following software:

- Python 3
- Git
- Visual Studio Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/hetmochi05/CampusID.git
```

Navigate to the project directory:

```bash
cd CampusID
```

> If your GitHub repository uses a different URL or capitalization, replace the URL and folder name accordingly.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` contains the packages required by your application.

### 4. Configure the application

Before running the project:

- Configure the Flask secret key securely.
- Ensure the required database tables are initialized.
- Create the upload directory if it does not exist.
- Configure or create an administrator account using your application's existing setup process.

**Important:** Do not publish real student records, private photographs, passwords, or production secrets.

### 5. Run the application

If `app.py` is the application's entry point, run:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

If your application uses a different startup command or route, follow the configuration in your source code.

## 📁 Project Structure

The structure below is a suggested layout. Keep the actual filenames and folders that exist in your repository.

```text
CampusID/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── student_profile.html
│   ├── id_card.html
│   ├── verify.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│       └── .gitkeep
│
└── screenshots/
    ├── admin-dashboard.png
    ├── student-dashboard.png
    ├── digital-id-card.png
    └── qr-verification.png
```

## 🔐 Security and Privacy

CampusID is an educational project and should be configured carefully before being used with real student information.

- Never commit real student databases or personal records to a public repository.
- Keep secret keys and credentials outside source control.
- Validate uploaded files and restrict allowed file types.
- Protect administrator and student routes against unauthorized access.
- Ensure QR verification pages reveal only the information necessary for verification.
- Use HTTPS and appropriate security controls before deploying publicly.

## 🚀 Future Enhancements

Potential improvements for future versions include:

- [ ] Email notifications for student registration.
- [ ] Student profile editing requests.
- [ ] Improved student search and filtering.
- [ ] ID card expiration and renewal management.
- [ ] Audit logs for administrative activities.
- [ ] Cloud deployment and database integration.
- [ ] Improved access control and security monitoring.
- [ ] Mobile-friendly ID card presentation.

## 🎯 Project Objectives

- Digitize student identity card management.
- Reduce repetitive administrative work.
- Provide convenient access to digital student ID cards.
- Simplify identity verification using QR codes.
- Practice real-world web development using Python and Flask.

## 🎓 Learning Outcomes

This project provides practical experience with:

- Flask routing and template rendering.
- Database operations using SQLite.
- Session-based authentication.
- HTML, CSS, and Bootstrap UI development.
- QR code generation and image handling.
- Excel data import and validation.
- PDF document generation.
- Organizing and publishing a software project on GitHub.

## 👨‍💻 Developer

**Het Mochi**

BCA Graduate | MCA Student | Aspiring Software Developer

GitHub: [@hetmochi05](https://github.com/hetmochi05)
Linkedin: [@hetmochi05]()

## ⭐ Support

If you find this project useful for learning or inspiration, consider giving the repository a star ⭐ on GitHub.

## 📄 License

No license has been specified yet. Unless a license is added, others should not assume they have permission to reuse, distribute, or modify this project's code.

---

\<p align="center">
&#x20; \<strong>CampusID — One Campus. One Identity. Smarter Verification.\</strong>
&#x20; \<br>
&#x20; Built with Python, Flask, and a passion for software development.
\</p>
