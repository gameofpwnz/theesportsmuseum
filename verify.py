#!/usr/bin/env python3
"""
Verify all required files are present
"""

import os
from pathlib import Path

def check_files():
    """Check all required files exist"""
    
    print("🔍 Checking Esports Museum Files...\n")
    
    required_files = {
        "Root Files": [
            ".gitignore",
            "README.md",
            "QUICKSTART.md",
            "WORKFLOW.md",
            "FIELDS.md",
            "requirements.txt",
            "schema.sql",
            "example-data.json"
        ],
        "GitHub Actions": [
            ".github/workflows/deploy.yml"
        ],
        "Scripts": [
            "scripts/build.py",
            "scripts/migrate.py"
        ],
        "Templates": [
            "templates/base.html",
            "templates/index.html",
            "templates/browse.html",
            "templates/record.html",
            "templates/steward.html",
            "templates/about.html"
        ],
        "Static Files": [
            "static/css/main.css",
            "static/js/main.js"
        ]
    }
    
    all_good = True
    missing_files = []
    
    for category, files in required_files.items():
        print(f"📁 {category}")
        for file in files:
            if Path(file).exists():
                size = Path(file).stat().st_size
                print(f"  ✅ {file} ({size:,} bytes)")
            else:
                print(f"  ❌ {file} - MISSING!")
                missing_files.append(file)
                all_good = False
        print()
    
    # Check directories
    print("📂 Directories")
    dirs = ["scripts", "templates", "static/css", "static/js", "static/images", ".github/workflows"]
    for directory in dirs:
        if Path(directory).exists():
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - MISSING!")
            all_good = False
    print()
    
    # Summary
    print("="*60)
    if all_good:
        print("✅ ALL FILES PRESENT!")
        print("\nNext steps:")
        print("1. Run: pip install jinja2")
        print("2. Run: python scripts/migrate.py example-data.json")
        print("3. Run: python scripts/build.py")
        print("4. Test: cd output && python -m http.server")
        print("5. Push to GitHub!")
    else:
        print("❌ MISSING FILES!")
        print(f"\nMissing {len(missing_files)} file(s):")
        for f in missing_files:
            print(f"  - {f}")
        print("\nPlease ensure all files are copied from esports-museum-github folder")
    print("="*60)
    
    return all_good

if __name__ == '__main__':
    check_files()
