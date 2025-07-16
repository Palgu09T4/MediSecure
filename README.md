
# 🏥 MediSecure

**MediSecure** is a full-stack web-based healthcare management system built using **Django** and **Bootstrap**, providing seamless coordination among patients, doctors, and lab technicians.

## 🚀 Features

### 👥 User Roles
- **Patients**: Register, login, view appointments, and access lab reports.
- **Doctors**: Manage appointments, add prescriptions, and request lab tests.
- **Lab Technicians**: Upload lab results and view doctor requests.

### 📋 Core Modules
- **Appointment Scheduling**: Patients can request appointments which are assigned to doctors.
- **Doctor Dashboard**: View assigned patients, upload prescriptions, and manage medical records.
- **Lab Test Requests**: Doctors can initiate lab tests; lab technicians upload results viewable by patients.
- **Medical History**: Centralized records accessible per patient across visits.

### 💻 Frontend Experience
- **Responsive Design**: Built with Bootstrap for a clean, mobile-friendly UI.
- **Role-based Dashboards**: Unique interfaces for each user type (Doctor, Patient, Lab).
- **Real-time Updates**: Smooth navigation and form feedback for improved UX.

## 🧰 Tech Stack

| Tool            | Purpose                          |
|-----------------|----------------------------------|
| Django          | Backend web framework            |
| SQLite          | Lightweight database             |
| Bootstrap       | Frontend styling                 |
| HTML/CSS        | Page structure and design        |
| JavaScript      | Basic interactivity              |

## Screenshots
<img width="772" height="641" alt="Screenshot 2025-05-26 200838" src="https://github.com/user-attachments/assets/9a989959-4a39-4c73-9252-67d20d747b5a" />
<img width="1627" height="892" alt="Screenshot 2025-05-26 200405" src="https://github.com/user-attachments/assets/ff2e78a0-325f-4766-a2ca-aca677c76c3c" />
<img width="1688" height="636" alt="Screenshot 2025-05-26 200453" src="https://github.com/user-attachments/assets/2067c015-d48c-4688-8dc0-d2ce2a4bb80e" />
<img width="765" height="846" alt="Screenshot 2025-05-26 200524" src="https://github.com/user-attachments/assets/6c90dd22-181d-4c8b-9514-62fe6934b3fe" />
<img width="909" height="380" alt="Screenshot 2025-05-26 200635" src="https://github.com/user-attachments/assets/bc733cac-32fb-4256-a077-8590d1b0fca9" />
<img width="1863" height="813" alt="Screenshot 2025-05-26 200646" src="https://github.com/user-attachments/assets/7aa40dce-e725-4f65-b094-9d4c969df596" />
<img width="1905" height="880" alt="Screenshot 2025-05-26 200721" src="https://github.com/user-attachments/assets/c767bb16-f41d-4055-9b8c-a7f34c153bfe" />
<img width="1911" height="734" alt="Screenshot 2025-05-26 200743" src="https://github.com/user-attachments/assets/3ea8684f-6192-422a-8a77-6fc7e51ad80c" />
<img width="1910" height="737" alt="Screenshot 2025-05-26 200756" src="https://github.com/user-attachments/assets/6c1f5b57-4bc5-45ef-bce4-6b192c89d206" />









## 🔧 Setup

```bash
git clone https://github.com/yourusername/healthcare.git
cd healthcare
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
