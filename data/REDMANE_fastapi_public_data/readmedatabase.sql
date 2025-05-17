--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: datasets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datasets (
    id integer NOT NULL,
    project_id integer NOT NULL,
    name text
);


ALTER TABLE public.datasets OWNER TO postgres;

--
-- Name: datasets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datasets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datasets_id_seq OWNER TO postgres;

--
-- Name: datasets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datasets_id_seq OWNED BY public.datasets.id;


--
-- Name: datasets_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datasets_metadata (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    key text NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.datasets_metadata OWNER TO postgres;

--
-- Name: datasets_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

      # Define the base path
      base_path <- "/vast/projects/TDE/TDE0005/"

      # Define the raw file array
      raw_file_array <- c(
        "./raw_data/batch1_test_LC_Sample1.fastq",
  "./raw_data/batch1_test_LC_Sample2.fastq",
  "./raw_data/batch1_test_LC_Sample3.fastq",
  "./raw_data/batch1_test_LC_Sample4.fastq",
  "./raw_data/batch1_test_LC_Sample5.fastq"
      )

      # Combine paths
      file_paths <- paste(base_path, raw_file_array, sep = "")

      # Print the file paths
      print(file_paths)

CREATE SEQUENCE public.datasets_metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.datasets_metadata_id_seq OWNER TO postgres;

--
-- Name: datasets_metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datasets_metadata_id_seq OWNED BY public.datasets_metadata.id;


--
-- Name: files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files (
    id integer NOT NULL,
    dataset_id integer NOT NULL,
    path text,
    file_type text,
    CONSTRAINT file_type_check CHECK ((file_type = ANY (ARRAY['raw'::text, 'processed'::text, 'summarised'::text])))
);


ALTER TABLE public.files OWNER TO postgres;

--
-- Name: files_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.files_metadata (
    metadata_id integer NOT NULL,
    file_id integer,
    metadata_key text NOT NULL,
    metadata_value text NOT NULL
);


ALTER TABLE public.files_metadata OWNER TO postgres;

--
-- Name: patients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    project_id integer NOT NULL,
    ext_patient_id text,
    ext_patient_url text,
    public_patient_id text
);


ALTER TABLE public.patients OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patients_id_seq OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: patients_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients_metadata (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    key text,
    value text
);


ALTER TABLE public.patients_metadata OWNER TO postgres;

--
-- Name: patients_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patients_metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.patients_metadata_id_seq OWNER TO postgres;

--
-- Name: patients_metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patients_metadata_id_seq OWNED BY public.patients_metadata.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    name text NOT NULL,
    status text
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO postgres;

--
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- Name: files_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.files_id_seq OWNER TO postgres;

--
-- Name: files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;


--
-- Name: files_metadata_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.files_metadata_metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.files_metadata_metadata_id_seq OWNER TO postgres;

--
-- Name: files_metadata_metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.files_metadata_metadata_id_seq OWNED BY public.files_metadata.metadata_id;


--
-- Name: samples; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samples (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    ext_sample_id text,
    ext_sample_url text
);


ALTER TABLE public.samples OWNER TO postgres;

--
-- Name: samples_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.samples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.samples_id_seq OWNER TO postgres;

--
-- Name: samples_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.samples_id_seq OWNED BY public.samples.id;


--
-- Name: samples_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samples_metadata (
    id integer NOT NULL,
    sample_id integer NOT NULL,
    key text,
    value text
);


ALTER TABLE public.samples_metadata OWNER TO postgres;

--
-- Name: samples_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.samples_metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.samples_metadata_id_seq OWNER TO postgres;

--
-- Name: samples_metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.samples_metadata_id_seq OWNED BY public.samples_metadata.id;


--
-- Name: datasets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets ALTER COLUMN id SET DEFAULT nextval('public.datasets_id_seq'::regclass);


--
-- Name: datasets_metadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets_metadata ALTER COLUMN id SET DEFAULT nextval('public.datasets_metadata_id_seq'::regclass);


--
-- Name: files id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);


