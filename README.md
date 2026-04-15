# 🇺🇸 CivicID — National Identity & Verification System

> A secure, role-based civic infrastructure platform designed to simulate real-world government systems.

---

## Overview

CivicID is a Django and Django REST Framework backend that models a multi-agency identity and civic management platform. It supports structured interaction across all major civic identity domains — from birth registration to death records, marriage certificates, Social Security, Selective Service, voter registration, and passport issuance.

The platform enforces strict role-based access control, JWT authentication, privacy-aware data design, and a permanent, tamper-evident audit trail.

---

## Project Goals

- Build a centralized national identity system
- Enforce role-based access control (RBAC) across all agencies
- Secure APIs with JWT authentication
- Track every sensitive action through an immutable audit log
- Support full civic lifecycle: birth → identity → civic participation → death
- Simulate real-world multi-agency backend architecture

---

## System Roles

| Role | Description |
|------|-------------|
| SUPER_ADMIN | Full system access for development and testing |
| REGISTRAR | Birth records, death records, marriage certificates, Social Security, Selective Service |
| DMV | ID applications and issued IDs |
| LAW_ENFORCEMENT | Identity verification lookups (reason required, privacy-first) |
| AUDITOR | Read-only audit log access |
| ELECTIONS | Voter registration, voter ID issuance, felony flag and rights restoration |
| STATE_DEPT | Passport issuance and status management |
| SSA | Social Security Number issuance and management |
| IMMIGRATION | Immigration status tracking and naturalization records |

---

## Tech Stack

- Python 3.12
- Django 5.2.4
- Django REST Framework 3.16.1
- SimpleJWT 5.5.1
- SQLite (development)
- django-cors-headers
- django-filter
- Celery 5.5.3
- Redis 6.4.0
- Pillow 11.3.0
- Gunicorn 23.0.0

---

## Authentication

JWT is used for all protected API access.

### Obtain token
`POST /api/token/`

### Refresh token
`POST /api/token/refresh/`

All protected routes require:
```
Authorization: Bearer <access_token>
```

---

## Core API Domains

| Endpoint | Description |
|----------|-------------|
| `/api/persons/` | Identity registry — PATCH triggers audit-logged change record |
| `/api/birth-records/` | Birth certificate registration |
| `/api/death-records/` | Death certificates — cascades to voter, passport, selective service |
| `/api/marriage-certificates/` | Civil union registry — name changes applied automatically |
| `/api/social-security/` | SSN assignment — SSN write-only, masked on read |
| `/api/selective-service/` | Federal Selective Service registration |
| `/api/person-photos/` | Photo history per person |
| `/api/id-applications/` | DMV ID applications |
| `/api/issued-ids/` | Issued ID credentials |
| `/api/immigration-status/` | Immigration status records |
| `/api/naturalization/` | Naturalization records |
| `/api/voter-registrations/` | Voter registration records |
| `/api/voter-ids/` | Voter ID credentials |
| `/api/passports/` | Passport issuance and management |
| `/api/law-enforcement/verify/` | Privacy-first identity lookup (reason required) |
| `/api/law-enforcement/history/` | Officer's own lookup history |
| `/api/voter/eligibility/` | Eligibility check (citizenship, age, felony gates) |
| `/api/voter/register/` | Register voter + issue voter ID |
| `/api/voter/flag-felony/` | Flag felony conviction, suspend voter ID |
| `/api/voter/restore/` | Restore voting rights, reactivate voter ID |
| `/api/audit-logs/` | Read-only compliance audit trail |
| `/api/token/` | Obtain JWT |
| `/api/token/refresh/` | Refresh JWT |

---

## Key Features

### Identity & Credentialing
- Person records with full demographic data, gender, address, and photo
- Birth record registration (link to existing or create new person simultaneously)
- Naturalization and immigration status tracking
- ID applications and issued credentials
- Passport issuance with days-remaining tracking

### Vital Events
- **Death Records** — filing automatically suspends voter registration, voter ID, passport, and selective service via Django signals
- **Marriage Certificates** — name changes applied automatically to Person records; maiden name preserved; audit logged
- **Person Edits** — every PATCH to a Person record diffs before/after state, requires a typed reason, and writes a permanent audit entry with officer identity and timestamp

### Social Security
- OneToOne SSN assignment per person
- SSN stored as plain text in dev; write-only in API (only masked display `***-**-1234` returned)
- Access restricted to SSA, REGISTRAR, and SUPER_ADMIN roles

### Selective Service
- Federal law compliance: all males 18–25 required to register (50 U.S.C. § 3802), regardless of citizenship
- Auto-registration via Celery Beat task daily at midnight UTC when a qualifying person turns 18
- Auto-deregistration at age 26 (daily task at 00:30 UTC)
- Manual registration with gender/age validation warnings in UI

