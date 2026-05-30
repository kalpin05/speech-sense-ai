-- Run these commands in pgAdmin Query Tool to create the tables natively.
-- Make sure you have created a database first (e.g., "speech_therapy_db") and are connected to it.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS therapy_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expected_text TEXT NOT NULL,
    transcription TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    accuracy_score FLOAT NOT NULL,
    fluency_score VARCHAR(50) NOT NULL,
    feedback TEXT NOT NULL,
    audio_file_path VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    language VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'beginner',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
