---
title: ""
type: item
subtype:
owner: ""
aliases: []
tags:
  - twin-portals
  - item
---

# {{title}}

**Type:** {{subtype}}
**Owner:** {{owner}}
**Also known as:** {{aliases}}
**First appearance:**

## Description



## History



## Episode Appearances

```dataview
TABLE date as "Air Date", "S" + season + "E" + episode as "Episode"
FROM "Twin Portals/Episodes"
WHERE contains(file.outlinks, this.file.link)
SORT overall ASC
```
