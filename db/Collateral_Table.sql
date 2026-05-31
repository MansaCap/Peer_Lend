CREATE TABLE fintech.collateral (
    collateral_id        INT AUTO_INCREMENT PRIMARY KEY,
    borrower_id          INT NOT NULL,
    type                 ENUM('digital_asset','payroll_deduction','gig_share','other') NOT NULL,
    value                DECIMAL(12,2) NOT NULL,
    verification_status  ENUM('pending','verified','rejected') DEFAULT 'pending',
    escrow_contract_addr VARCHAR(255),
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_collateral_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
);
