# Quick Start Guide

## 🚀 Get Your Museum Live in 5 Minutes

### Step 1: Setup Repository

```bash
# Create new repo on GitHub (or use existing)
# Clone it locally
git clone https://github.com/yourusername/esports-museum.git
cd esports-museum

# Copy all museum files into this directory
# (templates, static, scripts, schema.sql, etc.)
```

### Step 2: Create Your Database

**Option A: Start with Example Data**
```bash
pip install jinja2
python scripts/migrate.py example-data.json
```

**Option B: Start Fresh**
```bash
python
>>> import sqlite3
>>> conn = sqlite3.connect('museum.db')
>>> with open('schema.sql') as f:
>>>     conn.executescript(f.read())
>>> conn.close()
```

### Step 3: Test Locally

```bash
# Build the site
python scripts/build.py

# Check it worked
ls output/index.html  # Should exist

# Serve locally
cd output
python -m http.server 8000
# Visit http://localhost:8000
```

### Step 4: Enable GitHub Pages

1. Push your code:
```bash
git add .
git commit -m "Initial museum setup"
git push origin main
```

2. On GitHub.com:
   - Go to repository → Settings → Pages
   - Source: Select "GitHub Actions"
   - Save

3. Watch it deploy:
   - Go to Actions tab
   - See "Build and Deploy Museum" running
   - Wait 1-2 minutes

4. **Your site is live!**
   - Visit `https://yourusername.github.io/esports-museum/`

## 🎯 Daily Workflow

### Adding Records

1. **Update database**:
```bash
# Edit museum.db directly, or
python scripts/migrate.py new-records.json
```

2. **Test locally** (optional but recommended):
```bash
python scripts/build.py
cd output && python -m http.server
```

3. **Push to GitHub**:
```bash
git add museum.db
git commit -m "Added 3 new championship jerseys"
git push
```

4. **GitHub Actions deploys automatically!**
   - Check Actions tab to watch progress
   - Site updates in 1-2 minutes

## 📁 File Overview

**Must Have (tracked in git)**
- `museum.db` - Your database (track this!)
- `schema.sql` - Database structure
- `.github/workflows/deploy.yml` - Auto-deploy config
- `scripts/build.py` - Site generator
- `templates/*.html` - Page templates
- `static/` - CSS, JS, images

**Generated (git-ignored)**
- `output/` - Built site (don't track this)

## ✅ Checklist

Before going live:
- [ ] Database has at least one record
- [ ] Built locally and checked it works
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] Pushed to main branch
- [ ] GitHub Actions workflow ran successfully
- [ ] Site accessible at github.io URL

Optional customization:
- [ ] Update colors in `static/css/main.css`
- [ ] Edit mission in `templates/about.html`
- [ ] Add sponsor logos to `static/images/`
- [ ] Configure custom domain

## 🎨 Common Customizations

### Change Brand Colors
Edit `static/css/main.css`:
```css
:root {
    --color-accent: #ff4655;  /* Your color here */
}
```

### Update Footer Links
Edit `templates/base.html` - find the footer section

### Add Google Analytics
Add to `templates/base.html` in the `<head>` section

### Custom Domain
1. GitHub Settings → Pages → Custom domain
2. Add CNAME to your DNS: `yourusername.github.io`

## 🆘 Troubleshooting

**Build fails on GitHub?**
- Check Actions tab for error message
- Make sure Jinja2 is in deploy.yml dependencies
- Test locally first: `python scripts/build.py`

**Site shows 404?**
- Verify GitHub Pages is enabled
- Check Actions tab - did workflow succeed?
- Wait a few minutes for DNS propagation

**Search not working?**
- Check `output/static/search-index.json` exists
- Verify `static/js/main.js` was copied

**Images not loading?**
- Use full URLs: `https://example.com/image.jpg`
- Or place in `static/images/` and use `/static/images/image.jpg`

## 📊 Example Database Operations

### Add a Record
```python
import sqlite3, json

conn = sqlite3.connect('museum.db')
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO records (
        id, title, description, category, esport, 
        steward, year, verified, tags
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    'CE-042',
    'Scump OpTic Jersey 2017',
    'Championship-winning jersey from CWL',
    'jerseys',
    'cod',
    'myusername',
    2017,
    1,
    json.dumps(['optic', 'scump', 'championship'])
))

# Add image
cursor.execute("""
    INSERT INTO media (record_id, type, url, is_primary)
    VALUES (?, ?, ?, ?)
""", ('CE-042', 'image', 'https://example.com/jersey.jpg', 1))

conn.commit()
conn.close()
```

### Mark as Verified
```python
import sqlite3
conn = sqlite3.connect('museum.db')
cursor = conn.cursor()

cursor.execute("""
    UPDATE records 
    SET verified = 1, verification_date = '2025-02-08'
    WHERE id = 'CE-042'
""")

conn.commit()
conn.close()
```

## 🎉 You're Done!

You now have:
- ✅ Free hosting on GitHub Pages
- ✅ Automatic deployments
- ✅ Professional museum site
- ✅ Easy content management

Just update your database and push!
