import psycopg2
import csv
import argparse


# Function to import data from CSV into PostgreSQL tables
def import_csv_to_postgresql(conn, project_id, ext_sample_url, csv_file):
    cur = conn.cursor()

    # Open the CSV file and read its contents
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Process each row in the CSV file
        for row in reader:
            # Fetch patient_id based on project_id and record_id (ext_patient_id)
            cur.execute('''
            SELECT id FROM patients WHERE project_id = %s AND ext_patient_id = %s
            ''', (project_id, row['record_id']))
            patient_id = cur.fetchone()
            if patient_id:
                patient_id = patient_id[0]
            else:
                print(
                    f"No patient found with project_id '{project_id}' and record_id '{row['record_id']}'. Skipping row.")
                continue

            # Insert into samples table
            cur.execute('''
            INSERT INTO samples (patient_id, ext_sample_id, ext_sample_url)
            VALUES (%s, %s, %s)
            RETURNING id
            ''', (patient_id, row['sample_id'], ext_sample_url))

            sample_id = cur.fetchone()[0]

            # Insert into samples_metadata table
            cur.execute('''
            INSERT INTO samples_metadata (sample_id, key, value)
            VALUES (%s, %s, %s)
            ''', (sample_id, 'ext_sample_batch', row['ext_sample_batch']))

            cur.execute('''
            INSERT INTO samples_metadata (sample_id, key, value)
            VALUES (%s, %s, %s)
            ''', (sample_id, 'tissue', row['tissue']))

            cur.execute('''
            INSERT INTO samples_metadata (sample_id, key, value)
            VALUES (%s, %s, %s)
            ''', (sample_id, 'sample_date', row['sample_date']))

    # Commit the transaction
    conn.commit()


# Main execution when running the script
if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='Import CSV data into PostgreSQL database.')
    parser.add_argument('project_id', type=str, help='The project ID to use to find the patients')
    parser.add_argument('ext_sample_url', type=str, help='The external sample URL to populate in samples')
    parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')
    args = parser.parse_args()

    # PostgreSQL database connection configuration
    DATABASE_CONFIG = {
        'dbname': 'readmedatabase',
        'user': 'username',
        'password': 'password',
        'host': 'localhost',
        'port': 5432
    }

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**DATABASE_CONFIG)

    # Call function to import data into PostgreSQL tables
    import_csv_to_postgresql(conn, args.project_id, args.ext_sample_url, args.csv_file)

    # Close the database connection
    conn.close()
