-- Step 1. 데이터베이스 스키마
--   먼저 데이터베이스 스키마를 생성한다.

DROP TABLE IF EXISTS entries;

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title STRING NOT NULL,
    text STRING NOT NULL
);
