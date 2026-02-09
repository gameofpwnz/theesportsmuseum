#!/usr/bin/env python3
"""
Data Migration Script
Converts JSON data to SQLite database with updated field structure
Fields: Name, Organization, Brand, Game, Item Type, Badges, Year, Steward, 
        Rarity, Availability, Condition, Chain of Custody
"""

import sqlite3
import json
from pathlib import Path

def migrate_data(json_file='example-data.json', db_file='museum.db'):
    """
    Migrate JSON data to SQLite database
    """
    print("Starting data migration...")
    print(f"Source: {json_file}")
    print(f"Target: {db_file}\n")
    
    # Load JSON data
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data)} records from JSON")
    except FileNotFoundError:
        print(f"❌ Error: {json_file} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        return False
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Initialize schema
    print("Initializing database schema...")
    try:
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
        print("✓ Database schema created")
    except FileNotFoundError:
        print("❌ Error: schema.sql not found")
        return False
    
    # Migrate records
    print("\nMigrating records...")
    records_added = 0
    media_added = 0
    stewards = set()
    errors = []
    
    for item in data:
        try:
            # Convert lists to JSON strings
            badges_json = json.dumps(item.get('badges', [])) if item.get('badges') else None
            tags_json = json.dumps(item.get('tags', [])) if item.get('tags') else None
            custody_json = json.dumps(item.get('chain_of_custody', [])) if item.get('chain_of_custody') else None
            
            # Insert record with new field structure
            cursor.execute("""
                INSERT INTO records (
                    id, name, organization, brand, game, item_type,
                    badges, tags, year, steward, steward_link, rarity, 
                    availability, condition, chain_of_custody,
                    description, notes, verified, verification_date,
                    verification_notes, featured, featured_order, 
                    date_added
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get('id'),
                item.get('name'),
                item.get('organization'),
                item.get('brand'),
                item.get('game'),
                item.get('item_type'),
                badges_json,
                tags_json,
                item.get('year'),
                item.get('steward'),
                item.get('steward_link'),
                item.get('rarity'),
                item.get('availability'),
                item.get('condition'),
                custody_json,
                item.get('description'),
                item.get('notes'),
                1 if item.get('verified') else 0,
                item.get('verification_date'),
                item.get('verification_notes'),
                1 if item.get('featured') else 0,
                item.get('featured_order'),
                item.get('date_added')
            ))
            records_added += 1
            print(f"  ✓ {item.get('id')}: {item.get('name')}")
            
            # Track steward
            stewards.add(item.get('steward'))
            
            # Insert media
            if 'media' in item and item['media']:
                for idx, media in enumerate(item['media']):
                    cursor.execute("""
                        INSERT INTO media (
                            record_id, type, url, caption, display_order, is_primary
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        item.get('id'),
                        media.get('type', 'image'),
                        media.get('url'),
                        media.get('caption'),
                        idx,
                        1 if media.get('is_primary', idx == 0) else 0
                    ))
                    media_added += 1
            
        except Exception as e:
            error_msg = f"Error migrating record {item.get('id', 'UNKNOWN')}: {e}"
            errors.append(error_msg)
            print(f"  ❌ {error_msg}")
            continue
    
    # Create steward entries
    print("\nCreating steward entries...")
    for steward in stewards:
        cursor.execute("""
            INSERT OR IGNORE INTO stewards (username)
            VALUES (?)
        """, (steward,))
    print(f"✓ {len(stewards)} stewards registered")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    # Print summary
    print("\n" + "="*60)
    print("MIGRATION COMPLETE!")
    print("="*60)
    print(f"✓ Records migrated: {records_added}")
    print(f"✓ Media items added: {media_added}")
    print(f"✓ Stewards registered: {len(stewards)}")
    
    if errors:
        print(f"\n⚠  Errors encountered: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    
    print(f"\n✓ Database saved to: {db_file}")
    print("\nNext steps:")
    print("1. Test the build: python scripts/build.py")
    print("2. Push to GitHub: git add museum.db && git commit && git push")
    print()
    
    return len(errors) == 0

def verify_migration(db_file='museum.db'):
    """
    Verify the migration was successful
    """
    print("\n" + "="*60)
    print("VERIFYING MIGRATION")
    print("="*60)
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check record counts
        cursor.execute("SELECT COUNT(*) FROM records")
        record_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM media")
        media_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stewards")
        steward_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM records WHERE verified = 1")
        verified_count = cursor.fetchone()[0]
        
        print(f"\nDatabase Statistics:")
        print(f"  Total Records: {record_count}")
        print(f"  Total Media: {media_count}")
        print(f"  Total Stewards: {steward_count}")
        print(f"  Verified Records: {verified_count}")
        
        # Show sample records with new fields
        print(f"\nSample Records:")
        cursor.execute("""
            SELECT id, name, organization, game, item_type, year, steward
            FROM records
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")
            print(f"    Organization: {row[2] or 'N/A'}")
            print(f"    Game: {row[3]} | Type: {row[4]} | Year: {row[5] or 'N/A'}")
            print(f"    Steward: {row[6]}\n")
        
        # Check for chain of custody examples
        cursor.execute("""
            SELECT id, name, chain_of_custody
            FROM records
            WHERE chain_of_custody IS NOT NULL
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            print(f"Chain of Custody Example:")
            print(f"  Record: {result[0]} - {result[1]}")
            custody = json.loads(result[2])
            print(f"  Custody Events: {len(custody)}")
            for event in custody:
                print(f"    {event.get('date')}: {event.get('from')} → {event.get('to')} ({event.get('method')})")
        
        conn.close()
        print("\n✓ Verification complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'example-data.json'
    db_file = sys.argv[2] if len(sys.argv) > 2 else 'museum.db'
    
    # Remove existing database if requested
    if '--fresh' in sys.argv or not Path(db_file).exists():
        if Path(db_file).exists():
            print(f"Removing existing database: {db_file}\n")
            Path(db_file).unlink()
    
    # Run migration
    success = migrate_data(json_file, db_file)
    
    if success:
        verify_migration(db_file)
        print("\n✅ Ready to build! Run: python scripts/build.py")
        exit(0)
    else:
        print("\n❌ Migration failed. Please fix errors and try again.")
        exit(1)
