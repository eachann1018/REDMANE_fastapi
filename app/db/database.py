import sqlite3

DATABASE = 'data/data_redmane.db'

def init_db():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        # Create tables
        cur.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            name TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            ext_patient_id TEXT,
            ext_patient_url TEXT,
            public_patient_id TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS patients_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            key TEXT,
            value TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            ext_sample_id TEXT,
            ext_sample_url TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS samples_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id INTEGER NOT NULL,
            key TEXT,
            value TEXT,
            FOREIGN KEY (sample_id) REFERENCES samples(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS raw_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            path TEXT,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS raw_files_metadata (
            metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_file_id INTEGER,
            metadata_key TEXT NOT NULL,
            metadata_value TEXT NOT NULL,
            FOREIGN KEY (raw_file_id) REFERENCES raw_files (id)
        );
        ''')

        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