--
-- Name: files_metadata metadata_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_metadata ALTER COLUMN metadata_id SET DEFAULT nextval('public.files_metadata_metadata_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: patients_metadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients_metadata ALTER COLUMN id SET DEFAULT nextval('public.patients_metadata_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- Name: samples id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples ALTER COLUMN id SET DEFAULT nextval('public.samples_id_seq'::regclass);


--
-- Name: samples_metadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_metadata ALTER COLUMN id SET DEFAULT nextval('public.samples_metadata_id_seq'::regclass);


--
-- Data for Name: datasets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datasets (id, project_id, name) FROM stdin;
1	1	ABC
2	1	XYZ
3	2	DEF
\.


--
-- Data for Name: datasets_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datasets_metadata (id, dataset_id, key, value) FROM stdin;
\.


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.files (id, dataset_id, path, file_type) FROM stdin;
\.


--
-- Data for Name: files_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.files_metadata (metadata_id, file_id, metadata_key, metadata_value) FROM stdin;
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients (id, project_id, ext_patient_id, ext_patient_url, public_patient_id) FROM stdin;
1	1	EXT-P001	https://example.org/patient/EXT-P001	PUB-001
2	1	EXT-P002	https://example.org/patient/EXT-P002	PUB-002
3	1	EXT-P003	https://example.org/patient/EXT-P003	PUB-003
7	2	EXT-P004	https://example.org/patient/EXT-P004	PUB-004
8	3	EXT-P005	https://example.org/patient/EXT-P005	PUB-005
9	3	EXT-P006	https://example.org/patient/EXT-P006	PUB-006
\.


--
-- Data for Name: patients_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients_metadata (id, patient_id, key, value) FROM stdin;
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, name, status) FROM stdin;
1	Cancer Genomics Portal	In Progress
2	AI for Pathology	Completed
3	Brain Imaging Dashboard	Pending
\.


--
-- Data for Name: samples; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samples (id, patient_id, ext_sample_id, ext_sample_url) FROM stdin;
1	1	SAMPLE-001-A	https://example.org/sample/SAMPLE-001-A
2	2	SAMPLE-002-A	https://example.org/sample/SAMPLE-002-A
3	3	SAMPLE-003-A	https://example.org/sample/SAMPLE-003-A
\.


--
-- Data for Name: samples_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samples_metadata (id, sample_id, key, value) FROM stdin;
\.


--
-- Name: datasets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datasets_id_seq', 3, true);


--
-- Name: datasets_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datasets_metadata_id_seq', 1, false);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patients_id_seq', 9, true);


--
-- Name: patients_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patients_metadata_id_seq', 1, false);


--
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 3, true);


--
-- Name: files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.files_id_seq', 1, true);


--
-- Name: files_metadata_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.files_metadata_metadata_id_seq', 1, false);


--
-- Name: samples_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.samples_id_seq', 3, true);


--
-- Name: samples_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.samples_metadata_id_seq', 1, false);


--
-- Name: datasets_metadata datasets_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets_metadata
    ADD CONSTRAINT datasets_metadata_pkey PRIMARY KEY (id);


--
-- Name: datasets datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pkey PRIMARY KEY (id);


--
-- Name: patients_metadata patients_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients_metadata
    ADD CONSTRAINT patients_metadata_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: files_metadata files_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_metadata
    ADD CONSTRAINT files_metadata_pkey PRIMARY KEY (metadata_id);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);


--
-- Name: samples_metadata samples_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_metadata
    ADD CONSTRAINT samples_metadata_pkey PRIMARY KEY (id);


--
-- Name: samples samples_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples
    ADD CONSTRAINT samples_pkey PRIMARY KEY (id);


--
-- Name: datasets_metadata datasets_metadata_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets_metadata
    ADD CONSTRAINT datasets_metadata_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.datasets(id);


--
-- Name: datasets datasets_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: patients_metadata patients_metadata_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients_metadata
    ADD CONSTRAINT patients_metadata_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: patients patients_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: files files_dataset_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES public.datasets(id);


--
-- Name: files_metadata files_metadata_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.files_metadata
    ADD CONSTRAINT files_metadata_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.files(id);


--
-- Name: samples_metadata samples_metadata_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_metadata
    ADD CONSTRAINT samples_metadata_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.samples(id);


--
-- Name: samples samples_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples
    ADD CONSTRAINT samples_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO postgres;


--
-- PostgreSQL database dump complete
--