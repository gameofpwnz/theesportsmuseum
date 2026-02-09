# 👋 START HERE

Welcome to your Esports Collectors Museum!

## 🎯 What You Have

This is a **complete, ready-to-deploy** museum website that:
- ✅ Generates static pages from your SQLite database
- ✅ Automatically deploys via GitHub Actions when you push changes
- ✅ Hosts for FREE on GitHub Pages
- ✅ Has a beautiful, custom design
- ✅ Supports all your fields (Name, Organization, Brand, Game, etc.)

## 🚀 Quick Start (5 Minutes)

### 1. Verify You Have Everything

```bash
cd esports-museum-github
python verify.py
```

Should show all ✅ checkmarks. If not, you're missing files!

### 2. Create Your Database

```bash
pip install jinja2
python scripts/migrate.py example-data.json
```

This creates `museum.db` with 2 example records.

### 3. Test It Works

```bash
python scripts/build.py
cd output
python -m http.server 8000
```

Visit `http://localhost:8000` - you should see your museum!

### 4. Push to GitHub

```bash
cd ..
git init
git add -A
git commit -m "Initial museum setup"
git remote add origin https://github.com/YOUR-USERNAME/esports-museum.git
git push -u origin main
```

### 5. Enable GitHub Pages

1. Go to your repo on GitHub
2. Settings → Pages
3. Source: **GitHub Actions**
4. Save

### 6. Done! 🎉

Your site will be live at:
```
https://YOUR-USERNAME.github.io/esports-museum/
```

## 📚 Documentation

- **SETUP.md** - Complete step-by-step setup guide
- **FIELDS.md** - What each database field means
- **QUICKSTART.md** - Fast deployment guide
- **WORKFLOW.md** - How GitHub Actions automation works
- **README.md** - Full project documentation

## 🗂️ Project Structure

```
esports-museum-github/
├── .github/workflows/deploy.yml   ← GitHub Actions (auto-deploy)
├── scripts/
│   ├── build.py                   ← Generates static HTML
│   └── migrate.py                 ← Creates database from JSON
├── templates/                     ← Page layouts (6 files)
├── static/                        ← CSS, JS, images
├── schema.sql                     ← Database structure
├── example-data.json              ← Sample records
└── museum.db                      ← Your database (create with migrate.py)
```

## ✏️ Adding Your Records

### Option 1: Use JSON

Create `my-records.json`:
```json
[
  {
    "id": "CE-001",
    "name": "My Item Name",
    "game": "Call of Duty",
    "item_type": "jersey",
    "steward": "myusername",
    "organization": "OpTic Gaming",
    "year": 2024
  }
]
```

Then:
```bash
python scripts/migrate.py my-records.json
git add museum.db
git commit -m "Added new items"
git push
```

### Option 2: Direct Database

```python
import sqlite3, json

conn = sqlite3.connect('museum.db')
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO records (id, name, game, item_type, steward, organization, year)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", ('CE-042', 'My Jersey', 'Call of Duty', 'jersey', 'myusername', 'FaZe Clan', 2024))

conn.commit()
conn.close()
```

See **FIELDS.md** for all available fields!

## 🎨 Customizing Design

### Colors
Edit `static/css/main.css`:
```css
:root {
    --color-accent: #ff4655;  /* Change this! */
}
```

### Content
Edit `templates/about.html` for your mission/about page.

### Sponsors
Add logos to `static/images/` and update footer in `templates/base.html`.

## 🆘 Need Help?

### Files Missing?
```bash
python verify.py
```

### Build Errors?
Check `scripts/build.py` error messages. Common issues:
- Database file not found
- Jinja2 not installed

### GitHub Actions Not Running?
- Make sure `.github/workflows/deploy.yml` exists
- Check you selected "GitHub Actions" in Pages settings
- Look at Actions tab for errors

### Site Shows 404?
- Wait 2-3 minutes after first deployment
- Check workflow completed (green checkmark in Actions tab)

## 📋 Your Checklist

- [ ] All files verified (`python verify.py`)
- [ ] Database created (`museum.db` exists)
- [ ] Built successfully (`python scripts/build.py`)
- [ ] Tested locally (works at localhost:8000)
- [ ] Pushed to GitHub
- [ ] GitHub Pages enabled (Settings → Pages → GitHub Actions)
- [ ] Workflow completed (Actions tab shows ✅)
- [ ] Site is live!

## 🎯 What's Next?

1. **Add your real data** - Replace example-data.json with your records
2. **Customize styling** - Update colors in main.css
3. **Add images** - Put them in static/images/
4. **Write about page** - Edit templates/about.html
5. **Share your museum** - Send the link to collectors!

## 💡 Pro Tips

- **Test locally first** - Always run `python scripts/build.py` before pushing
- **Commit database** - Your `museum.db` file should be tracked in git
- **Use chain of custody** - Great for provenance documentation
- **Add badges** - Makes items stand out (["Signed", "World Champion"])
- **Verify important items** - Set `verified: true` for authenticated pieces

## 🎉 You're Ready!

Everything you need is here. Follow the steps above and your museum will be live in minutes!

Questions? Check the docs or the error messages - they're very helpful!

Good luck! 🚀
