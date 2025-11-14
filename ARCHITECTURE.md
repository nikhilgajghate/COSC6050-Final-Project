# System Architecture Diagram

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           G2I Application                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                             │
├─────────────────────────────────────────────────────────────────────┤
│  Web UI (index.html)                                                │
│  ├─ Single Name Input Form                                          │
│  ├─ CSV Upload Form                                                 │
│  └─ Audio Playback                                                  │
│                                                                     │
│  JavaScript                                                         │
│  ├─ Form submission handlers                                        │
│  ├─ AJAX requests to backend                                        │
│  └─ Audio playback control                                          │
└─────────────────────────────────────────────────────────────────────┘
                               ↕ HTTP/AJAX
┌─────────────────────────────────────────────────────────────────────┐
│                          Backend Layer (Flask)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  app.py (Flask Server)                                              │
│  ├─ Routes                                                          │
│  │  ├─ GET  /                  → Serve HTML                         │
│  │  ├─ POST /pronounce         → Single pronunciation               │
│  │  ├─ POST /upload            → CSV batch processing               │
│  │  ├─ GET  /api/health        → Health check                       │
│  │  ├─ GET  /api/stats         → Database stats                     │
│  │  ├─ GET  /api/operations/*  → Query operations                   │
│  │                                                                  │
│  └─ Database Integration                                            │
│     └─ get_db() → Lazy initialization with graceful degradation     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
         ↓                              ↓                       ↓
    ┌────────┐                   ┌──────────────┐        ┌─────────────┐
    │ Audio  │                   │   Database   │        │  ElevenLabs │
    │ Files  │                   │   Manager    │        │     API     │
    └────────┘                   └──────────────┘        └─────────────┘
         ↓                              ↓                       ↓
┌─────────────────┐         ┌──────────────────────┐   ┌───────────────┐
│ app.py          │         │ database_manager.py  │   │   External    │
│                 │         │                      │   │   Service     │
│ pronounce_name()│         │ Data Bridge Layer    │   │               │
│ - Text→Speech   │         │ ├─ insert_driver     │   │ - Voice Gen   │
│ - Save MP3      │         │ ├─ insert_single     │   │ - Multilingual│
└─────────────────┘         │ ├─ insert_csv_upload │   │ - High Quality│
                            │ ├─ get_operations    │   └───────────────┘
                            │ └─ get_stats         │
                            └──────────────────────┘
                                       ↓
                             ┌──────────────────────┐
                             │   PostgreSQL DB      │
                             │                      │
                             │  ┌────────────┐      │
                             │  │  driver    │      │
                             │  │ (parent)   │      │
                             │  └─────┬──────┘      │
                             │        │             │
                             │   ┌────┴─────┐       │
                             │   │          │       │
                             │  ┌▼──────┐ ┌▼──┐     │
                             │  │single │ │csv│     │
                             │  │(child)│ │   │     │
                             │  └───────┘ └───┘     │
                             └──────────────────────┘
```

## Request Flow Diagrams

### Single Name Pronunciation Flow

```
┌──────┐     ┌───────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ User │────>│Browser│────>│  Flask   │────>│app.py    │────>│ElevenLabs│
│      │     │  UI   │     │ /pronounce     │          │     │   API    │
└──────┘     └───────┘     └──────────┘     └──────────┘     └──────────┘
                  ↓              ↓                ↓                 ↓
              Submit         Route            Generate           Convert
              Form          Handler           Audio File        Text→Speech
                  ↓              ↓                ↓                 ↓
                  │              │                │            Return Audio
                  │              │                │                 ↓
                  │              │                └─────────────────┘
                  │              │                ↓
                  │              │           Save MP3
                  │              │                ↓
                  │              ↓           ┌──────────┐
                  │         Log to DB ────>  │ Database │
                  │              ↓           │ Manager  │
                  │         Return URL       └──────────┘
                  │              ↓                ↓
                  │         JSON Response    Insert Driver
                  │              ↓            Insert Single
                  │              ↓                ↓
                  └──────────────┘           Commit to DB
                  ↓
            Play Audio
```

### CSV Upload Flow

```
┌──────┐     ┌───────┐     ┌──────────┐     ┌──────────┐
│ User │────>│Browser│────>│  Flask   │────>│ Parse    │
│      │     │  UI   │     │ /upload  │     │   CSV    │
└──────┘     └───────┘     └──────────┘     └──────────┘
                  ↓              ↓                ↓
           Upload CSV       Save File      Read Names
                  ↓              ↓                ↓
                  │              │         ┌──────────┐
                  │              │    ┌───>│app.py│─┐
                  │              │    │    └──────────┘ │
                  │              │    │         ↓       │
                  │              │    │    Generate     │
                  │              │    │    Audio 1      │
                  │              │    │         ↓       │
                  │              │    │    ┌──────────┐ │
                  │              │    └───>│app.py    │─┘
                  │              │         └──────────┘
                  │              │         (Loop for
                  │              │         all names)
                  │              ↓              ↓
                  │         Collect URLs   Save All MP3s
                  │              ↓              ↓
                  │              ↓         ┌──────────┐
                  │         Log to DB ──>  │ Database │
                  │              ↓         │ Manager  │
                  │         JSON Array     └──────────┘
                  │              ↓              ↓
                  │         [{name,url},  Insert Driver
                  │          {name,url},  Insert CSV_Upload
                  │          ...]              ↓
                  │              ↓         Commit to DB
                  └──────────────┘
                  ↓
         Play Audio Sequentially
         (with 2s delays)
```

## Database Schema Relationships

```
┌─────────────────────────────────────────┐
│           Driver Table                  │
│         (Parent Table)                  │
├─────────────────────────────────────────┤
│ id          UUID (PK)                   │
│ feature     VARCHAR                     │
│             'single_text' |             │
│             'csv_upload'                │
│ datetime    TIMESTAMP                   │
└────────────┬────────────────────────────┘
             │
             │ Foreign Key Relationship
             │ (1:1 with child tables)
             │
        ┌────┴─────┐
        │          │
        ▼          ▼
┌────────────┐  ┌───────────────┐
│Single Table│  │CSV_Upload Tbl │
│  (Child)   │  │    (Child)    │
├────────────┤  ├───────────────┤
│id (PK, FK) │  │id (PK, FK)    │
│input       │  │filename       │
│datetime    │  │contents(JSONB)│
└────────────┘  │datetime       │
                └───────────────┘
```

## Database Manager (Data Bridge Layer)

```
┌────────────────────────────────────────────────────────┐
│            database_manager.py                         │
│         (Abstraction Layer)                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Class: DatabaseManager                                │
│  ├─ __init__()                                         │
│  │   └─ Create SQLAlchemy engine                       │
│  │                                                     │
│  ├─ Connection Methods                                 │
│  │   ├─ _connect()                                     │
│  │   └─ test_connection()                              │
│  │                                                     │
│  ├─ Insert Methods (Write Operations)                  │
│  │   ├─ insert_driver_record()                         │
│  │   ├─ insert_single_record()                         │
│  │   └─ insert_csv_upload_record()                     │
│  │                                                     │
│  ├─ Query Methods (Read Operations)                    │
│  │   ├─ get_driver_records()                           │
│  │   ├─ get_single_records()                           │
│  │   ├─ get_csv_upload_records()                       │
│  │   ├─ get_single_operations_with_details()           │
│  │   ├─ get_csv_operations_with_details()              │  
│  │   └─ get_operation_by_id()                          │
│  │                                                     │
│  └─ Utility Methods                                    │
│      ├─ get_all_tables_info()                          │
│      └─ close_connection()                             │
│                                                        │
│  Benefits:                                             │
│  • Single point of database access                     │
│  • SQL abstraction (Flask doesn't write SQL)           │
│  • Easy to test and maintain                           │
│  • Pandas DataFrame integration                        │
│  • Type hints and documentation                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Setup Flow

```
Developer Setup Process
         ↓
    ┌────────────────────────────────┐
    │ 1. Install Dependencies        │
    │    pip install -r requirements │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ 2. Create .env file            │
    │    - ELEVENLABS_API_KEY        │
    │    - DB_* (optional)           │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ 3. Run Setup Script            │
    │    python database/            │
    │    setup_database.py           │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ Setup Script Actions:          │
    │ ✓ Check PostgreSQL running     │
    │ ✓ Create database if needed    │
    │ ✓ Run SQL schema files         │
    │ ✓ Verify tables created        │
    │ ✓ Test DatabaseManager         │
    │ ✓ Show status summary          │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ 4. Start Flask Backend         │
    │    cd src/Backend              │
    │    python app.py               │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ Flask Initialization:          │
    │ ├─ Import DatabaseManager      │
    │ ├─ Lazy load database          │
    │ │  ├─ Success: Enable logging  │
    │ │  └─ Fail: Continue w/o DB    │
    │ └─ Start server                │
    └────────────────────────────────┘
         ↓
    ┌────────────────────────────────┐
    │ 5. Ready to Use!               │
    │    http://localhost:5000       │
    └────────────────────────────────┘
```

## Graceful Degradation Flow

```
Flask Backend Startup
         ↓
    ┌────────────────┐
    │ Try to connect │
    │ to database    │
    └────────┬───────┘
             │
        ┌────┴────┐
        │         │
   Success      Failure
        │         │
        ↓         ↓
┌───────────┐  ┌──────────┐
│ db_manager│  │db_manager│
│ = DBM()   │  │ = False  │
└─────┬─────┘  └────┬─────┘
      │             │
      ↓             ↓
┌─────────────┐  ┌──────────────┐
│Print:       │  │Print:        │
│Database     │  │Database      │
│connected    │  │not available │
└──────┬──────┘  └──────┬───────┘
       │                │
       ↓                ↓
┌──────────────┐  ┌──────────────┐
│Full Features:│  │Basic Features│
│- Logging ✓   │  │- Logging ✗   │
│- APIs ✓      │  │- APIs ✗      │
│- Stats ✓     │  │- Stats ✗     │
│- App ✓       │  │- App ✓       │
└──────────────┘  └──────────────┘
       │                │
       └────────┬───────┘
                ↓
       ┌─────────────────┐
       │ Flask App Runs  │
       │ (Both Paths OK) │
       └─────────────────┘
```

## API Endpoints Architecture

```
┌──────────────────────────────────────────────┐
│           Flask API Routes                   │
├──────────────────────────────────────────────┤
│                                              │
│  Main Routes                                 │
│  ├─ GET  /              → index.html         │
│  ├─ POST /pronounce     → Single name        │
│  └─ POST /upload        → CSV batch          │
│                                              │
│  Monitoring API                              │
│  └─ /api/                                    │
│      ├─ GET /health                          │
│      │   └─ Check app & DB status            │
│      │                                       │
│      ├─ GET /stats                           │
│      │   └─ Get record counts                │
│      │                                       │
│      └─ /operations/                         │
│          ├─ GET /recent?limit=N              │
│          │   └─ Latest N operations          │
│          │                                   │
│          ├─ GET /single?limit=N              │
│          │   └─ Single text ops              │
│          │                                   │
│          └─ GET /csv?limit=N                 │
│              └─ CSV upload ops               │
│                                              │
└──────────────────────────────────────────────┘
```

## Key Design Patterns

### 1. Lazy Initialization
```python
db_manager = None  # Not initialized yet

def get_db():
    global db_manager
    if db_manager is None:
        # Initialize only when first needed
        db_manager = DatabaseManager()
    return db_manager
```

### 2. Graceful Degradation
```python
try:
    db = get_db()
    if db:
        # Try to log to database
        db.insert_driver_record(...)
except Exception:
    # Continue without logging
    pass
```

### 3. Data Bridge Pattern
```
Flask ──> DatabaseManager ──> SQLAlchemy ──> PostgreSQL
         (Abstraction)        (ORM)
```

### 4. Parent-Child Foreign Key
```sql
Driver (1) ──< FK >── (1) Single
       (1) ──< FK >── (1) CSV_Upload
```

---

**Legend:**
- `→` : Data flow / Function call
- `↓` : Sequential step
- `──>` : Dependency / Connection
- `<─` : Return value
- `FK` : Foreign Key
- `PK` : Primary Key
- `✓` : Enabled
- `✗` : Disabled

