# Database Conventions

Working assumptions: PostgreSQL, SQLAlchemy 2.0 ORM, Alembic migrations. Adjust if the stack changes — the rules survive the swap.

- **Schema changes happen only through Alembic migrations.** Manual DDL on any shared database (including staging) is forbidden; the migration is the record.
- Every migration is generated from model changes (`alembic revision --autogenerate -m "conventional commit style message"`) and then **hand-reviewed**: autogenerate misses renames and data backfills.
- Migrations run in CI against a disposable DB so they can't rot; destructive changes (drop/rename) ship as two steps when data is at risk (add → backfill → remove).
- Naming: `snake_case` tables (plural), explicit constraint names, `id UUID` primary keys, `created_at`/`updated_at` timestamps on every table.
- Every FK gets an index; queries in reviews are checked for N+1 (`selectinload`, not lazy loops).
- One connection pool per process, sized from the environment; transactions are short and explicit.
- Seed data lives in a separate idempotent script, never in migrations.
- Backups: point-in-time recovery enabled before the database holds anything real; restore is tested, not assumed.
