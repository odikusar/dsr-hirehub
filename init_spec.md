# JobMatch Lab — Level 1 Project Specification

## 1. Project Purpose

JobMatch Lab is an educational full-stack project for practicing modern Python backend engineering, React/Next.js frontend development, AI integration, and system design.

This is **not a production project** and the primary goal is **not fast delivery**.

The main goal is deliberate practice:
- implement the application manually;
- understand the technologies and architectural decisions;
- build muscle memory;
- practice patterns commonly discussed in Senior Full-Stack / Python backend interviews;
- gradually evolve a simple monolith into a more distributed AI-enabled system.

The project should stay understandable and compact. Avoid unnecessary entities, abstractions, libraries, and infrastructure.

---

## 2. Important Working Rules for Claude

Claude should behave as a technical mentor and pair-programming assistant, not as an autonomous implementation agent.

### Claude MAY:
- discuss architecture and trade-offs;
- help design specifications;
- review code written by the developer;
- explain errors and concepts;
- suggest terminal commands;
- provide small focused code examples;
- help design database models, APIs, tests, and system architecture;
- ask questions that help the developer reason about implementation;
- generate checklists and documentation.

### Claude SHOULD NOT:
- generate the entire application;
- generate large groups of files unless explicitly requested;
- silently implement features on behalf of the developer;
- perform large refactors automatically;
- introduce technologies only because they are popular;
- over-engineer simple requirements.

The developer should manually create and type the main project code.

When implementation is discussed, prefer:
1. explain the goal;
2. explain the design;
3. show the relevant command or small code fragment;
4. let the developer implement it;
5. review the result.

---

## 3. Product Idea

JobMatch Lab is a small job board and applicant tracking system.

There are two main user roles:

### Candidate
A candidate can:
- register and authenticate;
- browse available jobs;
- view job details;
- apply for a job;
- provide structured application information;
- upload a CV/resume;
- view their applications and application status.

### Employer / HR
An HR user can:
- register and authenticate;
- create and manage job vacancies;
- define basic candidate requirements;
- view applicants for a vacancy;
- inspect candidate information and CV data;
- update application status;
- later use AI-assisted candidate summaries, matching, and ranking.

---

## 4. Core Domain Model

Keep the database model intentionally small.

Initial core entities:

### User
Represents both candidates and HR users.

Possible fields:
- id
- email
- password/auth fields
- first_name
- last_name
- role: CANDIDATE | HR
- created_at
- updated_at

Do not create separate Candidate and HR tables unless a real requirement appears.

### Job
Represents a vacancy.

Possible fields:
- id
- title
- description
- company_name
- location
- employment_type
- requirements
- created_by -> User
- status: DRAFT | OPEN | CLOSED
- created_at
- updated_at

Initially, some job requirements may stay simple rather than being normalized into many extra tables.

### Application
Connects a candidate to a job.

Possible fields:
- id
- job -> Job
- candidate -> User
- status
- cover_note
- expected_salary
- years_of_experience
- created_at
- updated_at

The Application entity should become the central object for the hiring workflow.

### Resume
Represents an uploaded CV.

Possible fields:
- id
- user -> User
- original_filename
- storage_key / S3 object key
- mime_type
- uploaded_at
- processing_status
- extracted_text or processed metadata later

Prefer one active resume per candidate initially unless multiple resumes become useful.

### Main relationships

User (HR) 1 --- N Job

User (Candidate) 1 --- N Application

Job 1 --- N Application

User (Candidate) 1 --- 1 Resume
(initial simplification)

---

## 5. Main MVP User Flows

### Authentication
- user registration;
- login;
- logout;
- role-based access.

### Candidate Flow
1. Candidate logs in.
2. Candidate sees open jobs.
3. Candidate opens a job.
4. Candidate submits an application.
5. Candidate sees their applications and statuses.

### HR Flow
1. HR logs in.
2. HR creates a job.
3. HR edits or closes the job.
4. HR sees applications for the job.
5. HR opens an applicant.
6. HR changes application status.

Possible application statuses:
- APPLIED
- REVIEWING
- INTERVIEW
- REJECTED
- OFFER

Keep the workflow simple at first.

---

## 6. Phase 1 Technical Scope — Full-Stack Core

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- React Hook Form
- Zod
- routing and layouts
- forms and validation
- loading and error states
- protected routes

### Backend
- Python
- Django
- Django REST Framework
- Django ORM
- PostgreSQL
- models and migrations
- 1:1, 1:N and optionally N:N relationships
- serializers
- APIView
- ViewSet
- routers
- authentication
- permissions / roles
- CRUD
- pagination
- filtering / search / ordering
- middleware
- Django Admin
- basic transactions

### Infrastructure
- Docker
- Docker Compose

Phase 1 should result in a complete usable application without AI.

---

## 7. Backend Architecture Direction

CQRS should be the primary application pattern.

Conceptual request flow:

HTTP / DRF
    |
Command or Query
    |
Handler
    |
Unit of Work / Repository
    |
Django ORM / PostgreSQL

Examples:

Commands:
- CreateJobCommand
- UpdateJobCommand
- ApplyToJobCommand
- ChangeApplicationStatusCommand
- UploadResumeCommand

Queries:
- GetJobQuery
- ListJobsQuery
- GetApplicationQuery
- ListCandidateApplicationsQuery
- ListJobApplicantsQuery

Important:
CQRS here means separation of read and write responsibilities in application code.

Do NOT initially introduce:
- separate read/write databases;
- event sourcing;
- distributed CQRS infrastructure.

Those may be discussed later as system-design evolution.

---

## 8. Phase 2 — Backend Engineering

Gradually introduce:

