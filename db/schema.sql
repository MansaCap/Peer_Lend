create table if not exists public.borrowers (
	id bigint primary key,
	full_name text not null,
	email text unique,
	created_at timestamptz not null default now()
);

create table if not exists public.loans (
	id bigint primary key,
	borrower_id bigint references public.borrowers(id),
	principal numeric(12, 2) not null,
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

