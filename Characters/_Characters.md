---
title: "Characters"
type: moc
tags:
  - twin-portals
  - moc
---

# Characters

## Season 1-2 Player Characters (SWOJ Campaign)

```dataview
TABLE player as "Player", race as "Race", class as "Class"
FROM "Twin Portals/Characters/PCs"
WHERE type = "character" AND (subtype = "pc" OR subtype = "guest-pc") AND !contains(tags, "icewind-dale")
SORT title ASC
```

## Season 3 Player Characters (Icewind Dale Campaign)

```dataview
TABLE player as "Player", race as "Race", class as "Class", campaign as "Campaign"
FROM "Twin Portals/Characters/PCs"
WHERE type = "character" AND contains(tags, "icewind-dale")
SORT title ASC
```

## Non-Player Characters

```dataview
TABLE WITHOUT ID file.link as "NPC", status as "Status"
FROM "Twin Portals/Characters/NPCs"
WHERE type = "character"
SORT title ASC
```
