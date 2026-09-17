# E Glass — how this repo relates to eliwoahzja/Loader

E Glass = the zenxveld loader with:
- app id `com.eglass.loader` (installs side-by-side with E's Loader)
- original native panel flow (v1/v2/v3 list) — untouched
- VPN gate removed
- per-URL download cache + `[READY]/[NEW]` states (kept)
- liquid-glass UI (frosted panels, icy blue, glass icon + pulsing glow, motion)

This repo holds the **delta overlay**. For full sources either grab
`EGlass-1.0-sources.zip` from Releases, or:

1. Take [eliwoahzja/Loader](https://github.com/eliwoahzja/Loader) at commit
   `51e5e7ad94096778e04b989292ea912f9f066281` (vE-1.3 sources).
2. Copy every file in this repo over it (overwrite).
3. Delete these three files (E Glass uses the native list, not econfig):
   - `smali_classes2/zenxveld/loader/EConfig.smali`
   - `smali_classes2/zenxveld/loader/EConfig$1.smali`
   - `eutils/EConfig.java`
4. Rebuild: `apktool b` → `zipalign -p 4` → `apksigner sign`.

Class names intentionally stay `zenxveld.loader.*` — the native
`libokhttp.so` registers `fetchJsonFromUrl` against that exact class, so
renaming classes would break the JNI bridge. Only the manifest `package=`
(app id) changes.
