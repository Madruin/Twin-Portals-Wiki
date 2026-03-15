---
title: "Squidky"
type: character
subtype: npc
status: unknown
aliases: []
tags:
  - twin-portals
  - character
  - npc
---

# Squidky

A familiar figure at the Short Rest, present when SWOJ returns.

**First appearance:** Episode 
**Total appearances:** 0 episodes

## Description

A familiar figure at the Short Rest, present when SWOJ returns.

## Role in the Story



## Episode Appearances

```dataview
TABLE date as "Air Date", "S" + season + "E" + episode as "Episode"
FROM "Twin Portals/Episodes"
WHERE contains(file.outlinks, this.file.link)
SORT overall ASC
```
