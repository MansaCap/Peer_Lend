CREATE TABLE borrower_payback_status (
	status_id          INT AUTO_INCREMENT PRIMARY KEY,
	loan_id            INT NOT NULL,
	borrower_id        INT NOT NULL,
	current_status     ENUM('on_time', 'late', 'defaulted', 'completed') NOT NULL,
	last_payment_date  DATETIME,
	next_due_date      DATETIME,
	days_past_due      INT DEFAULT 0,
	total_paid         DECIMAL(12,2) DEFAULT 0.00,
	outstanding_amount DECIMAL(12,2) DEFAULT 0.00,
	risk_flag          ENUM('low', 'medium', 'high') DEFAULT 'low',
	updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

	KEY idx_payback_loan (loan_id),
	KEY idx_payback_borrower (borrower_id),
	CONSTRAINT fk_payback_loan FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
	CONSTRAINT fk_payback_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);

CREATE TABLE payback_analysis_tally (
	tally_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
	analyzed_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	total_loans       INT NOT NULL,
	healthy_count     INT NOT NULL DEFAULT 0,
	watch_count       INT NOT NULL DEFAULT 0,
	critical_count    INT NOT NULL DEFAULT 0,
	completed_count   INT NOT NULL DEFAULT 0,
	not_found_count   INT NOT NULL DEFAULT 0
);
