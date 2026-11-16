# Findings & Decisions

## Requirements
- Review all `bulk-add` CLI commands and their shared database path.
- Answer specifically whether more indexes improve bulk-add performance.
- Preserve scope: recommendations only unless a concrete code change is requested.

## Research Findings
- Every current bulk-add command constructs one SQLObject per row inside one SQLObject transaction and commits once at the end. The transaction optimization is already present.
- Current bulk-add commands cover organization, person, job, person/organization address, person/organization bank account, and person debit card. Key-value commands do not expose bulk-add.
- The schema already creates unique indexes for gID/unique columns and all declared composite `DatabaseIndex` constraints (bank accounts, debit cards, key/value ownership, and job employee/organization).
- Address creation generates fake address fields and performs a `selectBy(...).getOne()` uniqueness check when defaults are used.
- Bank-account creation generates values and performs a `selectBy(routingNumber, accountNumber)` uniqueness check when defaults are used.
- Debit-card creation performs a `selectBy(cardNumber)` uniqueness check when defaults are used.
- Those uniqueness checks occur during each object construction and are likely a larger avoidable cost than missing indexes for inserts.
- Foreign-key columns used by relationship lists and cascaded deletes are not separately indexed in the generated SQLite schema. Such indexes help reads/deletes, but add write maintenance cost and do not generally make inserting a new child row faster.
- Local SQLite benchmark, one run per case, 5,000 rows: address/bank/card bulk-add took about 7.1s without lookup indexes. Adding indexes matching the listener probes reduced those runs to about 6.3–6.6s. This is directional only; process startup and Faker/SQLObject work remain significant.
- The listener probe indexes would be `person_address(street, locality, region, postal_code)`, `person_bank_account(routing_number, account_number)`, and `person_debit_card(card_number)` (with equivalent organization tables). They are useful for the current generation checks, but they are not relationship indexes and should not be added solely because a bulk insert exists.
- The existing `(person_id, routing_number, account_number)` and `(person_id, card_number)` indexes can support owner-prefix queries, but not the listener's lookup without `person_id` as a predicate. The same left-prefix rule applies to other composite indexes.
- `job(employee_id, organization_id)` does not support organization-only or person-only relationship lookups because those columns are not the leading key; this is a read/delete concern, not an insert-throughput fix.
- The largest structural write optimization would be a dedicated bulk insert path that batches rows (or uses database-native bulk loading), but it must reproduce SQLObject event defaults, generated IDs, uniqueness behavior, and cross-database SQL. That is materially larger and riskier than adding indexes.
- Faker collision checks currently issue a database query inside the generation loop for person names, phone numbers, SSNs, organization names/EINs, addresses, bank-account numbers, and debit-card numbers. Email generation can issue several database lookups per row.
- `fake.unique` can avoid those per-candidate database reads by tracking values in memory, but its state is local to one Faker instance and does not know about rows already in the database. It also raises when its finite value space is exhausted.
- The safest bulk-only optimization is to load the relevant existing values once into Python sets, generate candidates with Faker (optionally through `fake.unique`), add accepted candidates to the sets, and retain database unique constraints as the final protection. This trades repeated queries for bounded memory and one initial query per field.
- Removing checks entirely is safe only where a database uniqueness constraint exists and the insertion path can retry correctly. PostgreSQL transactions need savepoints after a uniqueness error; manual retry loops are not a drop-in replacement for the current pre-checks.
- Several current uniqueness policies are not represented by constraints: person names/phone, address combinations, and the global bank/card lookup rules. Those must not silently switch to database-error handling without deciding whether the policy should change.
- Implemented bulk-only caching: each bulk transaction loads each model's existing rows once, tracks generated values in Python sets, and clears the cache on commit or rollback. Non-bulk handlers retain their original database checks.
- All existing CLI bulk-add commands now enable the cache through a shared transaction context, including auto-created dependents.
- Local SQLite 5,000-row timings after the change were approximately 3.14s for persons, 3.29s for addresses, and 3.31s for bank accounts; earlier unoptimized 5,000-row address/bank/card timings were approximately 7.1s. These are directional local measurements.
- Review follow-up: the cache no longer retains full SQLObject rows; it builds and retains only the needed field-value set. Bulk-add's single-writer assumption is documented because cross-engine locking or new uniqueness constraints would change the schema/transaction design.
- Review follow-up: `tests/test_bulk.py` now covers all specialized bulk handlers and fails if they call their old per-row lookup methods.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Benchmark representative SQLite bulk-add paths before suggesting changes | SQLite is available locally and the project has a required build/test command; direct measurements can distinguish Python/default-generation cost from SQL/index cost. |
| Separate write-path indexes from read-path indexes | An index can accelerate relationship lookup/cascade work while slowing every insert/update and increasing storage. |
| Do not recommend blanket additional indexes for bulk-add | Existing unique/index constraints already protect inserts; indexes only help the specific unindexed existence probes or downstream reads. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Planning initializer command initially failed due to shell variable expansion | Re-ran it using the absolute installed script path. |

## Resources
- `src/test_db/cli/_*.py` bulk-add commands
- `src/test_db/_schemas/v2.sql`
- model modules under `src/test_db/_*.py`
