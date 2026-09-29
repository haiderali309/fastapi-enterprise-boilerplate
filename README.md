# FastAPI Enterprise Modular Architecture

A production-ready, highly structured FastAPI boilerplate that brings **Django-like modularity and organization** to FastAPI projects. This architecture is designed for scalability, maintainability, and enterprise-grade applications. It provides built-in solutions for routing, role-based access control, email handling, and logging.

---

## 🚀 Why Use This Architecture?

FastAPI is brilliant, but it leaves project structure up to the developer. This often leads to messy codebases as the project grows. This boilerplate solves that by giving you:

1. **Django-Like Apps:** Code is separated into distinct "modules" (e.g., `users`, `auth`). Each module manages its own models, schemas, repository, and routes.
2. **Advanced Role-Based Access Control (RBAC):** Built-in `SecureRouter` allows declarative permission management directly on route decorators.
3. **Robust Email Infrastructure:** Centralized service for sending HTML/text emails synchronously or via background tasks.
4. **Pre-configured Integrations:** SQLAlchemy, Alembic, standard Logging, and structured JSON API Responses are already set up for you.

---

## 📁 Complete Project Structure

```text
fast_api_structure/
├── alembic/                # Database migrations (auto-generated)
├── app/
│   ├── authorization/      # Core RBAC, SecureRouter, Policies & Permissions
│   │   ├── checker.py      # Dependency that verifies permissions
│   │   ├── permissions.py  # Centralized Enum of all permissions
│   │   ├── policy.py       # Maps Roles to their allowed Permissions
│   │   ├── roles.py        # Centralized Enum of User Roles
│   │   └── router.py       # Custom SecureRouter class
│   ├── core/               # App configuration, Middleware, Logging, Exceptions
│   ├── database/           # SQLAlchemy Base and Session management
│   ├── infrastructure/     # External services (Email, templates, Celery, Stripe etc)
│   ├── modules/            # Your Domain logic (Django-like apps)
│   │   ├── auth/           # Authentication endpoints & logic
│   │   ├── tokens/         # Token generation, storage & validation
│   │   └── users/          # Users management endpoints & logic
│   ├── shared/             # Reusable utilities (JWT, Validators, Dependencies)
│   └── main.py             # FastAPI application entry point
├── logs/                   # Application logs
├── requirements.txt        # Project dependencies
├── alembic.ini             # Alembic configuration
└── .env                    # Environment variables
```

---

## 🛡️ Deep Dive: SecureRouter & Authorization

One of the most powerful features of this boilerplate is the `SecureRouter`. It entirely abstracts away permission checking and JWT validation from your route logic.

### 🔄 The Request Flow

When a client hits a protected route, the request goes through an automated security pipeline:

```text
       Client Request
             |
             v
   Authorization: Bearer <JWT>
             |
             v
          FastAPI
             |
             v
       SecureRouter (Checks endpoint requirements)
             |
             v
    PermissionChecker (Dependency)
             |
             v
    get_current_user() (Decodes JWT, finds user)
             |
             v
      Check ROLE_POLICY (Does user role have permission?)
             |
      +------+------+
      |             |
   Allowed       Denied
      |             |
      v             v
  Endpoint      HTTP 403 (Forbidden)
```

### 🧑‍💻 How to use `SecureRouter`

Instead of using FastAPI's standard `APIRouter`, use our `SecureRouter`. You can enforce permissions just by passing them to the route decorator!

```python
# app/modules/users/router.py
from app.authorization.router import SecureRouter
from app.authorization.permissions import Permission

# Initialize SecureRouter
router = SecureRouter(prefix="/users", tags=["Users"])

# Protected Route - Requires VIEW_USER permission
@router.get("/", permissions=[Permission.VIEW_USER])
async def get_users():
    return {"users": ["User A", "User B"]}

# Multiple Permissions - User must have ALL of them
@router.delete("/{id}", permissions=[Permission.DELETE_USER, Permission.VIEW_USER])
async def delete_user(id: int):
    return {"message": "User deleted"}

# Public Route - Simply omit the `permissions` argument!
@router.get("/health")
async def health():
    return {"status": "Service is up and running"}
```

### 🔧 How to Customize Roles & Permissions

To add new features to your app, you will need to add new permissions. This is done centrally in the `app/authorization/` directory.

**1. Create the Permission (`permissions.py`)**
```python
class Permission(str, Enum):
    VIEW_USER = "view_user"
    DELETE_USER = "delete_user"
    # Add your new permission here:
    CREATE_PRODUCT = "create_product"
```

**2. Create or Identify the Role (`roles.py`)**
```python
class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    MANAGER = "MANAGER" # <--- Adding a new role
    USER = "USER"
```

**3. Map the Permission to the Role (`policy.py`)**
```python
ROLE_POLICY = {
    Role.SUPER_ADMIN: {
        Permission.VIEW_USER,
        Permission.DELETE_USER,
        Permission.CREATE_PRODUCT, # Admins can do this
    },
    Role.MANAGER: {
        Permission.VIEW_USER,
        Permission.CREATE_PRODUCT, # Managers can also do this
    }
}
```

