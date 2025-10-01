# Implementation Log

## 1. Language and Framework
- Chosen Python + FastAPI for rapid, readable REST development, strong typing with Pydantic, and excellent testability.

## 2. Project Layout
- Created layered structure: `api` (routers), `services` (business rules), `repositories` (storage), `models` (schemas), `utils` (time).
- This separation improves maintainability and testability.

## 3. Data Model
- `Order`, `OrderCreate`, `OrderUpdate` with `OrderType`, `MarketType` enums.
- `productType` fixed to `ELECTRICITY` and validated.
- `quantity` validated positive.

## 4. Business Rules
- Quarter-hour alignment utility in `app/utils/time.py`.
- Create: align provided `start`; default window to 15 minutes.
- Update: if `end` in past, auto-adjust to `now`..`now+15m`.

## 5. API Endpoints
- Implemented `/api/v1/orders` CRUD with FastAPI router.
- Response models ensure contract consistency.

## 6. Repository
- `InMemoryOrderRepository` for development and tests; interface allows swapping for PostgreSQL/Mongo/Redis later.

## 7. Tests
- Unit tests for time alignment, service rules, and API happy path using `pytest` and `fastapi.testclient`.

## 8. Containerization
- Dockerfile and docker-compose for local running and portability.

## 9. Configurability
- Duration (15 min) centralized in service; can be made configurable via env in future.

## 10. Next Steps
- Add persistent repository (PostgreSQL or MongoDB) and config.
- Add logging/middleware and observability.
- CI workflow and linting (ruff) integration.
