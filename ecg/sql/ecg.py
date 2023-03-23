CREATE_ECG_QUERY = """
    INSERT INTO ecgs (id, owner_id, date)
    VALUES (:id, :owner_id, :date)
"""
CREATE_LEAD_QUERY = """
    INSERT INTO leads (name, ecg_id, signal)
    VALUES (:name, :ecg_id, :signal)
"""
GET_ECG_BY_ID_QUERY = """
    SELECT * FROM ecgs WHERE id = :ecg_id
"""
GET_LEAD_BY_ECG_ID_QUERY = """
    SELECT * FROM leads WHERE ecg_id = :ecg_id
"""
CREATE_ECG_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ecgs (
    id VARCHAR(24) PRIMARY KEY,
    owner_id UUID NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
"""
CREATE_LEAD_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(4) NOT NULL,
    ecg_id VARCHAR(24) NOT NULL,
    signal INTEGER[],
    FOREIGN KEY (ecg_id) REFERENCES ecgs(id) ON DELETE CASCADE
);
"""
