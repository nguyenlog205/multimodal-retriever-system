CREATE TABLE multimedia_objects (
    -- Unique identifier for each multimedia object
    id UUID PRIMARY KEY,
    content_type VARCHAR NOT NULL,
    raw_content_url VARCHAR,
    embedding_vector VECTOR(768),
    upload_timestamp TIMESTAMP,
    author_id UUID
);

CREATE TABLE multimedia_metadata (
    multimedia_id UUID PRIMARY KEY REFERENCES multimedia_objects(id) ON DELETE CASCADE,

    -- Metadata
    title VARCHAR,
    description TEXT,
    language VARCHAR(10),
    categories VARCHAR[],
    tags VARCHAR[],
    source VARCHAR,
    duration_seconds FLOAT,
    resolution VARCHAR,
    asr_transcript TEXT,
    detected_objects JSONB,
    user_annotations TEXT,
    popularity_score FLOAT,
    location_metadata JSONB,
    sentiment_score FLOAT
);
