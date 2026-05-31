CREATE DATABASE IF NOT EXISTS fintech;
USE fintech;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    borrower_id INT NOT NULL,
    principal_amount DECIMAL(12,2) NOT NULL,
    status ENUM('open','closed','defaulted') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_loans_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS borrower_payback_status (
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
    
    CONSTRAINT fk_payback_loan FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    CONSTRAINT fk_payback_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);
