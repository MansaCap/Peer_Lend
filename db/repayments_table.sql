CREATE TABLE fintech.repayments (
    repayment_id     INT AUTO_INCREMENT PRIMARY KEY,
    loan_id          INT NOT NULL,
    borrower_id      INT NOT NULL,
    amount           DECIMAL(12,2) NOT NULL,
    source           ENUM('bank_transfer','digital_wallet','payroll_deduction','gig_share') NOT NULL,
    payment_date     DATETIME NOT NULL,
    status           ENUM('pending','completed','failed') DEFAULT 'pending',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_repayment_loan FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    CONSTRAINT fk_repayment_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);