That's it! Now just attach `permissions=[Permission.CREATE_PRODUCT]` to any route, and only Admins and Managers will be allowed to access it.

---

## 🧱 Deep Dive: Adding a New Module (Django-style App)

When you want to build a new feature (e.g., a "Products" API), you keep it isolated inside `app/modules/`.

1. Create a folder: `app/modules/products/`
2. Create the standard files inside it:
    - `models.py`: SQLAlchemy database models.
    - `schemas.py`: Pydantic validation models (In/Out).
    - `repository.py`: Direct database interactions (CRUD).
    - `service.py`: Business logic.
    - `router.py`: The `SecureRouter` defining API endpoints.
3. Link the router in `app/main.py`:
```python
from app.modules.products.router import router as products_router

app.include_router(products_router)
```

This keeps your codebase perfectly organized even if you have 50+ modules.

---

## 🔑 Deep Dive: Token Management System

This architecture includes a built-in, modular Token system (`app/modules/tokens/`) designed to handle lifecycle-critical security tokens out-of-the-box. It safely persists and validates tokens in the database rather than relying exclusively on stateless JWTs.

### Supported Token Types

The `TokenType` enum supports three primary security flows:

1. **Refresh Tokens (`REFRESH`)**: Long-lived tokens used to generate new short-lived access JWTs without forcing the user to log in again.
2. **Email Verification (`EMAIL_VERIFY`)**: Short-lived tokens generated when a user signs up, sent via the Email Infrastructure to verify their email address.
3. **Password Reset (`PASSWORD_RESET`)**: Highly sensitive, short-lived tokens generated when a user requests a password reset.

### Security Configurations

Token lifespans are globally configured via `.env` (and parsed in `app/core/config.py`):

```env
ACCESS_TOKEN_EXPIRY_MINUTE=15
REFRESH_TOKEN_EXPIRY_DAYS=30
EMAIL_VERIFY_TOKEN_EXPIRY_MINUTE=15
PASSWORD_RESET_EXPIRY_MINUTE=10
```

By decoupling tokens into their own domain module (`app/modules/tokens`), we prevent the `users` and `auth` modules from becoming bloated, adhering strictly to the Single Responsibility Principle!

---

## 📧 Email Infrastructure

This boilerplate ships with a centralized email sending system located in `app/infrastructure/email/`. It uses Jinja2 templates (located in the `templates/` folder) and supports two types of email delivery.

### 1. Direct Sending (Critical Emails)
Use direct sending when the API process **must** wait to ensure the email is delivered (e.g., OTP Verification, Password Resets). If it fails, the API throws an error.

```python
from app.infrastructure.email.service import send_mail

# Inside an async route or service:
await send_mail(
    subject="Your OTP Code",
    message="Your OTP is 123456",
    recipient_list=["user@test.com"],
    template_name="otp.html",      # Uses app/infrastructure/email/templates/otp.html
    context={"otp": "123456"}      # Variables passed to the HTML template
)
```

### 2. Background Sending (Non-Critical Emails)
Use background tasks for emails where the user shouldn't have to wait for SMTP servers (e.g., Welcome Emails, Marketing, Notifications).

```python
from fastapi import BackgroundTasks
from app.infrastructure.email.background_service import send_mail_background

@router.post("/welcome")
async def welcome_email(background_tasks: BackgroundTasks):
    
    send_mail_background(
        background_tasks,          # Pass the BackgroundTasks object
        subject="Welcome Aboard!",
        message="Welcome to our platform",
        recipient_list=["user@test.com"],
        template_name="welcome.html",
        context={"name": "Alice"}
    )
    
    # Returns immediately, email sends in the background
    return {"message": "Welcome email scheduled"}
```

---

## 📝 Centralized Logging

Forget `print()`. Use the pre-configured global logger to ensure consistent, timestamped log formats.

```python
from app.core.logging import logger

logger.info("New user registered successfully.")
logger.warning("User attempted login with wrong password.")
logger.error("Failed to connect to third-party API.")
logger.exception("An unexpected crash occurred!") # Automatically includes traceback
```

---

## 🛠️ Installation & Setup

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd fast_api_structure/fast_api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
APP_NAME=YOUR_APP_NAME
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000
ENABLE_HTTPS_REDIRECT=True

DATABASE_URL=postgresql+asyncpg://YOUR DB URL
BASE_URL=https://localhost:8000
FRONTEND_URL=http://localhost:3000

JWT_SECRET=YOU KEY
JWT_ALGO=HS256
ACCESS_TOKEN_EXPIRY_MINUTE=15
REFRESH_TOKEN_EXPIRY_DAYS=30
EMAIL_VERIFY_TOKEN_EXPIRY_MINUTE=15
PASSWORD_RESET_EXPIRY_MINUTE=10

MAIL_USERNAME=YOUR USER NAME
MAIL_PASSWORD=YOUR PASSWORD
MAIL_FROM=YOUR FROM EMAIL
MAIL_PORT=YOUR PORT
MAIL_SERVER=YOUR SMTP SERVER
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
```

### 3. Run Database Migrations

```bash
alembic upgrade head
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 🤝 Contributing

This project is open-source and welcomes contributions!
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - feel free to use it for your own projects!
