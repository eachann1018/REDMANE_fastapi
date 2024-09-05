from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
import sqlite3
from typing import List
from app.schemas.schemas import (
    RawFileCreate,
)
from fastapi.responses import RedirectResponse

from app.schemas.schemas import (
    Project,
    Dataset,
    DatasetMetadata,
    DatasetWithMetadata,
    Patient,
    PatientWithSampleCount,
    PatientMetadata,
    PatientWithMetadata,
    SampleMetadata,
    Sample,
    SampleWithoutPatient,
    RawFileResponse,
    PatientWithSamples,
    RawFileMetadataCreate,
    RawFileCreate,
    MetadataUpdate,
)

DATABASE = 'data/data_redmane.db'

router = APIRouter()

@router.post("/add_raw_files/")
async def add_raw_files(raw_files: List[RawFileCreate]):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert raw_files and fetch their IDs
        raw_file_ids = []
        for raw_file in raw_files:
            cursor.execute('''
                INSERT INTO raw_files (dataset_id, path)
                VALUES (?, ?)
            ''', (raw_file.dataset_id, raw_file.path))
            raw_file_id = cursor.lastrowid
            raw_file_ids.append(raw_file_id)

            # Insert associated metadata for this raw_file
            if raw_file.metadata:
                for metadata in raw_file.metadata:
                    cursor.execute('''
                        INSERT INTO raw_files_metadata (raw_file_id, metadata_key, metadata_value)
                        VALUES (?, ?, ?)
                    ''', (raw_file_id, metadata.metadata_key, metadata.metadata_value))

        conn.commit()
        conn.close()
        return {"status": "success", "message": "Raw files and metadata added successfully"}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/")
async def root():
    return RedirectResponse(url="/projects")

