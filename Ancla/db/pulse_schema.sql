USE fintech

-- Loans table
CREATE TABLE IF NOT EXISTS loans (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    borrower_id BIGINT NOT NULL,
    principal DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Repayments table
CREATE TABLE IF NOT EXISTS repayments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    loan_id BIGINT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    repayment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loans(id)
);

-- Compliance Logs table
CREATE TABLE IF NOT EXISTS compliance_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
