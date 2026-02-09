# Esports Collectors Museum
## Static Site with GitHub Actions Auto-Deployment

A museum archive for esports memorabilia with **automatic deployment via GitHub Actions**. Push your database changes and the site rebuilds and deploys automatically!

## 🎯 How It Works

```
You update database → Push to GitHub → Actions builds site → Deploys to GitHub Pages
```

**No servers, no hosting costs, completely automated!**

## ✨ Features

- **Static HTML generation** from SQLite database
- **GitHub Actions** automatically build and deploy
- **Individual pages** for each record (SEO-friendly)
- **Client-side search** with JSON index
- **Mobile-responsive** design
- **Free hosting** on GitHub Pages

## 🚀 Quick Setup

### 1. Initial Setup

```bash
# Clone or create your repository
git clone https://github.com/yourusername/esports-museum.git
cd esports-museum

# Install Python dependencies
pip install jinja2

# Create your database (or migrate existing data)
python scripts/migrate.py example-data.json
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Settings → Pages
3. Source: **GitHub Actions**
4. Save

### 3. Push to GitHub

```bash
git add .
git commit -m "Initial museum setup"
git push origin main
```

**That's it!** GitHub Actions will automatically:
- Build all static pages
- Deploy to GitHub Pages
- Your site will be live at `https://yourusername.github.io/esports-museum/`

## 📁 Project Structure

```
esports-museum/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── scripts/
│   ├── build.py               # Static site generator
│   └── migrate.py             # JSON to SQLite migration
├── templates/                 # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── browse.html
│   ├── record.html
│   ├── steward.html
│   └── about.html
├── static/                    # CSS, JS, images
│   ├── css/main.css
│   ├── js/main.js
│   └── images/
├── museum.db                  # SQLite database
├── schema.sql                 # Database schema
└── output/                    # Generated site (git-ignored)
```

## 💾 Working with Data

### Adding New Records

**Option 1: Direct Database**
```python
import sqlite3
conn = sqlite3.connect('museum.db')
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO records (id, title, description, category, esport, steward, year, verified)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", ('CE-004', 'My New Jersey', 'Description...', 'jerseys', 'cod', 'myusername', 2024, 0))

conn.commit()
conn.close()
```

**Option 2: Migrate from JSON**
```bash
# Add records to example-data.json, then:
python scripts/migrate.py example-data.json
```

### Pushing Updates

```bash
git add museum.db
git commit -m "Added 5 new records"
git push
```

GitHub Actions will automatically rebuild and redeploy!

## 🎨 Customization

### Update Styles

Edit `static/css/main.css` and push:

```bash
git add static/css/main.css
git commit -m "Updated color scheme"
git push
```

### Modify Templates

Edit files in `templates/` directory:

```bash
git add templates/
git commit -m "Updated homepage layout"
git push
```

### Change Content

Edit `templates/about.html` for mission/about page.

## 🔍 How Search Works

The build script generates `static/search-index.json` with all records. The JavaScript (`static/js/main.js`) loads this file and performs client-side filtering for instant search results.

## 📊 Database Schema

Your records support 30+ fields:

**Core**
- id, title, description, category, esport

**Provenance**
- steward, verified, verification_date, authenticity_notes

**Historical**
- year, season, event, team, player, achievement

**Physical**
- size, condition, material, manufacturer, serial_number

**Acquisition**
- acquisition_date, acquisition_method, acquisition_source

**Curation**
- featured, display_priority, curator_notes, view_count

See `schema.sql` for complete structure.

## 🔧 Local Development

Test your site locally before pushing:

```bash
# Build the site
python scripts/build.py

# Serve locally (Python 3)
cd output
python -m http.server 8000

# Visit: http://localhost:8000
```

## 🚀 GitHub Actions Workflow

The `.github/workflows/deploy.yml` file handles everything:

1. **Triggers**: Runs when you push changes to `main` branch
2. **Builds**: Runs `scripts/build.py` to generate static site
3. **Deploys**: Publishes `output/` directory to GitHub Pages

### Manual Trigger

You can also manually trigger a rebuild:
1. Go to Actions tab on GitHub
2. Select "Build and Deploy Museum"
3. Click "Run workflow"

## 📝 Content Guidelines

### Record IDs
Format: `CE-###` (Collectors Envy Museum numbering)

### Titles
Be specific: "Item Type - Player/Team - Event/Year"

Example: `OpTic Gaming Championship Jersey - Scump - CWL 2017`

### Descriptions
- 100-300 words
- Start with significance
- Include historical context
- Mention unique characteristics

### Images
- Min 1200px width
- Multiple angles
- Clean backgrounds
- Proper lighting

## 🎯 SEO Benefits

Static sites are SEO-friendly:
- ✅ Individual URLs for each record
- ✅ Fast page loads (pre-generated HTML)
- ✅ Proper meta tags
- ✅ Clean URL structure

## 🔐 Verification System

Mark records as verified in database:

```sql
UPDATE records SET verified = 1, verification_date = '2025-02-08' 
WHERE id = 'CE-001';
```

Verified records show:
- Blue verification badge
- Enhanced styling
- Verification date in provenance

## 📱 Mobile Support

Fully responsive design:
- **Desktop**: Multi-column layouts
- **Tablet**: 2-column grids
- **Mobile**: Single column, hamburger menu

## ⚡ Performance

Static sites are FAST:
- No database queries at runtime
- No server processing
- Just HTML + CSS + minimal JS
- Global CDN via GitHub Pages

## 🔄 Typical Workflow

```bash
# 1. Add records to database locally
python scripts/migrate.py new-records.json

# 2. Test locally
python scripts/build.py
cd output && python -m http.server

# 3. Push when satisfied
git add museum.db
git commit -m "Added 10 new jerseys from MLG era"
git push

# 4. GitHub Actions deploys automatically!
```

## 🆘 Troubleshooting

### Build Fails on GitHub

Check Actions tab for error logs. Common issues:
- Missing Jinja2 dependency (check deploy.yml)
- Database file corruption
- Template syntax errors

### Search Not Working

Ensure `search-index.json` was generated:
```bash
python scripts/build.py
ls output/static/search-index.json
```

### Images Not Loading

Check image paths in database - they should be:
- Absolute URLs (https://...)
- Or relative to `/static/images/`

### Custom Domain

In repository settings → Pages → Custom domain:
1. Add your domain (e.g., `museum.collectorsenvy.com`)
2. Add CNAME record in your DNS:
   - Type: CNAME
   - Name: museum
   - Value: yourusername.github.io

## 🎉 You're Ready!

Your museum is now:
- ✅ Hosted for free on GitHub Pages
- ✅ Auto-deploys on every push
- ✅ Blazing fast (static HTML)
- ✅ SEO-optimized
- ✅ Fully customizable

Just push database changes and let GitHub Actions handle the rest!

## 📧 Need Help?

- Check the GitHub Actions logs in the Actions tab
- Review `scripts/build.py` for generation logic
- Test locally before pushing

## 🔗 Links

- **Collectors Envy**: https://collectorsenvy.com
- **Submit Records**: https://forms.gle/hrbaadeGTpLCaeYj7

---

Built with ❤️ by the esports collecting community