### Voter Registration
- Three-gate eligibility: citizenship, age 18+, no active felony
- Automatic voter registration + voter ID issuance on eligibility confirmation
- Felony flagging suspends voter ID immediately
- Rights restoration reactivates registration and voter ID

### Law Enforcement Verification
- Reason required before any data is returned
- Only 5 minimum-necessary fields returned (name, DOB, citizenship)
- Every lookup automatically logged to audit trail
- Officers can only view their own history

### Audit & Compliance
- All sensitive actions across every module write to `AuditLog`
- Person edits record: officer, timestamp, reason, and field-level diff (`{from, to}` per field)
- Death record filings, marriage registrations, voter actions, LE lookups all auto-logged
- Read-only via API; no delete endpoint

### Automated Tasks (Celery + Redis)
- **Midnight UTC**: `run_daily_civic_checks` — auto-registers voters and selective service for everyone turning 18 that day
- **00:30 UTC**: `deregister_selective_service_age_26` — removes persons from selective service rolls at age 26

---

## Frontend Pages

| Page | Roles | Description |
|------|-------|-------------|
| `/` | All | Agency selection + secure login |
| `/pages/dashboard/` | All | System-wide stats and recent activity |
| `/pages/persons/` | All (edit: REGISTRAR, DMV, SUPER_ADMIN) | Identity registry with edit modal + audit trail |
| `/pages/birth-records/` | REGISTRAR, SUPER_ADMIN | New record modal: existing person or create new inline; gender field |
| `/pages/death-records/` | REGISTRAR, LAW_ENFORCEMENT, SUPER_ADMIN | File death record; cascades fire automatically |
| `/pages/marriage/` | REGISTRAR, SUPER_ADMIN | Register marriage; name changes auto-applied |
| `/pages/social-security/` | SSA, REGISTRAR, SUPER_ADMIN | Issue SSN; masked display |
| `/pages/selective-service/` | REGISTRAR, SUPER_ADMIN | Registry + manual registration with age/gender warnings |
| `/pages/id-applications/` | DMV, SUPER_ADMIN | ID application management |
| `/pages/issued-ids/` | DMV, SUPER_ADMIN | Credential status and expiration tracking |
| `/pages/immigration/` | IMMIGRATION, SUPER_ADMIN | Immigration status + naturalization |
| `/pages/voter-registration/` | ELECTIONS, SUPER_ADMIN | Eligibility check, registration, felony flag, rights restoration |
| `/pages/passport/` | STATE_DEPT, SUPER_ADMIN | Passport issuance and status management |
| `/pages/law-enforcement/` | LAW_ENFORCEMENT | Identity lookup portal |
| `/pages/audit/` | AUDITOR, SUPER_ADMIN | Full audit log with action filtering |
| `/pages/administration/` | SUPER_ADMIN | System overview, module links, API reference |

---

## Running the Project

### 1. Start Django
```bash
python manage.py runserver
```

### 2. Start Redis (required for Celery)
```bash
brew install redis        # macOS — one time only
brew services start redis
redis-cli ping            # expect: PONG
```

### 3. Start Celery Worker
```bash
celery -A civicid worker --loglevel=info
```

### 4. Start Celery Beat (scheduled tasks)
```bash
celery -A civicid beat --loglevel=info
```

### Media directory setup (one time)
```bash
mkdir -p media/person_photos/history
cp templates/civicid-frontend/media/civic_id_2026.png media/civic_id_2026.png
```

### Create superuser
```bash
python manage.py createsuperuser
```

---

## Project Status

### Completed
- Core identity models with full migration history
- JWT authentication + RBAC (9 roles)
- Law enforcement verification (privacy-first, audit-logged)
- Voter registration module (eligibility gates, felony tracking, rights restoration)
- Passport module with days-remaining calculation
- Birth records with inline person creation
- Death records with automatic cascade signals
- Marriage certificates with automatic name change signals
- Social Security registry (SSN masked in API)
- Selective Service registry (federal law compliance)
- Person edit audit logging (field-level diff, officer, timestamp, reason)
- Celery + Redis automated civic tasks (age 18 registration, age 26 deregistration)
- Full frontend with 16 pages, role-gated navigation
- SSA agency card on login page

### Planned
- Docker deployment
- Cloud hosting
- Java / Spring Boot version
- Full permission hardening (DRF permission classes per role per endpoint)
- Person profile page with linked records view
- Photo upload UI

---

## Why This Project Matters

CivicID demonstrates:

- Secure, production-grade backend architecture
- Multi-agency role-based system design
- Full civic lifecycle modeling (birth → identity → participation → death)
- Privacy-first API design (law enforcement minimal-data pattern)
- Audit-focused engineering (immutable logs, field-level diffs, officer attribution)
- Signal-driven cascade automation
- Scheduled task automation with Celery and Redis
- Real-world multi-domain data relationships

---

## Author

**Veries Seals III**
B.S. Computer Science (Software Engineering)
Colorado Technical University

---

> Built with real-world system design in mind.