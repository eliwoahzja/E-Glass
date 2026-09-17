# E Glass

Liquid-glass variant of [E's Loader](https://github.com/eliwoahzja/Loader) for side-by-side install.

- App ID: `com.eglass.loader` (E's Loader = `zenxveld.loader`) — both can be installed at once
- Uses the **original native panel flow** (`fetchJsonFromUrl` -> zxx panel server list, v1/v2/v3) exactly like the zenxveld loader
- **VPN detection removed** (`getDetectedVPN()` returns null — splash + inject-time blocks dead)
- Per-URL download cache with `[READY]/[NEW]` dropdown states kept (EUtils)
- Liquid-glass UI: frosted panels, icy blue accent, glass icon + pulsing glow, motion

## Relationship to the Loader repo

This repo is a **delta pack**. To get full sources:

1. Clone [eliwoahzja/Loader](https://github.com/eliwoahzja/Loader) at commit `51e5e7ad`
2. Copy every file from this repo over it (overwrites), and **delete**
   `smali_classes2/zenxveld/loader/EConfig.smali`,
   `smali_classes2/zenxveld/loader/EConfig$1.smali`,
   `eutils/EConfig.java`
3. `apktool b` -> zipalign -> apksigner

Or just install the APK from Releases.