# Route to fetch all patients and their metadata for a project_id
@router.get("/patients_metadata/{patient_id}", response_model=List[PatientWithSamples])
async def get_patients_metadata(project_id: int,patient_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()


        if patient_id != 0:

            cursor.execute('''
                SELECT p.id, p.project_id, p.ext_patient_id, p.ext_patient_url, p.public_patient_id,
                       pm.id, pm.key, pm.value
                FROM patients p
                LEFT JOIN patients_metadata pm ON p.id = pm.patient_id
                WHERE p.project_id = ? and p.id = ?
                ORDER BY p.id
            ''', (project_id,patient_id,))
        else:
    
            cursor.execute('''
                SELECT p.id, p.project_id, p.ext_patient_id, p.ext_patient_url, p.public_patient_id,
                       pm.id, pm.key, pm.value
                FROM patients p
                LEFT JOIN patients_metadata pm ON p.id = pm.patient_id
                WHERE p.project_id = ?
                ORDER BY p.id
            ''', (project_id,))

        rows = cursor.fetchall()

        patients = []
        current_patient = None
        for row in rows:

            if not current_patient or current_patient['id'] != row[0]:

                if current_patient:
                    patients.append(current_patient)

                current_patient = {
                    'id': row[0],
                    'project_id': row[1],
                    'ext_patient_id': row[2],
                    'ext_patient_url': row[3],
                    'public_patient_id': row[4],
                    'samples': [],
                    'metadata': [] 
                }

            if row[5]:
                current_patient['metadata'].append({
                    'id': row[5],
                    'patient_id': row[0],
                    'key': row[6],
                    'value': row[7]
                })

        if current_patient:
            patients.append(current_patient)


        for patient in patients:
            cursor.execute('''
                SELECT s.id, s.patient_id, s.ext_sample_id, s.ext_sample_url,
                       sm.id, sm.key, sm.value
                FROM samples s
                LEFT JOIN samples_metadata sm ON s.id = sm.sample_id
                WHERE s.patient_id = ?
                ORDER BY s.id
            ''', (patient['id'],))

            sample_rows = cursor.fetchall()
            current_sample = None
            for sample_row in sample_rows:
                if not current_sample or current_sample['id'] != sample_row[0]:
                    if current_sample:
                        patient['samples'].append(current_sample)
                    current_sample = {
                        'id': sample_row[0],
                        'patient_id': sample_row[1],
                        'ext_sample_id': sample_row[2],
                        'ext_sample_url': sample_row[3],
                        'metadata': []
                    }
                if sample_row[4]:
                    current_sample['metadata'].append({
                        'id': sample_row[4],
                        'sample_id': sample_row[0],
                        'key': sample_row[5],
                        'value': sample_row[6]
                    })
            if current_sample:
                patient['samples'].append(current_sample)

        conn.close()

        return patients

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Route to fetch all samples and metadata for a project_id and include patient information
@router.get("/samples/{sample_id}", response_model=List[Sample])
async def get_samples_per_patient(sample_id: int, project_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if sample_id != 0:
            cursor.execute('''
                SELECT s.id AS sample_id, s.patient_id, s.ext_sample_id, s.ext_sample_url,
                       sm.id AS metadata_id, sm.key, sm.value,
                       p.id AS patient_id, p.project_id, p.ext_patient_id, p.ext_patient_url, p.public_patient_id
                FROM samples s
                LEFT JOIN samples_metadata sm ON s.id = sm.sample_id
                LEFT JOIN patients p ON s.patient_id = p.id
                WHERE p.project_id = ? and s.id = ?
                ORDER BY s.id, sm.id
            ''', (project_id,sample_id,))
        else:
            cursor.execute('''
                SELECT s.id AS sample_id, s.patient_id, s.ext_sample_id, s.ext_sample_url,
                       sm.id AS metadata_id, sm.key, sm.value,
                       p.id AS patient_id, p.project_id, p.ext_patient_id, p.ext_patient_url, p.public_patient_id
                FROM samples s
                LEFT JOIN samples_metadata sm ON s.id = sm.sample_id
                LEFT JOIN patients p ON s.patient_id = p.id
                WHERE p.project_id = ?
                ORDER BY s.id, sm.id
            ''', (project_id,))
 


        rows = cursor.fetchall()
        conn.close()

        samples = []
        current_sample = None
        for row in rows:
            if not current_sample or current_sample['id'] != row[0]:
                if current_sample:
                    samples.append(current_sample)
                current_sample = {
                    'id': row[0],
                    'patient_id': row[1],
                    'ext_sample_id': row[2],
                    'ext_sample_url': row[3],
                    'metadata': [],
                    'patient': {
                        'id': row[7],
                        'project_id': row[8],
                        'ext_patient_id': row[9],
                        'ext_patient_url': row[10],
                        'public_patient_id': row[11]
                    }
                }

            if row[4]:  # Check if metadata exists
                current_sample['metadata'].append({
                    'id': row[4],
                    'sample_id': row[0],
                    'key': row[5],
                    'value': row[6]
                })

        if current_sample:
            samples.append(current_sample)

        return samples

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Route to fetch all patients with sample counts
@router.get("/patients/", response_model=List[PatientWithSampleCount])
async def get_patients(
    project_id: Optional[int] = Query(None, description="Filter by project ID")
):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Base query to fetch all patients with sample counts
        query = '''
            SELECT patients.id, patients.project_id, patients.ext_patient_id, patients.ext_patient_url,
                   patients.public_patient_id, COUNT(samples.id) AS sample_count
            FROM patients
            LEFT JOIN samples ON patients.id = samples.patient_id
        '''
        params = []

        # Append conditions based on the presence of project_id
        if project_id is not None:
            query += ' WHERE patients.project_id = ?'
            params.append(project_id)
        
        # Complete the query
        query += ' GROUP BY patients.id ORDER BY patients.id'

        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Process the results
        patients = []
        for row in rows:
            patients.append({
                'id': row[0],
                'project_id': row[1],
                'ext_patient_id': row[2],
                'ext_patient_url': row[3],
                'public_patient_id': row[4],
                'sample_count': row[5]
            })
        
        return patients
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Route to fetch all projects and their statuses
@router.get("/projects/", response_model=List[Project])
async def get_projects():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, status FROM projects")
    rows = cursor.fetchall()
    conn.close()
    return [Project(id=row[0], name=row[1], status=row[2]) for row in rows]

# Route to fetch all datasets
@router.get("/datasets/", response_model=List[Dataset])
async def get_datasets(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    dataset_id: Optional[int] = Query(None, description="Filter by dataset ID")
):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT id, project_id, name FROM datasets WHERE 1=1"
    params = []

    if project_id is not None:
        query += " AND project_id = ?"
        params.append(project_id)
    
    if dataset_id is not None:
        query += " AND id = ?"
        params.append(dataset_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [Dataset(id=row[0], project_id=row[1], name=row[2]) for row in rows]

# Endpoint to fetch dataset details and metadata by dataset_id
@router.get("/datasets_with_metadata/{dataset_id}", response_model=DatasetWithMetadata)
async def get_dataset_with_metadata(dataset_id: int, project_id: int):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Fetch dataset details
        cursor.execute('''
            SELECT id, project_id, name
            FROM datasets
            WHERE id = ? AND project_id = ?
        ''', (dataset_id, project_id))
        dataset_row = cursor.fetchone()
        
        if not dataset_row:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Fetch dataset metadata
        cursor.execute('''
            SELECT id, dataset_id, key, value
            FROM datasets_metadata
            WHERE dataset_id = ?
        ''', (dataset_id,))
        metadata_rows = cursor.fetchall()
        
        conn.close()
        
        dataset = {
            "id": dataset_row[0],
            "project_id": dataset_row[1],
            "name": dataset_row[2],
            "metadata": [{"id": row[0], "dataset_id": row[1], "key": row[2], "value": row[3]} for row in metadata_rows]
        }

        return dataset

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/raw_files_with_metadata/{dataset_id}", response_model=List[RawFileResponse])
async def get_raw_files_with_metadata(dataset_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Query to get raw files and their associated metadata
    query = """
    SELECT rf.id, rf.path, rfm.metadata_value AS sample_id, s.ext_sample_id
    FROM raw_files rf
    LEFT JOIN raw_files_metadata rfm ON rf.id = rfm.raw_file_id
    LEFT JOIN samples s ON rfm.metadata_value = s.id
    WHERE rf.dataset_id = ? AND rfm.metadata_key = 'sample_id'
    """
    cursor.execute(query, (dataset_id,))
    raw_files = cursor.fetchall()

    response = []
    
    for raw_file in raw_files:
        raw_file_id, path, sample_id, ext_sample_id = raw_file
        
        # Fetch sample metadata
        cursor.execute("SELECT id, sample_id, key, value FROM samples_metadata WHERE sample_id = ?", (sample_id,))
        sample_metadata_rows = cursor.fetchall()

        sample_metadata_list = []
        for row in sample_metadata_rows:
            sample_metadata_list.append({
                'id': row[0],
                'sample_id': row[1],
                'key': row[2],
                'value': row[3]
                

            }) 
        print(sample_metadata_list)


        response.append(RawFileResponse(
            id=raw_file_id,
            path=path,
            sample_id=sample_id,
            ext_sample_id=ext_sample_id,
            sample_metadata=sample_metadata_list
        ))

    conn.close()
    return response

@router.put("/datasets_metadata/size_update", response_model=MetadataUpdate)
def update_metadata(update: MetadataUpdate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Update record with key 'raw_file_extension_size_of_all_files' for the given dataset_id
    if update.raw_file_size:
        cursor.execute(
            "SELECT id, value FROM datasets_metadata WHERE key = 'raw_file_extension_size_of_all_files' AND dataset_id = ?",
            (update.dataset_id,)
        )
        record = cursor.fetchone()
        if record:
            record_id, value_str = record
            # Update the metadata with the new value
            cursor.execute(
                "UPDATE datasets_metadata SET value = ? WHERE id = ?",
                (update.raw_file_size, record_id)
            )
        else:
            # Insert a new record if it doesn't exist
            cursor.execute(
                "INSERT INTO datasets_metadata (dataset_id, key, value) VALUES (?, 'raw_file_extension_size_of_all_files', ?)",
                (update.dataset_id, update.raw_file_size))
            
    
    # Update record with key 'last_size_update' for the given dataset_id
    if update.last_size_update:
        cursor.execute(
            "SELECT id, value FROM datasets_metadata WHERE key = 'last_size_update' AND dataset_id = ?",
            (update.dataset_id,)
        )
        record = cursor.fetchone()
        if record:
            record_id, value_str = record
            # Update the metadata with the new value
            cursor.execute(
                "UPDATE datasets_metadata SET value = ? WHERE id = ?",
                (update.last_size_update, record_id)
            )
        else:
            # Insert a new record if it doesn't exist
            cursor.execute(
                "INSERT INTO datasets_metadata (dataset_id, key, value) VALUES (?, 'last_size_update', ?)",
                (update.dataset_id, update.last_size_update))
    
    conn.commit()
    conn.close()

    return update
