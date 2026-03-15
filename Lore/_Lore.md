---
title: "Lore"
type: moc
tags:
  - twin-portals
  - moc
  - lore
---

# Lore

This page serves as the Map of Content for the lore and story arcs of the Twin Portals campaign. Browse by season, status, or explore individual arcs below.

## Story Arcs

### All Story Arcs

```dataview
TABLE seasons AS "Seasons", status AS "Status"
FROM "Twin Portals/Lore/Story Arcs"
WHERE type = "story-arc"
SORT file.name ASC
```

### Season 1 Arcs

```dataview
TABLE status AS "Status"
FROM "Twin Portals/Lore/Story Arcs"
WHERE type = "story-arc" AND contains(seasons, 1)
SORT file.name ASC
```

### Season 2 Arcs

```dataview
TABLE status AS "Status"
FROM "Twin Portals/Lore/Story Arcs"
WHERE type = "story-arc" AND contains(seasons, 2)
SORT file.name ASC
```

### Ongoing Arcs

```dataview
TABLE seasons AS "Seasons"
FROM "Twin Portals/Lore/Story Arcs"
WHERE type = "story-arc" AND status = "ongoing"
SORT file.name ASC
```

### Resolved Arcs

```dataview
TABLE seasons AS "Seasons"
FROM "Twin Portals/Lore/Story Arcs"
WHERE type = "story-arc" AND status = "resolved"
SORT file.name ASC
```

## Arc Timeline

The major story arcs of Twin Portals flow roughly as follows:

### Season 1 (Episodes 1-30)
1. [[The Search for Floon]] -- The campaign's inciting incident
2. [[Trollskull Manor and The Short Rest]] -- Home base established (ongoing)
3. [[The Stone of Golorr]] -- Central MacGuffin; the chase for Neverember's gold
4. [[The Cassalanter Conspiracy]] -- The Asmodeus pact and the Founder's Day battle
5. [[Lark's Death and Resurrection]] -- The most devastating moment of Season 1
6. [[The Kolat Towers and the Necromancer]] -- The Zhentarim base and the Necromancer's identity
7. [[The Hunt for Manshoon]] -- Begins at the end of Season 1

### Season 2 (Episodes 31-68)
8. [[The Great Beast of Erua]] -- Shadowfell journey and the Dynamo of Possibility
9. [[The Jolly Gents]] -- Alliance, betrayal, and the 14th clone
10. [[The Journey to Neverwinter]] -- Sprawling arc across the Sword Coast and beyond
11. [[Xae's Portal Mystery and Halaster's Siblings]] -- The contract and the twin portals (ongoing)
12. [[The Wall of the Faithless and the Radiant Citadel]] -- Season 2 finale

## Tags in Use

Story arc pages use the following tags for filtering:
- `story-arc` -- All story arc pages
- `season-1`, `season-2` -- Season-specific arcs
- `waterdeep`, `neverwinter`, `shadowfell`, `radiant-citadel` -- Location-based
- `manshoon`, `asmodeus`, `halaster` -- Antagonist-based
- `character-arc` -- Personal character stories
- `cult-of-the-dragon`, `zhentarim`, `jolly-gents` -- Faction-based
