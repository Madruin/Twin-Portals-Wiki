---
title: ""
type: location
subtype:
parent_location: ""
aliases: []
tags:
  - twin-portals
  - location
---

# {{title}}

**Type:** {{subtype}}
**Located in:** {{parent_location}}
**Also known as:** {{aliases}}
**First appearance:**

## Description



## Notable Events

-

## Connected Characters

-

## Episode Appearances

```dataview
TABLE date as "Air Date", "S" + season + "E" + episode as "Episode"
FROM "Twin Portals/Episodes"
WHERE contains(file.outlinks, this.file.link)
SORT overall ASC
```
