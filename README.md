# 🇺🇸 CivicID — National Identity & Verification System

> A secure, role-based civic infrastructure platform designed to simulate real-world government systems.

---

## Overview

CivicID is a Django and Django REST Framework backend that models a multi-agency identity and civic management platform.

It supports structured interaction across domains such as:

- Identity management
- Birth registration
- Naturalization and immigration tracking
- ID applications and issued IDs
- Voter registration and voter ID issuance
- Passport issuance
- Law-enforcement verification
- Audit and compliance logging

The platform is designed around strict role-based access control, JWT authentication, and privacy-aware data access.

---

## Project Goals

- Build a centralized identity system
- Enforce role-based access control (RBAC)
- Secure APIs with JWT authentication
- Track sensitive actions through audit logs
- Support civic workflows such as voter registration
- Simulate real-world multi-domain backend architecture

---

## System Roles

| Role | Description |
|------|-------------|
| SUPER_ADMIN | Full system access for development and testing |
| REGISTRAR | Manages birth records and naturalization-related workflows |
| DMV | Handles ID applications and issued IDs |
| LAW_ENFORCEMENT | Performs identity verification requests |
| AUDITOR | Reviews audit logs and compliance records |
| ELECTIONS | Manages voter registration workflows |
| STATE_DEPT | Supports passport-related workflows |

---

## Tech Stack

- Python 3.12
- Django 5.2.4
- Django REST Framework 3.16.1
- SimpleJWT 5.5.1
- SQLite (development)
- django-cors-headers
- django-filter
- Celery
- Redis
- Pillow
- Gunicorn

---

## Authentication

JWT is used for protected API access.

### Obtain token
`POST /api/token/`

### Refresh token
`POST /api/token/refresh/`

Use the returned access token on protected routes:

`Authorization: Bearer <access_token>`

---

## Core API Domains

- `/api/persons/`
- `/api/birth-records/`
- `/api/id-applications/`
- `/api/issued-ids/`
- `/api/immigration-status/`
- `/api/naturalization/`
- `/api/voter-registrations/`
- `/api/voter-ids/`
- `/api/passports/`
- `/api/law-enforcement/`
- `/api/audit-logs/`

---

## Key Features

### Identity and Credentialing
- Person records
- Birth records
- Naturalization records
- Immigration status tracking
- ID applications and issued IDs
- Passport issuance

### Voter Registration
- Identity-linked voter registration
- Duplicate registration prevention
- Eligibility checks
- Felony ineligibility tracking
- Rights restoration tracking
- Voter ID issuance

### Law Enforcement Verification
- Reason-based identity verification requests
- Minimal-person-data response design
- Officer-specific verification history
- Automatic audit logging on lookups

### Audit Logging
- Tracks sensitive actions across the system
- Supports accountability and traceability
- Used in law-enforcement and voter workflows

---

## Frontend Pages

The project also includes a frontend template layer for:

- dashboard
- persons
- birth records
- ID applications
- issued IDs
- immigration
- law enforcement
- administration
- voter registration
- passport pages

---

## Project Status

### Completed
- Core identity models
- JWT authentication
- RBAC foundation
- Law-enforcement verification MVP
- Voter registration module
- Passport module
- Manual audit logging
- Frontend page routing

### In Progress
- Automated audit logging
- Permission hardening
- Template and frontend completion
- Data exposure controls

### Planned
- Full frontend dashboard polish
- Docker deployment
- Cloud hosting
- Java / Spring Boot version

---

## Why This Project Matters

CivicID demonstrates:

- secure backend architecture
- role-based system design
- civic and identity workflow modeling
- audit-focused engineering
- multi-domain data design
- real-world API and frontend integration

---

## Author

**Veries Seals III**  
B.S. Computer Science (Software Engineering)  
Colorado Technical University

---

> Built with real-world system design in mind.