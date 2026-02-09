-- Database Schema for Esports Museum
-- Fields: Name, Organization, Brand, Game, Item Type, Badges, Year, Steward, Rarity, Availability, Condition, Chain of Custody

CREATE TABLE IF NOT EXISTS records (
    id TEXT PRIMARY KEY,
    
    -- Core Information
    name TEXT NOT NULL,
    organization TEXT,  -- Team/Organization (OpTic Gaming, FaZe Clan, etc.)
    brand TEXT,         -- Manufacturer/brand (Nike, Scuf, etc.)
    game TEXT NOT NULL, -- CoD, Halo, CS, Valorant, LoL, etc.
    item_type TEXT NOT NULL CHECK(item_type IN ('jersey', 'hardware', 'peripheral', 'signature', 'media', 'other')),
    
    -- Classification & Metadata
    badges TEXT, -- JSON array: ["World Champion", "Signed", "Game-Worn", "MLG", "Tournament-Used"]
    year INTEGER,
    rarity TEXT CHECK(rarity IN ('common', 'uncommon', 'rare', 'very_rare', 'ultra_rare', 'unique', NULL)),
    
    -- Ownership & Provenance
    steward TEXT NOT NULL,
    steward_link TEXT,
    availability TEXT CHECK(availability IN ('in_collection', 'for_sale', 'traded', 'private', NULL)),
    condition TEXT CHECK(condition IN ('mint', 'near_mint', 'excellent', 'good', 'fair', 'poor', NULL)),
    
    -- Chain of Custody (JSON array of custody events)
    -- Example: [
    --   {"date": "2017-08", "from": "Scump", "to": "OpTic Organization", "method": "tournament", "notes": "Won at CWL Championship"},
    --   {"date": "2020-03", "from": "OpTic Organization", "to": "John Collector", "method": "purchase", "notes": "Bought at auction"},
    --   {"date": "2023-01", "from": "John Collector", "to": "Current Steward", "method": "trade", "notes": "Traded for..."}
    -- ]
    chain_of_custody TEXT,
    
    -- Additional Details
    description TEXT,
    notes TEXT,
    
    -- Display & Curation
    featured BOOLEAN DEFAULT 0,
    featured_order INTEGER,
    display_priority INTEGER DEFAULT 0,
    
    -- Authentication
    verified BOOLEAN DEFAULT 0,
    verification_date TEXT,
    verification_notes TEXT,
    
    -- Metadata
    date_added TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    view_count INTEGER DEFAULT 0,
    
    UNIQUE(id)
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('image', 'youtube', 'video')),
    url TEXT NOT NULL,
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT 0,
    FOREIGN KEY (record_id) REFERENCES records(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sponsors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    logo_url TEXT NOT NULL,
    website_url TEXT,
    tier TEXT CHECK(tier IN ('platinum', 'gold', 'silver', 'bronze')),
    display_order INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS stewards (
    username TEXT PRIMARY KEY,
    display_name TEXT,
    bio TEXT,
    social_link TEXT,
    avatar_url TEXT,
    verified BOOLEAN DEFAULT 0,
    joined_date TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_records_item_type ON records(item_type);
CREATE INDEX IF NOT EXISTS idx_records_game ON records(game);
CREATE INDEX IF NOT EXISTS idx_records_organization ON records(organization);
CREATE INDEX IF NOT EXISTS idx_records_brand ON records(brand);
CREATE INDEX IF NOT EXISTS idx_records_steward ON records(steward);
CREATE INDEX IF NOT EXISTS idx_records_year ON records(year);
CREATE INDEX IF NOT EXISTS idx_records_rarity ON records(rarity);
CREATE INDEX IF NOT EXISTS idx_records_featured ON records(featured);
CREATE INDEX IF NOT EXISTS idx_records_verified ON records(verified);
CREATE INDEX IF NOT EXISTS idx_records_date_added ON records(date_added);
CREATE INDEX IF NOT EXISTS idx_media_record_id ON media(record_id);
CREATE INDEX IF NOT EXISTS idx_media_is_primary ON media(is_primary);

-- Full-text search index
CREATE VIRTUAL TABLE IF NOT EXISTS records_fts USING fts5(
    id UNINDEXED,
    name,
    description,
    steward,
    organization,
    brand,
    game,
    badges,
    notes,
    content=records,
    content_rowid=rowid
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS records_ai AFTER INSERT ON records BEGIN
    INSERT INTO records_fts(rowid, id, name, description, steward, organization, brand, game, badges, notes)
    VALUES (new.rowid, new.id, new.name, new.description, new.steward, new.organization, new.brand, new.game, new.badges, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS records_ad AFTER DELETE ON records BEGIN
    DELETE FROM records_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER IF NOT EXISTS records_au AFTER UPDATE ON records BEGIN
    UPDATE records_fts SET 
        name = new.name,
        description = new.description,
        steward = new.steward,
        organization = new.organization,
        brand = new.brand,
        game = new.game,
        badges = new.badges,
        notes = new.notes
    WHERE rowid = new.rowid;
END;
