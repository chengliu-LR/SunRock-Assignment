Electricity Orders Service (FastAPI)

Quickstart
- Install: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
- Run: uvicorn app.main:app --reload
- API: http://localhost:8000/api/v1/orders
- Docs: http://localhost:8000/docs
- Tests: pytest

Detailed Run Instructions
- Create and activate virtual environment (only tested on macOS, but should also work on other Unix-like systems):
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
- Install dependencies:
  - `pip install -r requirements.txt`
- Start the API:
  - navigate to the project root
  - run `./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000`

Health Check
- Verify server is up:
  - curl -s http://127.0.0.1:8000/health
  - Expected: {"status":"ok"}

Example API Calls (CRUD)
- Create order (Intra-Day BUY, quantity 2.5):
  - curl -s -X POST http://127.0.0.1:8000/api/v1/orders/ \
    -H 'Content-Type: application/json' \
    -d '{"orderType":"BUY","type":"Intra-Day","quantity":2.5}'
- List orders:
  - curl -s http://127.0.0.1:8000/api/v1/orders/
- Get by id (replace {id}):
  - curl -s http://127.0.0.1:8000/api/v1/orders/{id}
- Update order quantity to 3.0:
  - curl -s -X PUT http://127.0.0.1:8000/api/v1/orders/{id} \
    -H 'Content-Type: application/json' \
    -d '{"quantity":3.0}'
- Delete order:
  - curl -s -X DELETE http://127.0.0.1:8000/api/v1/orders/{id} -o /dev/null -w "%{http_code}\n"

Notes
- Business rules:
  - Start time aligns to 00/15/30/45 minutes.
  - Update: if provided end is in the past, system sets start=now, end=now+15m.
- Default productType is ELECTRICITY and validated; quantity must be positive.

Architecture
- FastAPI app with layers: API -> Service -> Repository -> Models/Utils.
- In-memory repository by default; swap with DB-specific repo as needed.

Project Structure
```
SunRock Assignment/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── orders.py         # Order API endpoints
│   │       └── routes.py         # Route definitions
│   ├── core/                     # Core application logic
│   │   └── __init__.py
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── orders.py             # Order data models
│   ├── repositories/             # Data access layer
│   │   ├── __init__.py
│   │   └── orders.py             # Order repository implementation
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   └── orders.py             # Order business logic
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── time.py               # Time-related utilities
├── tests/                        # Test suite
│   ├── test_api.py               # API endpoint tests
│   ├── test_service.py           # Service layer tests
│   └── test_time_utils.py        # Utility function tests
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── IMPLEMENTATION_LOG.md         # Development log
└── .gitignore                    # Git ignore rules
```

Layer Responsibilities:
- **API Layer** (`app/api/`): HTTP request/response handling, input validation
- **Service Layer** (`app/services/`): Business logic, order processing rules
- **Repository Layer** (`app/repositories/`): Data persistence, CRUD operations
- **Models** (`app/models/`): Data structures and validation schemas
- **Utils** (`app/utils/`): Shared utility functions (time alignment, etc.)

Business Rules
- Start aligned to quarter-hour (00/15/30/45).
- Update: if end < now, set start=now, end=now+15m.
