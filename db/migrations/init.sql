-- Core demo tables used by API endpoints
create table if not exists public.borrowers (
	id bigint primary key,
	full_name text not null,
	email text unique,
	created_at timestamptz not null default now()
);

create table if not exists public.loans (
	id bigint primary key,
	borrower_id bigint references public.borrowers(id),
	amount numeric(12, 2) not null,
	status text not null,
	created_at timestamptz not null default now()
);

create table if not exists public.repayments (
	id bigint primary key,
	loan_id bigint not null references public.loans(id),
	due_date date not null,
	amount_due numeric(12, 2) not null,
	status text not null,
	created_at timestamptz not null default now()
);

create table if not exists public.notifications (
	id bigint primary key,
	borrower_id bigint references public.borrowers(id),
	type text,
	message text,
	timestamp timestamptz not null default now(),
	created_at timestamptz not null default now()
);

-- Borrower seed data
insert into public.borrowers (id, full_name, email)
values
	(1, 'Alicia Carter', 'alicia.carter@example.com'),
	(2, 'Marcus Young', 'marcus.young@example.com'),
	(3, 'Nia Evans', 'nia.evans@example.com')
on conflict (id) do update
set
	full_name = excluded.full_name,
	email = excluded.email;

-- Loan seed data (includes loan_id=1 for /repayments?loan_id=1)
insert into public.loans (id, borrower_id, amount, status)
values
	(1, 1, 500.00, 'pending'),
	(2, 2, 1200.00, 'approved'),
	(3, 3, 800.00, 'pending')
on conflict (id) do update
set
	borrower_id = excluded.borrower_id,
	amount = excluded.amount,
	status = excluded.status;

-- Repayment seed data tied to seeded loans
insert into public.repayments (id, loan_id, due_date, amount_due, status)
values
	(1001, 1, current_date + 7, 110.00, 'Pending'),
	(1002, 1, current_date + 37, 110.00, 'Pending'),
	(1003, 2, current_date - 10, 200.00, 'Paid'),
	(1004, 3, current_date + 14, 150.00, 'Pending')
on conflict (id) do update
set
	loan_id = excluded.loan_id,
	due_date = excluded.due_date,
	amount_due = excluded.amount_due,
	status = excluded.status;

-- Borrower notification seed data
insert into public.notifications (id, borrower_id, type, message, timestamp)
values
	(2001, 1, 'Payment Reminder', 'Your next repayment of $110.00 is due in 7 days.', now()),
	(2002, 2, 'Loan Update', 'Your loan is approved and funds are scheduled for release.', now()),
	(2003, 3, 'Payment Reminder', 'Repayment schedule is active. First due date is in 14 days.', now())
on conflict (id) do update
set
	borrower_id = excluded.borrower_id,
	type = excluded.type,
	message = excluded.message,
	timestamp = excluded.timestamp;

