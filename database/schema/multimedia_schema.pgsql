--
-- Tên file: create_content_table.pgsql
-- Mô tả: Tạo bảng 'contents' để lưu trữ siêu dữ liệu và vector embedding.
--

--
-- Extension `pgvector` phải được cài đặt và kích hoạt để sử dụng kiểu dữ liệu `vector`.
-- Để cài đặt, bạn cần chạy lệnh:
-- CREATE EXTENSION IF NOT EXISTS vector;
--

-- Xóa bảng cũ nếu tồn tại
DROP TABLE IF EXISTS contents;

-- Tạo bảng `contents`
CREATE TABLE contents (
    -- ID là khóa chính, tự động tăng, không được để trống
    id SERIAL PRIMARY KEY,
    
    -- Tiêu đề của nội dung
    title VARCHAR(255),
    
    -- Mô tả chi tiết của nội dung
    description TEXT,
    
    -- Ngôn ngữ chính của nội dung (ví dụ: 'vi', 'en')
    language VARCHAR(10),
    
    -- Thời gian nội dung được đưa vào hệ thống
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Các danh mục của nội dung, lưu dưới dạng mảng
    categories VARCHAR(50)[],
    
    -- Nguồn gốc của nội dung
    source VARCHAR(50) DEFAULT 'self_ingested',
    
    -- Độ dài của nội dung (đối với âm thanh, video)
    duration_seconds FLOAT,
    
    -- Độ phân giải của nội dung (đối với hình ảnh, video)
    resolution VARCHAR(50),
    
    -- Bản ghi chép nội dung
    transcript TEXT,
    
    -- Tác giả của nội dung
    author VARCHAR(255),
    
    -- Thông tin địa lý dưới dạng JSONB để linh hoạt lưu trữ
    location_metadata JSONB,
    
    -- Cột lưu vector embedding, với 38 chiều.
    -- Bạn cần đảm bảo đã cài đặt extension `pgvector`
    embedding_vector vector(38)
);

--
-- Tạo các chỉ mục để tăng tốc độ truy vấn
--

-- Chỉ mục trên cột `language` và `source` để tìm kiếm nhanh các nội dung theo ngôn ngữ hoặc nguồn.
CREATE INDEX idx_contents_language ON contents(language);
CREATE INDEX idx_contents_source ON contents(source);

-- Chỉ mục GIN trên cột `categories` để tìm kiếm hiệu quả các phần tử trong mảng.
CREATE INDEX idx_contents_categories ON contents USING GIN(categories);

-- Chỉ mục cho tìm kiếm vector tương tự.
-- Sử dụng chỉ mục IVF hoặc HNSW để tối ưu hóa tìm kiếm.
-- Ví dụ: Chỉ mục HNSW cho tìm kiếm tương tự cosine
-- CREATE INDEX ON contents USING hnsw (embedding_vector vector_cosine_ops);
-- Hoặc chỉ mục IVF cho tìm kiếm tương tự L2
-- CREATE INDEX ON contents USING ivfflat (embedding_vector vector_l2_ops);