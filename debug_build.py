#!/usr/bin/env python3
"""
Debug script - check what files were actually generated
"""

import os
from pathlib import Path

def check_output():
    """Check what was generated in output directory"""
    
    output_dir = Path('output')
    
    if not output_dir.exists():
        print("❌ output/ directory doesn't exist!")
        print("Run: python scripts/build.py")
        return
    
    print("📂 Checking output directory...\n")
    
    # Check main pages
    print("Main Pages:")
    for page in ['index.html', 'about/index.html', 'browse/index.html']:
        path = output_dir / page
        if path.exists():
            print(f"  ✅ {page}")
        else:
            print(f"  ❌ {page} - MISSING")
    
    # Check record pages
    print("\nRecord Pages:")
    record_dir = output_dir / 'record'
    if record_dir.exists():
        records = list(record_dir.glob('*/index.html'))
        if records:
            for rec in records:
                print(f"  ✅ {rec.parent.name}/index.html")
        else:
            print("  ❌ No record pages found")
    else:
        print("  ❌ record/ directory doesn't exist")
    
    # Check steward pages
    print("\nSteward Pages:")
    steward_dir = output_dir / 'steward'
    if steward_dir.exists():
        stewards = list(steward_dir.glob('*/index.html'))
        if stewards:
            for st in stewards:
                print(f"  ✅ {st.parent.name}/index.html")
        else:
            print("  ❌ No steward pages found")
    else:
        print("  ❌ steward/ directory doesn't exist")
    
    # Check static files
    print("\nStatic Files:")
    for static_file in ['static/css/main.css', 'static/js/main.js', 'static/search-index.json']:
        path = output_dir / static_file
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {static_file} ({size:,} bytes)")
        else:
            print(f"  ❌ {static_file} - MISSING")
    
    # Full file count
    print(f"\nTotal HTML files: {len(list(output_dir.rglob('*.html')))}")
    print(f"Total files: {len(list(output_dir.rglob('*.*')))}")
    
    # Show record links in browse page
    print("\nChecking links in browse page...")
    browse_html = output_dir / 'browse/index.html'
    if browse_html.exists():
        with open(browse_html) as f:
            content = f.read()
            if 'href="record/' in content:
                print("  ✅ Found record links: href=\"record/...")
            elif 'href="/record/' in content:
                print("  ⚠️  Found absolute links: href=\"/record/...")
            elif 'href="../record/' in content:
                print("  ✅ Found relative links: href=\"../record/...")
            else:
                print("  ❌ No record links found!")

if __name__ == '__main__':
    check_output()
