from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.db.database import get_db  # Import the database session
from app.schemas.schemas import (
    RawFileCreate, Project, Dataset, DatasetMetadata, DatasetWithMetadata,
    Patient, PatientWithSampleCount, PatientMetadata, PatientWithMetadata,
    SampleMetadata, Sample, SampleWithoutPatient, RawFileResponse,
    PatientWithSamples, RawFileMetadataCreate, MetadataUpdate
)

DATABASE = 'data/data_redmane.db'

router = APIRouter()

@router.post("/add_raw_files/")
async def add_raw_files(raw_files: List[RawFileCreate], db: Session = Depends(get_db)):
    try:
        raw_file_ids = []
        for raw_file in raw_files:
            new_raw_file = RawFile(dataset_id=raw_file.dataset_id, path=raw_file.path)
            db.add(new_raw_file)
            db.commit()
            db.refresh(new_raw_file)
            raw_file_ids.append(new_raw_file.id)

            # Insert associated metadata for this raw file
            if raw_file.metadata:
                for metadata in raw_file.metadata:
                    new_metadata = RawFileMetadata(
                        raw_file_id=new_raw_file.id,
                        metadata_key=metadata.metadata_key,
                        metadata_value=metadata.metadata_value
                    )
                    db.add(new_metadata)

        db.commit()
        return {"status": "success", "message": "Raw files and metadata added successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/")
async def root():
    return RedirectResponse(url="/projects")

# Route to fetch all patients and their metadata for a project_id
@router.get("/patients_metadata/{patient_id}", response_model=List[PatientWithSamples])
async def get_patients_metadata(project_id: int, patient_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(Patient).filter(Patient.project_id == project_id)
        if patient_id != 0:
            query = query.filter(Patient.id == patient_id)

        patients = query.all()

        return patients

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Route to fetch all samples and metadata for a project_id and include patient information
@router.get("/samples/{sample_id}", response_model=List[Sample])
async def get_samples_per_patient(sample_id: int, project_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(Sample).join(Patient).filter(Patient.project_id == project_id)

        if sample_id != 0:
            query = query.filter(Sample.id == sample_id)

        samples = query.all()

        return samples

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Route to fetch all patients with sample counts
@router.get("/patients/", response_model=List[PatientWithSampleCount])
async def get_patients(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db)
):
    try:
        query = (
            db.query(Patient.id, Patient.project_id, Patient.ext_patient_id,
                     Patient.ext_patient_url, Patient.public_patient_id,
                     db.query(Sample).filter(Sample.patient_id == Patient.id).count().label("sample_count"))
        )

        if project_id is not None:
            query = query.filter(Patient.project_id == project_id)

        patients = query.all()
        return [
            PatientWithSampleCount(
                id=row[0], project_id=row[1], ext_patient_id=row[2], 
                ext_patient_url=row[3], public_patient_id=row[4], sample_count=row[5]
            )
            for row in patients
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Route to fetch all projects and their statuses
@router.get("/projects/", response_model=List[Project])
async def get_projects(db: Session = Depends(get_db)):
    try:
        projects = db.query(Project).all()
        return projects

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Route to fetch all datasets
@router.get("/datasets/", response_model=List[Dataset])
async def get_datasets(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    dataset_id: Optional[int] = Query(None, description="Filter by dataset ID"),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Dataset)
        if project_id:
            query = query.filter(Dataset.project_id == project_id)
        if dataset_id:
            query = query.filter(Dataset.id == dataset_id)

        datasets = query.all()
        return datasets

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Endpoint to fetch dataset details and metadata by dataset_id
@router.get("/datasets_with_metadata/{dataset_id}", response_model=DatasetWithMetadata)
async def get_dataset_with_metadata(dataset_id: int, project_id: int, db: Session = Depends(get_db)):
    try:
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.project_id == project_id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        metadata = db.query(DatasetMetadata).filter(DatasetMetadata.dataset_id == dataset_id).all()

        return DatasetWithMetadata(
            id=dataset.id,
            project_id=dataset.project_id,
            name=dataset.name,
            metadata=[{"id": md.id, "dataset_id": md.dataset_id, "key": md.key, "value": md.value} for md in metadata]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/raw_files_with_metadata/{dataset_id}", response_model=List[RawFileResponse])
async def get_raw_files_with_metadata(dataset_id: int, db: Session = Depends(get_db)):
    try:
        raw_files = (
            db.query(RawFile.id, RawFile.path, RawFileMetadata.metadata_value.label("sample_id"), Sample.ext_sample_id)
            .join(RawFileMetadata, RawFile.id == RawFileMetadata.raw_file_id)
            .join(Sample, RawFileMetadata.metadata_value == Sample.id)
            .filter(RawFile.dataset_id == dataset_id, RawFileMetadata.metadata_key == 'sample_id')
            .all()
        )

        response = []
        for raw_file_id, path, sample_id, ext_sample_id in raw_files:
            # Fetch sample metadata
            sample_metadata = db.query(SampleMetadata).filter(SampleMetadata.sample_id == sample_id).all()

            sample_metadata_list = [
                {"id": sm.id, "sample_id": sm.sample_id, "key": sm.key, "value": sm.value} for sm in sample_metadata
            ]

            response.append(RawFileResponse(
                id=raw_file_id,
                path=path,
                sample_id=sample_id,
                ext_sample_id=ext_sample_id,
                sample_metadata=sample_metadata_list
            ))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/datasets_metadata/size_update", response_model=MetadataUpdate)
async def update_metadata(update: MetadataUpdate, db: Session = Depends(get_db)):
    try:
        # Update or insert raw file extension size
        metadata_record = db.query(DatasetMetadata).filter(
            DatasetMetadata.key == 'raw_file_extension_size_of_all_files',
            DatasetMetadata.dataset_id == update.dataset_id
        ).first()

        if metadata_record:
            metadata_record.value = update.raw_file_size
        else:
            new_metadata = DatasetMetadata(
                dataset_id=update.dataset_id,
                key='raw_file_extension_size_of_all_files',
                value=update.raw_file_size
            )
            db.add(new_metadata)

        # Update or insert last size update timestamp
        last_update_record = db.query(DatasetMetadata).filter(
            DatasetMetadata.key == 'last_size_update',
            DatasetMetadata.dataset_id == update.dataset_id
        ).first()

        if last_update_record:
            last_update_record.value = update.last_size_update
        else:
            new_metadata = DatasetMetadata(
                dataset_id=update.dataset_id,
                key='last_size_update',
                value=update.last_size_update
            )
            db.add(new_metadata)

        db.commit()
        return update

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
