## Goal

Reuse the same Supabase project as Mansa Capital while keeping Accesso Ancla fully isolated. All Ancla data moves into a new `ancla` Postgres schema (tables, enums, functions, triggers, RLS). The `public` schema is left untouched so Mansa's KYC/Stripe tables can live there safely.

Auth (`auth.users`) is shared at the Postgres level (Supabase only allows one auth schema per project), but users are treated as fully separate per app: an Ancla signup only creates a row in `ancla.profiles`, never touches anything Mansa owns, and vice versa.

## Database migration

Single migration that:

1. `CREATE SCHEMA ancla;`
2. Recreate enums in `ancla` (`app_role`, `loan_status`, `collateral_type`, `verification_status`, `repayment_status`, `repayment_source`, `transaction_type`, `transaction_status`, `notification_type`, `notification_status`, `payback_status_kind`, `risk_flag`).
3. `ALTER TABLE public.X SET SCHEMA ancla` for: `profiles`, `user_roles`, `loans`, `collateral`, `loan_documents`, `repayments`, `transactions`, `borrower_payback_status`, `payback_analysis_tally`, `notifications`.
4. Recreate `has_role`, `handle_new_user`, `set_updated_at` inside `ancla` (SECURITY DEFINER, `search_path = ancla`).
5. Re-point the `on_auth_user_created` trigger on `auth.users` to `ancla.handle_new_user` so signups only land in `ancla.profiles` (Mansa is expected to do the equivalent in its own schema/trigger; we will not touch any Mansa trigger).
6. RLS + GRANTs re-applied in `ancla` (same policies as today, just qualified).
7. Expose schema to the Data API:
   ```sql
   ALTER ROLE authenticator SET pgrst.db_schemas = 'public,ancla,graphql_public';
   NOTIFY pgrst, 'reload config';
   ```
8. Storage: create new bucket `ancla-collateral-docs` with the same per-user-folder policies, then drop the old `collateral-docs` bucket (no production data yet).

## App code changes

- `src/integrations/supabase/client.ts` is auto-generated and read-only. Instead of editing it, use the per-query helper `supabase.schema('ancla').from('loans')` in every data-access site. Auth calls (`supabase.auth.*`) remain unchanged.
- Add a tiny wrapper `src/integrations/ancla-db.ts` that exports `const db = supabase.schema('ancla')` so components do `db.from('loans')` and we have one place to swap the schema name later.
- Update all current call sites:
  - `src/components/borrower/apply-form.tsx` (loans, collateral, loan_documents inserts + storage upload bucket name)
  - `src/routes/status.tsx` (loans, loan_documents reads + signed-URL bucket name)
  - `src/hooks/use-auth.tsx` — no change (auth only)
- Storage bucket name constant: replace `'collateral-docs'` with `'ancla-collateral-docs'` in the two files above.
- After the migration runs, Supabase regenerates `src/integrations/supabase/types.ts` to include the `ancla` schema; cross-schema typing then works via `supabase.schema('ancla')`.

## Out of scope

