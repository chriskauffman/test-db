# Task Plan: Issue #118 — Verify the database encryption key on open

## Goal

A wrong database encryption key must be refused at open instead of letting new secrets be written under it.

## Design

- Store `TestDB_EncryptedPickleColCheck` (a restricted key): a Fernet token of a fixed value, created with the key.
- On open with a key: decrypt the check value; mismatch raises `ValueError("wrong database encryption key")`.
- Databases without a check value (created before this change): authenticate against existing ciphertext first (as the legacy path already did), then backfill the check value. Without ciphertext there is nothing to verify, so the first key wins.

## Phases

- Discovery: password was never verified once salt and iterations existed. **complete**
- Implement: controller check + restricted key. **complete**
- Tests: wrong key refused, check created once, legacy backfill, legacy wrong key does not pin; decryption-error CLI tests rebuilt around a foreign-key row because wrong-key open is now refused. **complete**
- Verify: `make build`. **in progress**
