# Museum Field Guide

Complete documentation for all record fields in the Esports Museum database.

## Core Fields (Required)

### `id` (TEXT, PRIMARY KEY)
- **Format**: `CE-###` (Collectors Envy numbering)
- **Example**: `CE-001`, `CE-042`, `CE-1337`
- **Rules**: Must be unique, uppercase, use consistent numbering
- **Purpose**: Permanent identifier for the record

### `name` (TEXT, REQUIRED)
- **What it is**: The title/name of the item
- **Examples**:
  - `"OpTic Gaming Championship Jersey - Scump"`
  - `"MLG Anaheim 2013 Trophy"`
  - `"Scuf Infinity4PS Pro Controller - Crimsix"`
- **Best practices**: Be descriptive, include player/team when relevant

### `game` (TEXT, REQUIRED)
- **What it is**: Which esport/game this item is from
- **Examples**: `"Call of Duty"`, `"Halo"`, `"Counter-Strike"`, `"Valorant"`, `"League of Legends"`
- **Format**: Full game name (not abbreviations in database)

### `item_type` (TEXT, REQUIRED)
- **What it is**: Category of item
- **Valid values**:
  - `jersey` - Team jerseys, apparel
  - `hardware` - Trophies, medals, awards
  - `peripheral` - Controllers, mice, keyboards, headsets
  - `signature` - Signed items, autographs
  - `media` - Posters, prints, promotional materials
  - `other` - Anything else

### `steward` (TEXT, REQUIRED)
- **What it is**: Current owner/collector username
- **Example**: `"collector_one"`, `"halo_archive"`
- **Format**: Lowercase, no spaces (use underscores)
- **Purpose**: Tracks who owns the item

## Organization & Brand

### `organization` (TEXT, OPTIONAL)
- **What it is**: Team or organization associated with the item
- **Examples**: `"OpTic Gaming"`, `"FaZe Clan"`, `"Team Liquid"`, `"Final Boss"`
- **When to use**: Items from specific teams/orgs

### `brand` (TEXT, OPTIONAL)
- **What it is**: Manufacturer or brand
- **Examples**: `"Scuf Gaming"`, `"Nike"`, `"PlayerWear"`, `"Crown Awards"`
- **When to use**: When brand/manufacturer is relevant

## Classification & Metadata

### `badges` (JSON ARRAY, OPTIONAL)
- **What it is**: Visual badges/labels shown on the item (displayed to users)
- **Format**: JSON array of strings
- **Examples**:
  ```json
  ["World Champion", "Game-Worn", "Signed"]
  ["Tournament-Used", "MLG", "Limited Edition"]
  ["Prototype", "One-of-a-Kind"]
  ```
- **Common badges** (shown as visual badges):
  - `World Champion` - From world championship win
  - `Game-Worn` - Actually worn in competition
  - `Tournament-Used` - Used in tournament
  - `Signed` - Has autograph(s)
  - `Limited Edition` - Limited production run
  - `Prototype` - Pre-production item
  - `Historical` - Significant historical value
  - `MLG` / `ESL` / `DreamHack` - From specific leagues

### `tags` (JSON ARRAY, OPTIONAL)
- **What it is**: Keywords for searching/filtering (not displayed as badges)
- **Format**: JSON array of lowercase strings
- **Examples**:
  ```json
  ["optic", "scump", "cwl", "championship", "green-wall"]
  ["mlg", "anaheim", "2013", "complexity"]
  ["final-boss", "ogre2", "halo-2"]
  ```
- **Use for**: Player names, event names, nicknames, specific tournaments
- **Best practices**: 
  - Keep lowercase
  - Use hyphens for multi-word tags
  - Include player nicknames
  - Add tournament-specific tags

**Badges vs Tags:**
- **Badges** = Visual labels shown on items (formal, displayed)
- **Tags** = Search keywords (informal, hidden, for filtering)

### `year` (INTEGER, OPTIONAL)
- **What it is**: Year associated with the item
- **Example**: `2017`, `2013`, `2024`
- **When to use**: Tournament year, manufacturing year, or season year

### `rarity` (TEXT, OPTIONAL)
- **What it is**: How rare/common the item is
- **Valid values** (in order):
  - `common` - Widely available
  - `uncommon` - Somewhat limited
  - `rare` - Hard to find
  - `very_rare` - Very few exist
  - `ultra_rare` - Extremely limited
  - `unique` - One-of-a-kind

## Ownership & Status

### `steward_link` (TEXT, OPTIONAL)
- **What it is**: Link to steward's social profile
- **Example**: `"https://twitter.com/collector_one"`
- **Format**: Full URL

### `availability` (TEXT, OPTIONAL)
- **What it is**: Current status of the item
- **Valid values**:
  - `in_collection` - In steward's collection
  - `for_sale` - Available for purchase
  - `traded` - Has been traded away
  - `private` - Not for sale/trade

### `condition` (TEXT, OPTIONAL)
- **What it is**: Physical condition of the item
- **Valid values** (in order, best to worst):
  - `mint` - Perfect, like new
  - `near_mint` - Minimal wear
  - `excellent` - Light wear, great condition
  - `good` - Normal wear, functional
  - `fair` - Noticeable wear
  - `poor` - Heavy wear, damage

## Chain of Custody

