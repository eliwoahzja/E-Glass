"""Remove the orphan 'move-object p1, v3' left by the EConfig strip (VerifyError crash)."""
PATH = "smali_classes2/zenxveld/loader/MainActivity.smali"

with open(PATH, encoding="utf-8") as f:
    src = f.read()

needle = "    move-object p1, v3\n"
count = src.count(needle)
assert count == 1, "expected exactly 1 orphan, found %d" % count
src = src.replace(needle, "", 1)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("removed orphan move-object p1, v3 — populateSpinnerFromNativeJson now verifies")
