-- 프로젝트 루트나 app/ 내부
CREATE TABLE IF NOT EXISTS info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_mbti TEXT,
    user_gender TEXT,
    partner_name TEXT NOT NULL,
    partner_mbti TEXT,
    partner_gender TEXT,
    file_name TEXT
);
