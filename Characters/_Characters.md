---
title: "Characters"
type: moc
tags:
  - twin-portals
  - moc
---

# Characters

## Player Characters

```dataview
TABLE player as "Player", race as "Race", class as "Class"
FROM "Twin Portals/Characters/PCs"
WHERE type = "character"
SORT title ASC
```

## Guest Characters

```dataview
TABLE player as "Player", race as "Race", class as "Class"
FROM "Twin Portals/Characters/PCs"
WHERE subtype = "guest-pc"
SORT title ASC
```

## Non-Player Characters

```dataview
TABLE WITHOUT ID file.link as "NPC", status as "Status"
FROM "Twin Portals/Characters/NPCs"
WHERE type = "character"
SORT title ASC
```
