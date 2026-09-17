CREATE DATABASE IF NOT EXISTS retail_feedback_db;

USE retail_feedback_db;


-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- FEEDBACK TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,

    unique_id VARCHAR(50) NOT NULL UNIQUE,

    category VARCHAR(100) NOT NULL,

    review_header VARCHAR(500),

    review_text TEXT NOT NULL,

    rating INT NOT NULL,

    own_rating VARCHAR(20) NULL,

    predicted_sentiment VARCHAR(20) NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_rating
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT chk_sentiment
        CHECK (own_rating IS NULL OR own_rating IN ('Positive', 'Neutral', 'Negative')),

    CONSTRAINT chk_predicted_sentiment
        CHECK (
            predicted_sentiment IS NULL
            OR predicted_sentiment IN ('Positive', 'Neutral', 'Negative')
        )
);


-- ==========================================
-- INDEXES
-- ==========================================

CREATE INDEX idx_feedback_category
ON feedback(category);

CREATE INDEX idx_feedback_rating
ON feedback(rating);

CREATE INDEX idx_feedback_sentiment
ON feedback(own_rating);

CREATE INDEX idx_feedback_predicted_sentiment
ON feedback(predicted_sentiment);
