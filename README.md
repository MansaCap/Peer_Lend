# Peer_Lend Project

## Current Repository Layout

The runnable app currently lives under `github/PeerLending`.

## Local MySQL Setup (Fintech schema)

1. Copy `.env.example` to `.env` at repository root.
2. Update the MySQL values in `.env`.
3. Apply schema and table scripts:

```powershell
python scripts/apply_fintech_schema.py
```

4. Verify tables in Workbench under schema `fintech`.

## Verify Local and GitHub Sync

Use these commands from repo root:

```powershell
git status --short --branch
git add -A
git commit -m "Sync local changes"
git push origin main
```

If GitHub Desktop fails to commit, use the terminal commands above to surface the exact error.
