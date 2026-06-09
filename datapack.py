#!/usr/bin/env python3
import json, zipfile, os, re

# ---- settings ----
JAR     = "data/versions/1.21.11/server-1.21.11.jar"
OUT     = "data/world/datapacks/more_ores"
DIAMOND = 3.0   # diamonds x3
DEBRIS  = 4.0   # ancient debris (netherite) x4
# ------------------

WG   = "data/minecraft/worldgen"
WANT = re.compile(rf"{WG}/(placed_feature|configured_feature)/(ore_diamond|ore_ancient_debris).*\.json$")

def scale(name, o):
    f = DEBRIS if "ancient_debris" in name else DIAMOND
    if "placed_feature/" in name:
        for m in o.get("placement", []):
            if m.get("type") in ("minecraft:count", "minecraft:count_on_every_layer") and isinstance(m.get("count"), int):
                m["count"] = max(1, round(m["count"] * f))
            elif m.get("type") == "minecraft:rarity_filter" and isinstance(m.get("chance"), int):
                m["chance"] = max(1, round(m["chance"] / f))
    else:
        c = o.get("config", {})
        if isinstance(c.get("size"), int):
            c["size"] = min(64, max(1, round(c["size"] * f)))
        if "ancient_debris" not in name and "discard_chance_on_air_exposure" in c:
            c["discard_chance_on_air_exposure"] = 0.0   # show diamonds in caves; leave debris buried
    return o

os.makedirs(OUT, exist_ok=True)

count = 0
with zipfile.ZipFile(JAR) as z:
    pv = json.loads(z.read("version.json"))["pack_version"]
    major = pv.get("data_major", pv.get("data"))
    minor = pv.get("data_minor", 0)
    for name in z.namelist():
        if not WANT.match(name):
            continue
        dst = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w") as fp:
            json.dump(scale(name, json.loads(z.read(name))), fp, indent=2)
        print("wrote", name)
        count += 1

with open(os.path.join(OUT, "pack.mcmeta"), "w") as fp:
    json.dump({"pack": {
        "description": f"Diamond x{DIAMOND}, Netherite x{DEBRIS}",
        "min_format": [major, 0],
        "max_format": [major, minor],
    }}, fp, indent=2)

print(f"\n{count} ore files written to {OUT}")
print(f"pack.mcmeta format {major}.{minor}")
if count == 0:
    print("WARNING: no ore files matched — check the JAR path.")