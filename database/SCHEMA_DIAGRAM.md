# Database Schema Diagram

## Entity Relationship Diagram

```
┌─────────────────────────────┐
│         DRIVER              │
│         (Parent)            │
├─────────────────────────────┤
│ id (UUID) PK                │◄─────┐
│ feature (VARCHAR)           │      │
│ datetime (TIMESTAMP)        │      │
└─────────────────────────────┘      │
                                     │
                                     │ Foreign Key
                    ┌────────────────┴────────────────┐
                    │                                 │
       ┌────────────▼──────────────┐   ┌─────────────▼─────────────┐
       │        SINGLE             │   │      CSV_UPLOAD           │
       │        (Child)            │   │        (Child)            │
       ├───────────────────────────┤   ├───────────────────────────┤
       │ id (UUID) PK, FK          │   │ id (UUID) PK, FK          │
       │ input (VARCHAR)           │   │ filename (VARCHAR)        │
       │ datetime (TIMESTAMP)      │   │ contents (JSONB)          │
       └───────────────────────────┘   │ datetime (TIMESTAMP)      │
                                       └───────────────────────────┘
```

## Relationships

- **Driver → Single**: One-to-Zero-or-One
  - A Driver record with `feature='single_text'` has exactly one Single record
  - The Single.id references Driver.id (foreign key)
  - Cascade delete: Deleting a Driver record deletes its Single record

- **Driver → CSV_Upload**: One-to-Zero-or-One
  - A Driver record with `feature='csv_upload'` has exactly one CSV_Upload record
  - The CSV_Upload.id references Driver.id (foreign key)
  - Cascade delete: Deleting a Driver record deletes its CSV_Upload record

## Example Data Flow

### Scenario 1: User enters single text "Hello World"

```
Step 1: Insert into Driver
┌──────────────────────────────────────┐
│ id: 550e8400-e29b-41d4-a716-446655440000 │
│ feature: 'single_text'                    │
│ datetime: 2024-10-28 14:30:00            │
└──────────────────────────────────────┘

Step 2: Insert into Single (using same id)
┌──────────────────────────────────────┐
│ id: 550e8400-e29b-41d4-a716-446655440000 │ ◄── Same ID!
│ input: 'Hello World'                      │
│ datetime: 2024-10-28 14:30:00            │
└──────────────────────────────────────┘
```

### Scenario 2: User uploads CSV file "names.csv"

```
Step 1: Insert into Driver
┌──────────────────────────────────────┐
│ id: 7c9e6679-7425-40de-944b-e07fc1f90ae7 │
│ feature: 'csv_upload'                     │
│ datetime: 2024-10-28 14:35:00            │
└──────────────────────────────────────┘

Step 2: Insert into CSV_Upload (using same id)
┌──────────────────────────────────────┐
│ id: 7c9e6679-7425-40de-944b-e07fc1f90ae7 │ ◄── Same ID!
│ filename: 'names.csv'                     │
│ contents: {"names": [...], "count": 10}   │
│ datetime: 2024-10-28 14:35:00            │
└──────────────────────────────────────┘
```

## Query Examples

### Get all operations with their type
```sql
SELECT id, feature, datetime 
FROM driver 
ORDER BY datetime DESC;
```

### Get single text operations with full details
```sql
SELECT d.id, d.feature, d.datetime, s.input
FROM driver d
INNER JOIN single s ON d.id = s.id
WHERE d.feature = 'single_text';
```

### Get CSV upload operations with full details
```sql
SELECT d.id, d.feature, d.datetime, c.filename, c.contents
FROM driver d
INNER JOIN csv_upload c ON d.id = c.id
WHERE d.feature = 'csv_upload';
```

### Get complete details for a specific operation
```sql
SELECT 
    d.id,
    d.feature,
    d.datetime,
    s.input as single_input,
    c.filename as csv_filename
FROM driver d
LEFT JOIN single s ON d.id = s.id
LEFT JOIN csv_upload c ON d.id = c.id
WHERE d.id = '550e8400-e29b-41d4-a716-446655440000';
```

## Benefits of This Design

1. **Single Source of Truth**: All operations tracked in Driver table
2. **Type Safety**: Foreign key constraints ensure data integrity
3. **Efficient Queries**: Can query Driver alone or JOIN for details
4. **Clear Separation**: Operation metadata vs. operation-specific data
5. **Easy Analytics**: Count operations by type, track usage patterns
6. **Cascade Protection**: Deleting parent automatically cleans up children
