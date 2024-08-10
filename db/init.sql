CREATE TABLE IF NOT EXISTS user_metrics (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    talked_time FLOAT CHECK (talked_time >= 0),
    microphone_used BOOLEAN,
    speaker_used BOOLEAN,
    voice_sentiment FLOAT CHECK (voice_sentiment >= 0 AND voice_sentiment <= 1),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, session_id)
);

CREATE INDEX idx_user_id ON user_metrics(user_id);
CREATE INDEX idx_session_id ON user_metrics(session_id);