### `chain_of_custody` (JSON ARRAY, OPTIONAL)
- **What it is**: History of ownership transfers
- **Format**: JSON array of custody events
- **Structure**:
  ```json
  [
    {
      "date": "YYYY-MM",
      "from": "Previous Owner Name",
      "to": "Next Owner Name",
      "method": "purchase|trade|gift|tournament|auction|direct",
      "notes": "Additional details"
    }
  ]
  ```

**Full Example**:
```json
[
  {
    "date": "2017-08",
    "from": "Seth 'Scump' Abner",
    "to": "OpTic Gaming",
    "method": "tournament",
    "notes": "Worn during CWL Championship 2017 Grand Finals"
  },
  {
    "date": "2020-03",
    "from": "OpTic Gaming",
    "to": "Private Collector",
    "method": "auction",
    "notes": "Sold at OpTic memorabilia auction for $2,500"
  },
  {
    "date": "2023-01",
    "from": "Private Collector",
    "to": "collector_one",
    "method": "purchase",
    "notes": "Acquired through private sale with COA"
  }
]
```

**Methods**:
- `tournament` - Item originated from tournament/competition
- `purchase` - Bought with money
- `trade` - Traded for other items
- `gift` - Given as gift
- `auction` - Acquired at auction
- `direct` - Direct from player/team/org

## Description & Notes

### `description` (TEXT, OPTIONAL)
- **What it is**: Detailed description of the item
- **Guidelines**:
  - 100-500 words ideal
  - Start with what makes it significant
  - Include historical context
  - Mention unique characteristics
  - Write in complete sentences

**Example**:
> "Game-worn OpTic Gaming jersey from the 2017 Call of Duty World League Championship Grand Finals. This iconic green jersey was worn by Seth 'Scump' Abner during the match that secured OpTic's first CWL Championship title. Features authentic wear patterns and is signed by Scump on the back. This tournament marked a turning point in competitive Call of Duty history."

### `notes` (TEXT, OPTIONAL)
- **What it is**: Additional notes, observations, or caveats
- **Use for**:
  - Condition details
  - Included items (COA, original packaging)
  - Authentication details
  - Storage/display notes

**Example**:
> "Includes original OpTic Gaming certificate of authenticity. Minor wear on right sleeve consistent with tournament use. Stored in climate-controlled display case."

## Authentication

### `verified` (BOOLEAN, DEFAULT FALSE)
- **What it is**: Whether the item has been verified as authentic
- **Values**: `true` or `false`
- **When to mark true**: 
  - Direct from source (player/team/org)
  - Expert authentication
  - Provenance documentation
  - Community verification

### `verification_date` (TEXT, OPTIONAL)
- **What it is**: When verification occurred
- **Format**: `YYYY-MM-DD`
- **Example**: `"2024-01-15"`

### `verification_notes` (TEXT, OPTIONAL)
- **What it is**: How/why item was verified
- **Example**:
> "Verified through OpTic Gaming records, tournament photos showing item in use, and expert authentication by EsportsAuth. Serial number matches team inventory records."

## Display & Curation

### `featured` (BOOLEAN, DEFAULT FALSE)
- **What it is**: Should this be featured on homepage?
- **Values**: `true` or `false`
- **Use sparingly**: Only 2-3 items should be featured

### `featured_order` (INTEGER, OPTIONAL)
- **What it is**: Order in featured section
- **Example**: `1`, `2`, `3`
- **Only set if**: `featured = true`

### `display_priority` (INTEGER, DEFAULT 0)
- **What it is**: Overall display priority (higher = shown first)
- **Example**: `100`, `50`, `0`
- **Use for**: Controlling sort order in browse pages

## Metadata (Auto-managed)

### `date_added` (TEXT, AUTO)
- **What it is**: When record was added to database
- **Format**: `YYYY-MM-DD HH:MM:SS`
- **Automatically set**: Don't edit manually

### `last_updated` (TEXT, AUTO)
- **What it is**: When record was last modified
- **Automatically updated**: Don't edit manually

### `view_count` (INTEGER, AUTO)
- **What it is**: How many times record page was viewed
- **Starts at**: `0`
- **Increments**: Automatically

## Media

Media is stored in a separate `media` table with these fields:

### Media Fields
- `record_id` - Links to record ID
- `type` - `image`, `youtube`, or `video`
- `url` - Full URL to media
- `caption` - Optional description
- `display_order` - Sort order (0, 1, 2...)
- `is_primary` - Is this the thumbnail? (only one per record)

### Media in JSON
```json
"media": [
  {
    "type": "image",
    "url": "https://example.com/photo.jpg",
    "caption": "Front view",
    "is_primary": true
  },
  {
    "type": "image",
    "url": "https://example.com/photo2.jpg",
    "caption": "Back view"
  },
  {
    "type": "youtube",
    "url": "dQw4w9WgXcQ"
  }
]
```

## Quick Reference

**Minimum Required**:
```json
{
  "id": "CE-###",
  "name": "Item Name",
  "game": "Game Name",
  "item_type": "jersey|hardware|peripheral|signature|media|other",
  "steward": "username"
}
```

**Recommended**:
Add: `organization`, `year`, `description`, `rarity`, `condition`, `media`

**Complete**:
Fill in all relevant fields including `badges`, `chain_of_custody`, verification details

## Future Fields

The schema is designed to be extensible. Future additions might include:
- Estimated value
- Acquisition cost
- Insurance value
- Physical dimensions
- Materials/construction
- Serial numbers
- Related records
- Exhibition history

To add new fields, update `schema.sql` and rebuild.
