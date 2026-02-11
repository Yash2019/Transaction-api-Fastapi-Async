# Core Banking API

A transaction engine built with FastAPI that handles deposits, withdrawals, and transfers with race condition protection and a full audit trail.

## Tech Stack

- **FastAPI** — async REST API framework
- **SQLAlchemy** — async ORM with mapped column types
- **PostgreSQL** — relational database
- **Alembic** — database migrations
- **Pydantic** — request/response validation

## Features

- Account creation with optional initial deposit
- Deposit and withdrawal with balance validation
- Atomic transfers between accounts using database transactions
- Row-level locking (`SELECT FOR UPDATE`) to prevent race conditions
- Immutable transaction logs for audit compliance
- Transaction history query by account ID

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/create_account` | Create a new account |
| GET | `/api/get_one_account` | Get account details by ID |
| POST | `/api/deposit` | Deposit money into an account |
| POST | `/api/withdraw` | Withdraw money from an account |
| POST | `/api/transaction` | Transfer money between accounts |
| GET | `/api/transaction_history` | Get all transactions for an account |

## Screenshots

![Swagger Overview](screenshots/swagger_overview.png)

![Create Account](screenshots/create_account.png)

![Transaction](screenshots/transaction.png)

![Transaction History](screenshots/transaction_history.png)

## Technical Challenges Solved

### Atomicity
If a transfer crashes halfway, one account loses money and the other never receives it. Solved using database transactions — a single `db.commit()` ensures both balance changes and the transaction log are saved together, or none of them are.

### Concurrency
If a user sends money to two people simultaneously with insufficient balance for both, a race condition can cause negative balances. Solved using `SELECT FOR UPDATE` row locking to serialize concurrent access.

### Audit Trail
Every successful transfer creates an immutable [TransactionLog](cci:2://file:///home/yash/Desktop/CoreBanking/project/models.py:18:0-28:58) entry. Logs are never updated or deleted, ensuring a reliable record for compliance and dispute resolution.

## Setup

```bash
git clone <your-repo-url>
cd CoreBanking
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a [.env](cci:7://file:///home/yash/Desktop/CoreBanking/.env:0:0-0:0) file:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/your_db
```

Run migrations and start the server:
```bash
alembic upgrade head
uvicorn app:app --reload
```