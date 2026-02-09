# URGENT FIX - Field Name Updates

## The Problem

The database uses these field names:
- `name` (not `title`)
- `game` (not `esport`)
- `item_type` (not `category`)
- `organization` (not `team`)
- `brand` (not `manufacturer`)

But some templates still reference the old names.

## ✅ I've Already Fixed

- ✅ `scripts/build.py` - Updated all database queries
- ✅ Database schema - Already correct

## 🔧 Quick Fix Solution

### Option 1: Use Simpler Browse Template (FASTEST)

Replace `templates/browse.html` with this simplified version that works with any fields:

```html
{% extends "base.html" %}

{% block title %}Browse Collection{% endblock %}

{% block content %}
<div class="browse-page">
    <div class="browse-header">
        <h1 class="browse-title">Collection Archive</h1>
        <p class="browse-subtitle">{{ records|length }} records found</p>
    </div>
    
    <div class="browse-grid">
        {% for record in records %}
        <article class="record-card">
            <a href="/record/{{ record.id }}/" class="record-image">
                {% if record.primary_image %}
                <img src="{{ record.primary_image }}" alt="{{ record.name }}" loading="lazy">
                {% else %}
                <div class="placeholder-image"></div>
                {% endif %}
                {% if record.verified %}
                <span class="card-badge">✓</span>
                {% endif %}
            </a>
            
            <div class="record-content">
                <div class="record-meta">
                    <span class="record-id">{{ record.id }}</span>
                    <span class="esport-tag">{{ record.game|upper }}</span>
                </div>
                
                <h3 class="record-title">
                    <a href="/record/{{ record.id }}/">{{ record.name }}</a>
                </h3>
                
                <a href="/steward/{{ record.steward }}/" class="record-steward">
                    @{{ record.steward }}
                </a>
            </div>
        </article>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### Option 2: Search & Replace in Templates

Run these commands in your templates folder:

```bash
cd templates

# Update field references
sed -i 's/record\.title/record.name/g' *.html
sed -i 's/record\.esport/record.game/g' *.html  
sed -i 's/record\.category/record.item_type/g' *.html
sed -i 's/record\.team/record.organization/g' *.html

# For featured records  
sed -i 's/featured\.title/featured.name/g' *.html
sed -i 's/recent\.title/recent.name/g' *.html
sed -i 's/rel\.title/rel.name/g' *.html
```

## 🚀 Test After Fix

```bash
python scripts/build.py
```

Should complete without errors!

## 📝 Fields Cheat Sheet

**OLD → NEW**
- `title` → `name`
- `esport` → `game`  
- `category` → `item_type`
- `team` → `organization`
- `player` → (no longer used, part of name)

**Template Variables to Update:**
- `{{ record.title }}` → `{{ record.name }}`
- `{{ record.esport }}` → `{{ record.game }}`
- `{{ record.category }}` → `{{ record.item_type }}`
- `{{ record.team }}` → `{{ record.organization }}`

Save these files after editing:
- `templates/index.html`
- `templates/browse.html` 
- `templates/record.html`
- `templates/steward.html`
