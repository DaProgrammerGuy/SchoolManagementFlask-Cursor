# SchoolManagementFlaskV2

## Modular Project Structure

```
SchoolManagementFlaskV2/
│
├── app.py                # App entry point, create_app() factory
├── config.py             # Configuration settings (dev, prod, etc.)
├── extensions.py         # Extensions (db, migrate, jwt, etc.)
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── grade.py
│   ├── subject.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── admin.py
│   ├── teacher.py
│   ├── student.py
│
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── grade_service.py
│   ├── subject_service.py
│
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   ├── serializers.py
│
├── migrations/           # Alembic migrations
│
├── tests/                # Unit tests
│
└── README.md
```