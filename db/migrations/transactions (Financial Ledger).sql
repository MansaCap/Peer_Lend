CREATE TABLE transactions (
    transaction_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    loan_id             BIGINT NOT NULL,
    borrower_id         BIGINT NOT NULL,

    txn_type            ENUM('DISBURSEMENT','REPAYMENT','FEE','ADJUSTMENT') NOT NULL,
    amount              DECIMAL(12,2) NOT NULL,
    currency            VARCHAR(10) DEFAULT 'COP',

    txn_status          ENUM('PENDING','COMPLETED','FAILED','REVERSED') DEFAULT 'PENDING',
    txn_reference       VARCHAR(255),   -- External processor ref (Stripe, Wompi, etc.)

    txn_timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_txn_loan FOREIGN KEY (loan_id)
        REFERENCES loans(loan_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_txn_borrower FOREIGN KEY (borrower_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    INDEX idx_txn_loan (loan_id),
    INDEX idx_txn_borrower (borrower_id),
    INDEX idx_txn_type (txn_type),
    INDEX idx_txn_status (txn_status),
    INDEX idx_txn_timestamp (txn_timestamp)
);
