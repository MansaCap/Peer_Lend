CREATE TABLE payback_analysis_tally (
    tally_id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    loan_id             BIGINT NOT NULL,
    borrower_id         BIGINT NOT NULL,

    total_disbursed     DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    total_repaid        DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    outstanding_balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,

    num_payments_made   INT NOT NULL DEFAULT 0,
    num_payments_due    INT NOT NULL DEFAULT 0,

    dpd                 INT NOT NULL DEFAULT 0,   -- Days past due
    risk_grade          VARCHAR(10),              -- A, B, C, D, High Risk

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_tally_loan FOREIGN KEY (loan_id)
        REFERENCES loans(loan_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tally_borrower FOREIGN KEY (borrower_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    INDEX idx_tally_loan (loan_id),
    INDEX idx_tally_borrower (borrower_id),
    INDEX idx_tally_risk (risk_grade)
);
