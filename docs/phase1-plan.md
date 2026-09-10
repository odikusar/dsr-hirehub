# Phase 1 — План: Full-Stack Core

Цель: работающий full-stack без AI. Django + DRF + PostgreSQL, Next.js + TypeScript + Tailwind + shadcn/ui + TanStack Query + React Hook Form + Zod. Всё поднимается через Docker Compose.

Подход: walking skeleton, затем фичи вертикальными срезами — каждый срез работает end-to-end.

## Принятые решения

- **Кандидаты без аккаунтов (решение от 2026-09-07):** в Phase 1 регистрируются и логинятся только HR. Вакансии и форма отклика — публичные, отклик анонимный (контакты — поля в Application). Кандидатские аккаунты и «мои отклики» — кандидат в отдельную будущую фазу.
- **Auth:** JWT (SimpleJWT) в httpOnly cookies, только для HR. Эндпоинты: register / login / refresh / logout / me.
- **Структура Django:** доменные apps — `users`, `jobs`, `applications` (`resumes` появится в Phase 3).
- **CQRS:** в Phase 1 не вводим — классический DRF (ViewSet/serializers). CQRS-рефакторинг — начало Phase 2 («learn before abstracting»).
- **Django project:** называется `config`, лежит в `backend/`.

## Структура репозитория

```
dsr-hirehub/
├── README.md
├── docker-compose.yml
├── .env.example
├── docs/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/               # settings.py, urls.py, wsgi/asgi
│   └── apps/
│       ├── users/
│       ├── jobs/
│       └── applications/
└── frontend/
    ├── Dockerfile
    └── src/                  # Next.js App Router
```

## Модели

### User (кастомный, создать ДО первой миграции!) — в Phase 1 только HR
- `email` — unique, `USERNAME_FIELD`
- `first_name`, `last_name`
- `role` — TextChoices: `CANDIDATE` | `HR` (пока всегда HR, задел на будущее)
- `created_at`, `updated_at`

### Job
- `title`, `company_name`, `location` — CharField
- `description`, `requirements` — TextField (requirements пока просто текст)
- `employment_type` — choices: `FULL_TIME` | `PART_TIME` | `CONTRACT`
- `status` — choices: `DRAFT` | `OPEN` | `CLOSED` (default `DRAFT`)
- `created_by` — FK → User (HR)
- `created_at`, `updated_at`

### Application — анонимный отклик на вакансию
- `job` — FK → Job
- `applicant_name` — CharField
- `applicant_email` — EmailField
- `status` — choices: `APPLIED` | `REVIEWING` | `INTERVIEW` | `REJECTED` | `OFFER` (default `APPLIED`)
- `cover_note` — TextField
- `expected_salary` — DecimalField (null=True)
- `years_of_experience` — PositiveSmallIntegerField
- `created_at`, `updated_at`
- `UniqueConstraint(job, applicant_email)` — один отклик на вакансию с одного email

Создаётся публично (без логина) через форму отклика; HR читает отклики и меняет их статус.

## REST API

| Метод | URL | Кто | Что |
|---|---|---|---|
| POST | `/api/auth/register` | все | регистрация HR |
| POST | `/api/auth/login` | все | логин, токены в httpOnly cookies |
| POST | `/api/auth/refresh` | все | обновление access-токена |
| POST | `/api/auth/logout` | авторизованные | логаут |
| GET | `/api/auth/me` | авторизованные | текущий пользователь |
| GET | `/api/jobs/` | публичный | открытые вакансии; пагинация, поиск, фильтры |
| POST | `/api/jobs/` | HR | создать вакансию |
| GET | `/api/jobs/{id}/` | публичный | детали вакансии |
| PATCH/DELETE | `/api/jobs/{id}/` | HR-владелец | редактировать/удалить |
| GET | `/api/jobs/mine/` | HR | свои вакансии, включая DRAFT |
| POST | `/api/jobs/{id}/apply/` | публичный | анонимный отклик (имя, email, cover note…) |
| GET | `/api/jobs/{id}/applications/` | HR-владелец | отклики на вакансию |
| PATCH | `/api/applications/{id}/status/` | HR-владелец | сменить статус отклика |

## Структура фронтенда

```
frontend/               # без src/ — дефолт create-next-app 16
├── app/
│   ├── (public)/jobs, jobs/[id]        # список, детали, форма отклика — без логина
│   ├── (auth)/login, register          # только HR
│   └── (hr)/hr/jobs, hr/jobs/[id]/applicants
├── components/        # + ui/ от shadcn
├── lib/               # api-клиент, query-клиент, zod-схемы
└── hooks/             # useAuth, useJobs и т.п. на TanStack Query
```

## Чеклист

### Срез 0 — Скелет ✅
- [x] git init, репо на GitHub (odikusar/dsr-hirehub), SSH-ключ
- [x] backend: uv, Django 6.1, `GET /api/health/` → `{"status": "ok"}` (FBV)
- [x] frontend: create-next-app 16 (TS, Tailwind, App Router, без src/), главная дергает health (SPA-стиль, "use client"), CORS настроен
- [x] Docker Compose: postgres 17 + backend + frontend; Django на Postgres (psycopg3, .env + python-dotenv)
- [x] логирование: console + SQL_DEBUG-переключатель для запросов
- [x] скелет ходит end-to-end

### Срез 1 — Users + Auth (только HR)
- [x] app `users` (в `apps/`): кастомный User (email-логин, role), пересозданная БД, admin, суперюзер
- [x] `POST /api/auth/register/` (CreateAPIView) + тестовый `GET /api/auth/users/<pk>/` (ручной APIView; удалить позже)
- [ ] SimpleJWT: login / refresh / logout / me; auth-класс, читающий JWT из cookie
- [ ] фронт: login/register (RHF + Zod), api-клиент, `useAuth`, защищённые HR-роуты

### Срез 2 — Jobs
- [ ] модель Job, миграция, admin
- [ ] JobViewSet + router, permissions, `/mine/`, пагинация, поиск, фильтры
- [ ] фронт: список, детали, HR-кабинет (создание/редактирование/закрытие)

### Срез 3 — Applications
- [ ] модель Application + UniqueConstraint(job, applicant_email), миграция, admin
- [ ] API: публичный apply, отклики HR, смена статуса; permissions
- [ ] фронт: публичная форма отклика (имя, email, cover note…), отклики и смена статуса у HR

### Срез 4 — Полировка
- [ ] loading / error / empty states
- [ ] README с инструкцией запуска
- [ ] ручной прогон candidate- и HR-флоу, сверка с критериями успеха (спека, раздел 16)
