#!/usr/bin/env python3
"""
Static Site Generator for Esports Museum
Generates static HTML from SQLite database using Jinja2
"""

import sqlite3
import json
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import datetime

class MuseumSiteGenerator:
    def __init__(self, db_path='museum.db', output_dir='output'):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.templates_dir = Path('templates')
        self.static_dir = Path('static')
        
        # Setup Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )
        self.jinja_env.filters['formatdate'] = self.format_date
        
    def format_date(self, date_str):
        """Format date string"""
        if not date_str:
            return ''
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%B %d, %Y')
        except:
            return date_str
    
    def clean_output(self):
        """Remove old output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        print(f"✓ Cleaned output directory: {self.output_dir}")
        
    def copy_static_files(self):
        """Copy CSS, JS, images to output"""
        print("Copying static files...")
        output_static = self.output_dir / 'static'
        if self.static_dir.exists():
            shutil.copytree(self.static_dir, output_static)
            print(f"✓ Copied static files to: {output_static}")
        else:
            print("⚠ Static directory not found")
    
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_stats(self, conn):
        """Get museum statistics"""
        cursor = conn.cursor()
        stats = cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT steward) as total_stewards,
                CAST(SUM(CASE WHEN verified = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as verified_percent,
                MIN(year) as earliest_year
            FROM records
            WHERE year > 0
        """).fetchone()
        return dict(stats) if stats else {}
    
    def get_all_records(self, conn):
        """Get all records with primary images"""
        cursor = conn.cursor()
        records = cursor.execute("""
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            ORDER BY date_added DESC
        """).fetchall()
        return [dict(r) for r in records]
    
    def get_featured_records(self, conn, limit=2):
        """Get featured records"""
        cursor = conn.cursor()
        records = cursor.execute("""
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            WHERE featured = 1
            ORDER BY featured_order, date_added DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in records]
    
    def get_recent_records(self, conn, limit=8):
        """Get recent records"""
        cursor = conn.cursor()
        records = cursor.execute("""
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            ORDER BY date_added DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in records]
    
    def get_record_with_media(self, conn, record_id):
        """Get single record with all media"""
        cursor = conn.cursor()
        
        record = cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
        if not record:
            return None
        
        media = cursor.execute("""
            SELECT * FROM media 
            WHERE record_id = ? 
            ORDER BY display_order, id
        """, (record_id,)).fetchall()
        
        result = dict(record)
        result['media'] = [dict(m) for m in media]
        
        # Handle badges (may or may not exist)
        try:
            result['badges'] = json.loads(record['badges']) if record['badges'] else []
        except (KeyError, IndexError):
            result['badges'] = []
        
        # Handle tags (may or may not exist)
        try:
            result['tags'] = json.loads(record['tags']) if record['tags'] else []
        except (KeyError, IndexError):
            result['tags'] = []
        
        # Handle chain of custody (may or may not exist)
        try:
            result['chain_of_custody'] = json.loads(record['chain_of_custody']) if record['chain_of_custody'] else []
        except (KeyError, IndexError):
            result['chain_of_custody'] = []
        
        return result
    
    def get_related_records(self, conn, record_id, game, organization, brand):
        """Get related records"""
        cursor = conn.cursor()
        related = cursor.execute("""
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            WHERE id != ? 
            AND (game = ? OR organization = ? OR brand = ?)
            ORDER BY RANDOM()
            LIMIT 4
        """, (record_id, game or '', organization or '', brand or '')).fetchall()
        return [dict(r) for r in related]
    
    def get_steward_info(self, conn, username):
        """Get steward information"""
        cursor = conn.cursor()
        steward = cursor.execute("""
            SELECT * FROM stewards WHERE username = ?
        """, (username,)).fetchone()
        return dict(steward) if steward else {'username': username}
    
    def get_steward_records(self, conn, username):
        """Get all records by steward"""
        cursor = conn.cursor()
        records = cursor.execute("""
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            WHERE steward = ?
            ORDER BY date_added DESC
        """, (username,)).fetchall()
        return [dict(r) for r in records]
    
    def get_all_stewards(self, conn):
        """Get all unique stewards"""
        cursor = conn.cursor()
        stewards = cursor.execute("""
            SELECT DISTINCT steward FROM records ORDER BY steward
        """).fetchall()
        return [s['steward'] for s in stewards]
    
    def get_filtered_records(self, conn, item_type='all', game='all', era='all'):
        """Get filtered records"""
        cursor = conn.cursor()
        
        query = """
            SELECT r.*,
                   (SELECT url FROM media WHERE record_id = r.id AND is_primary = 1 LIMIT 1) as primary_image
            FROM records r
            WHERE 1=1
        """
        params = []
        
        if item_type != 'all':
            query += " AND item_type = ?"
            params.append(item_type)
        
        if game != 'all':
            query += " AND game = ?"
            params.append(game)
        
        if era != 'all':
            if era == 'golden':
                query += " AND year <= 2015"
            elif era == 'global':
                query += " AND year > 2015 AND year <= 2020"
            elif era == 'modern':
                query += " AND year > 2020"
        
        query += " ORDER BY display_priority DESC, date_added DESC"
        
        records = cursor.execute(query, params).fetchall()
        return [dict(r) for r in records]
    
    def write_file(self, path, content):
        """Write content to file"""
        file_path = self.output_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_homepage(self, conn):
        """Generate homepage"""
        print("Generating homepage...")
        
        template = self.jinja_env.get_template('index.html')
        
        context = {
            'stats': self.get_stats(conn),
            'featured': self.get_featured_records(conn),
            'recent': self.get_recent_records(conn),
            'base_path': ''  # Root level, no prefix
        }
        
        html = template.render(**context)
        self.write_file('index.html', html)
        print("✓ Generated: index.html")
    
    def generate_browse_pages(self, conn):
        """Generate browse pages for all filter combinations"""
        print("Generating browse pages...")
        
        template = self.jinja_env.get_template('browse.html')
        
        item_types = ['all', 'jersey', 'hardware', 'peripheral', 'signature', 'media', 'other']
        games = ['all', 'Call of Duty', 'Halo', 'Counter-Strike', 'Valorant', 'League of Legends', 'Rocket League']
        eras = ['all', 'golden', 'global', 'modern']
        
        pages_generated = 0
        
        # Generate main browse page
        context = {
            'records': self.get_filtered_records(conn),
            'item_type': 'all',
            'game': 'all',
            'era': 'all',
            'base_path': '../'  # One level deep
        }
        html = template.render(**context)
        self.write_file('browse/index.html', html)
        pages_generated += 1
        
        # Generate filtered pages
        for item_type in item_types:
            for game in games:
                for era in eras:
                    if item_type == 'all' and game == 'all' and era == 'all':
                        continue  # Already generated
                    
                    records = self.get_filtered_records(conn, item_type, game, era)
                    
                    context = {
                        'records': records,
                        'item_type': item_type,
                        'game': game,
                        'era': era,
                        'base_path': '../../'  # Two levels deep
                    }
                    
                    html = template.render(**context)
                    
                    # Create path
                    parts = []
                    if item_type != 'all':
                        parts.append(f"type-{item_type}")
                    if game != 'all':
                        game_slug = game.lower().replace(' ', '-')
                        parts.append(f"game-{game_slug}")
                    if era != 'all':
                        parts.append(f"era-{era}")
                    
                    if parts:
                        path = f"browse/{'-'.join(parts)}/index.html"
                        self.write_file(path, html)
                        pages_generated += 1
        
        print(f"✓ Generated {pages_generated} browse pages")
    
    def generate_record_pages(self, conn):
        """Generate individual record pages"""
        print("Generating record pages...")
        
        template = self.jinja_env.get_template('record.html')
        records = self.get_all_records(conn)
        
        for record in records:
            record_data = self.get_record_with_media(conn, record['id'])
            related = self.get_related_records(
                conn, 
                record['id'],
                record.get('game'),
                record.get('organization'),
                record.get('brand')
            )
            
            context = {
                'record': record_data,
                'related': related,
                'base_path': '../../'  # Two levels deep: /record/CE-001/
            }
            
            html = template.render(**context)
            self.write_file(f"record/{record['id']}/index.html", html)
        
        print(f"✓ Generated {len(records)} record pages")
    
    def generate_steward_pages(self, conn):
        """Generate steward profile pages"""
        print("Generating steward pages...")
        
        template = self.jinja_env.get_template('steward.html')
        stewards = self.get_all_stewards(conn)
        
        for username in stewards:
            steward_info = self.get_steward_info(conn, username)
            records = self.get_steward_records(conn, username)
            
            context = {
                'steward': steward_info,
                'records': records,
                'base_path': '../../'  # Two levels deep: /steward/username/
            }
            
            html = template.render(**context)
            self.write_file(f"steward/{username}/index.html", html)
        
        print(f"✓ Generated {len(stewards)} steward pages")
    
    def generate_about_page(self):
        """Generate about page"""
        print("Generating about page...")
        
        template = self.jinja_env.get_template('about.html')
        context = {'base_path': '../'}  # One level deep: /about/
        html = template.render(**context)
        self.write_file('about/index.html', html)
        print("✓ Generated: about/index.html")
    
    def generate_search_json(self, conn):
        """Generate search index JSON"""
        print("Generating search index...")
        
        records = self.get_all_records(conn)
        search_data = []
        
        for record in records:
            search_data.append({
                'id': record['id'],
                'name': record['name'],
                'description': record['description'],
                'item_type': record['item_type'],
                'game': record['game'],
                'steward': record['steward'],
                'organization': record.get('organization'),
                'brand': record.get('brand'),
                'year': record.get('year'),
                'primary_image': record.get('primary_image'),
                'url': f"/record/{record['id']}/"
            })
        
        self.write_file('static/search-index.json', json.dumps(search_data, indent=2))
        print(f"✓ Generated search index with {len(search_data)} records")
    
    def build(self):
        """Build entire static site"""
        print("\n" + "="*60)
        print("ESPORTS MUSEUM - STATIC SITE GENERATOR")
        print("="*60 + "\n")
        
        # Check if database exists
        if not Path(self.db_path).exists():
            print(f"❌ Error: Database not found at {self.db_path}")
            return False
        
        try:
            conn = self.get_db_connection()
            
            # Clean and setup
            self.clean_output()
            self.copy_static_files()
            
            # Generate all pages
            self.generate_homepage(conn)
            self.generate_browse_pages(conn)
            self.generate_record_pages(conn)
            self.generate_steward_pages(conn)
            self.generate_about_page()
            self.generate_search_json(conn)
            
            conn.close()
            
            print("\n" + "="*60)
            print("✅ BUILD COMPLETE!")
            print("="*60)
            print(f"\nStatic site generated in: {self.output_dir.absolute()}")
            print("\nNext steps:")
            print("1. Review the output/ directory")
            print("2. Push to GitHub")
            print("3. GitHub Actions will deploy automatically")
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    generator = MuseumSiteGenerator()
    success = generator.build()
    exit(0 if success else 1)