- Repository Pattern
- Unit of Work
- dependency-injector
- Pydantic
- dataclasses
- Protocol / ABC where justified
- Redis
- caching
- Celery
- background jobs
- retries
- Celery Beat
- S3-compatible object storage
- presigned URLs
- PostgreSQL indexes
- constraints
- query optimization
- EXPLAIN / EXPLAIN ANALYZE
- transaction isolation
- locking
- asyncio
- structured logging
- pytest
- unit tests
- integration tests
- API tests

Security topics:
- authentication security
- authorization
- PII encryption at rest
- password hashing
- CSRF
- CORS
- rate limiting
- secrets management
- secure cookies / JWT depending on chosen auth design
- audit log
- log redaction

---

## 9. Phase 3 — Resume Processing and AI

Resume upload should become the natural entry point for AI functionality.

Target flow:

Candidate
    |
Upload CV
    |
S3
    |
Celery task
    |
Document extraction
    |
LLM processing
    |
Structured candidate profile
    |
PostgreSQL

LLM functionality may include:
- resume summarization;
- extraction of skills;
- extraction of experience;
- extraction of education;
- structured output validated with Pydantic;
- candidate-to-job match explanation;
- missing requirement detection.

The application should keep both original resume information and AI-generated information clearly separated.

---

## 10. RAG Evolution

Later, introduce:
- embeddings;
- pgvector first;
- document chunking;
- semantic search;
- retrieval;
- context construction;
- source references;
- simple RAG evaluation.

Possible use cases:
- HR asks questions about a candidate's resume;
- HR searches candidates semantically;
- AI compares a job description with candidate resume content;
- AI explains why a candidate matches or does not match a vacancy.

Prefer PostgreSQL + pgvector before adding a dedicated vector database.

---

## 11. Phase 4 — FastAPI AI Microservice

Initially, AI processing may live inside the Django application.

Later, move AI/document-processing responsibilities into a separate FastAPI service when this creates a useful architectural exercise.

Possible architecture:

Next.js
   |
Django / DRF
   |
   +---- PostgreSQL
   +---- Redis
   +---- S3
   |
   +---- Kafka / HTTP
             |
        FastAPI AI Service
             |
         LLM / RAG

FastAPI service topics:
- Pydantic request/response models;
- async endpoints;
- dependency injection;
- OpenAPI;
- service-to-service communication;
- retries and timeouts;
- health checks.

---

## 12. Phase 4+ — Messaging and Distributed Systems

Introduce Kafka only when there is a meaningful asynchronous event flow.

Potential events:
- ResumeUploaded
- ResumeProcessed
- ApplicationSubmitted
- ApplicationStatusChanged
- CandidateProfileUpdated

Practice:
- producer / consumer;
- topics;
- partitions;
- consumer groups;
- offsets;
- event schemas;
- idempotency;
- retries;
- dead-letter queue concept;
- eventual consistency;
- Outbox Pattern.

Do not use Kafka for simple synchronous CRUD.

---

## 13. Candidate Matching

Start simple and evolve.

### Version 1
Manual HR review.

### Version 2
Deterministic scoring:
- required skills;
- experience;
- location;
- salary expectations.

### Version 3
LLM-assisted matching:
- semantic comparison;
- explanation of strengths;
- explanation of missing requirements.

### Version 4
Optional ML exercise:
- small ranking/classification experiment;
- NumPy;
- Pandas;
- scikit-learn;
- train/test split;
- basic metrics.

The ML part is educational and should stay small.

---

## 14. Production / System Design Topics

After the application works, use it to practice:

- CI/CD;
- GitHub Actions;
- health checks;
- structured logging;
- correlation IDs;
- metrics;
- tracing;
- OpenTelemetry basics;
- deployment;
- managed PostgreSQL;
- managed Redis;
- object storage;
- horizontal scaling;
- stateless APIs;
- caching strategies;
- connection pooling;
- read replicas;
- load balancing;
- queues and backpressure;
- retries;
- circuit breakers;
- rate limiting;
- CDN;
- LLM rate limits;
- LLM cost optimization.

Optional later topics:
- Kubernetes;
- Terraform;
- Elasticsearch / OpenSearch;
- WebSockets;
- SSE;
- dedicated vector database.

---

## 15. Design Principles

### Keep it small
Avoid creating many domain entities.

Prefer:
- User
- Job
- Application
- Resume

Add new entities only when they solve a real design problem.

### Learn before abstracting
Start with understandable Django behavior before hiding everything behind abstractions.

### Introduce architecture gradually
The project should evolve:
1. working full-stack application;
2. stronger backend architecture;
3. background processing;
4. AI;
5. distributed system;
6. production/system-design exercises.

### Every technology needs a reason
Do not add Redis, Kafka, FastAPI, Kubernetes, or any other technology just to have it in the stack.

Each technology should solve a concrete project requirement.

---

## 16. Initial Success Criteria

The first milestone is complete when:

- Candidate and HR can register/login.
- HR can create and manage jobs.
- Candidate can browse jobs.
- Candidate can apply.
- HR can see applicants.
- HR can change application status.
- Candidate can see application status.
- PostgreSQL stores the domain data.
- Django ORM is used properly.
- DRF exposes the API.
- Next.js frontend consumes the API.
- Basic authorization is enforced.
- The whole project runs locally with Docker Compose.

At this milestone:
- no LLM is required;
- no Kafka is required;
- no FastAPI is required;
- no Kubernetes is required.

The project should first become a clean, understandable full-stack system.

---

## 17. Immediate Next Step

Do not generate the project automatically.

The next task is to design **Phase 1** in more detail:
- repository structure;
- Django project/apps structure;
- frontend structure;
- exact database fields;
- authentication approach;
- initial REST endpoints;
- first implementation order.

These decisions should be made interactively with the developer before implementation begins.