- Anything inside the `public` schema (Mansa's tables stay as-is).
- Mansa's own triggers, RLS, or `handle_new_user` — not touched.
- Data migration: there is no production Ancla data yet, so `ALTER TABLE ... SET SCHEMA` is safe and preserves any test rows.

## Execution order

1. Run the migration (renames + bucket + PostgREST reload).
2. Wait for `types.ts` to regenerate.
3. Add `ancla-db.ts` wrapper and update the 2 component files + bucket name.
4. Smoke test: sign up → apply form submits → status page lists the loan + signed doc URL works.

## Coupling contract (Ancla ↔ KYC, shared Supabase project)

Both apps share `auth.users`. Everything else is isolated by schema: Ancla owns `ancla.*`, KYC owns `public.*`. No table-name collisions exist today.

### Hard rules

1. **Namespaced auth triggers.** Ancla's trigger on `auth.users` is `on_auth_user_created_ancla` → `ancla.handle_new_user()`. KYC must use its own distinct trigger name (e.g. `on_auth_user_created_kyc`). Never share a trigger.
2. **Idempotent handlers.** Every `auth.users` handler uses `ON CONFLICT (...) DO NOTHING`. A single signup fires every trigger; each app tolerates its row already existing.
3. **Schema isolation in handlers.** `ancla.handle_new_user` has `SET search_path = ancla, public` and only writes to `ancla.*`. It must never `INSERT INTO public.*`. KYC's handler must never touch `ancla.*`.
4. **Per-schema enums.** `ancla.app_role` and `public.app_role` stay independent. Same for status enums. Do not consolidate.
5. **Storage buckets are per-app.** Ancla uses `ancla-collateral-docs`. KYC uses its own buckets. No cross-bucket policies.
6. **No cross-schema FKs.** Ancla tables never reference `public.*` and vice versa. Only `auth.users(id)` is shared.

### Documented enum mappings (analytics parity only — do not enforce in DB)

Loan status: `ancla.loan_status` (`open`, `funded`, `repaid`, ...) ↔ KYC `public.loan_requests.status` (`pending`, `funded`, `repaid`, ...). Map at the reporting layer.

Role: `ancla.app_role` (`borrower`, `lender`, `admin`) ↔ KYC `public.app_role` (project-defined). Map at the reporting layer.

### Do-not-touch list

- `public.*` tables, functions, triggers, enums, policies (owned by KYC).
- Any trigger on `auth.users` not named `on_auth_user_created_ancla`.
- `auth`, `storage`, `realtime`, `supabase_functions`, `vault` schemas.

### Verification

- `pg_trigger` on `auth.users` confirmed: `on_auth_user_created_ancla` → `ancla.handle_new_user()` (2026-06-02).
- `ancla.handle_new_user` uses `ON CONFLICT (id) DO NOTHING` and `search_path = ancla, public`.
- `ancla.assert_isolation()` runs the trigger-name + schema-boundary checks; re-run after any migration that touches `ancla.handle_new_user`, `auth.users` triggers, or ancla helper functions.
- `ancla.handle_new_user`, `ancla.has_role`, and `ancla.set_updated_at` now have `search_path = ancla` (no `public`), so an unqualified `public.*` reference fails at runtime.

## Enum mapping rules (analytics parity)

Enums are intentionally **not** shared between Ancla and KYC. Each app evolves
its own enum; the reporting layer (BI view, dbt model, notebook) is responsible
for mapping. These tables are the contract — update them whenever either app
adds, renames, or removes a value, in the SAME migration that changes the enum.

### `app_role`

| Ancla (`ancla.app_role`) | KYC (`public.app_role`) | Canonical analytics role | Notes |
| --- | --- | --- | --- |
| `borrower` | `borrower` | `borrower` | 1:1 |
| `lender`   | `investor` | `lender`   | KYC may call this `investor`; map to `lender` in reports. |
| `admin`    | `admin`    | `admin`    | 1:1; never grant cross-app. A row in `ancla.user_roles` does NOT imply admin in KYC, and vice versa. |

Rules:
1. Neither app may add a value without updating this table in the same PR.
2. Roles are per-schema: `has_role(uid, 'admin')` checks ONLY that schema's `user_roles`.
3. Cross-app admin must be granted explicitly in both `ancla.user_roles` and `public.<kyc_user_roles>`.

### Loan status

| Ancla (`ancla.loan_status`) | KYC (`public.loan_requests.status`) | Canonical analytics status | Notes |
| --- | --- | --- | --- |
| `open`           | `pending`        | `pending`   | Submitted, not yet funded. |
| `funded`         | `funded`         | `funded`    | 1:1. |
| `repaid`         | `repaid`         | `repaid`    | 1:1. |
| `defaulted`      | `defaulted`      | `defaulted` | 1:1 if both apps use it. |
| `cancelled`      | `cancelled`      | `cancelled` | 1:1. |
| (Ancla-only) `draft`  | —          | `pending`   | Pre-submission; roll up into `pending` for cross-app dashboards. |
| (Ancla-only) `active` | `funded`   | `funded`    | Funded + currently being serviced; roll up into `funded`. |
| — | (KYC-only) `rejected` | `cancelled` | Ancla has no equivalent; treat as `cancelled` in joined reports. |

Rules:
1. Do NOT add a CHECK constraint, FK, or trigger that references the other app's enum values.
2. Do NOT consolidate the two enums into a shared one — keeps deploys independent.
3. The mapping lives ONLY at the reporting layer (BI view named `analytics.loan_status_map`). Application code never translates between the two enums.
4. When either app adds a new status, append a row to this table in the same migration and update the BI mapping view before the next analytics run.

### Where the mapping is implemented

- Single source of truth: this document.
- Reporting layer: a `analytics` schema view (per-deployment) that UNIONs `ancla.loans` and `public.loan_requests` and projects both into the canonical columns above.
- No runtime cross-schema joins in app code — only the BI layer reads both schemas.

### Runtime enforcement

`SELECT ancla.assert_enum_mappings();` — raises if `ancla.app_role` or
`ancla.loan_status` drifts from the values listed above. Call it at the top
of every cross-app analytics job, view refresh, or scheduled report BEFORE
reading from both schemas. If it raises: update the tables above AND the
expected arrays inside `ancla.assert_enum_mappings()` in the same migration.