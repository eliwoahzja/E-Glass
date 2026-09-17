"""Strip ALL annotations from the d8-generated Efx inner class smali.

d8 emits Synthetic/Signature annotations; apktool round-trips them mangled
(Efx$2.<init> claimed '()V' while taking 2 args -> VerifyError -> crash after
splash). Annotations are debug metadata only - removing them is always safe.
"""
import re
import glob

files = glob.glob("smali_classes2/zenxveld/loader/Efx*.smali")
assert files, "no Efx smali found"

total = 0
for path in files:
    with open(path, encoding="utf-8") as f:
        src = f.read()
    # remove whole annotation blocks (possibly nested-less, end at .end annotation)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/Signature;.*?\.end annotation", "", src, flags=re.S)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/EnclosingMethod;.*?\.end annotation", "", new, flags=re.S)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/InnerClass;.*?\.end annotation", "", new, flags=re.S)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/MemberClasses;.*?\.end annotation", "", new, flags=re.S)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/Synthetic;.*?\.end annotation", "", new, flags=re.S)
    new = re.sub(r"\s*\.annotation system Ldalvik/annotation/EnclosingClass;.*?\.end annotation", "", new, flags=re.S)
    if new != src:
        n = len(re.findall(r"\.annotation", src)) - len(re.findall(r"\.annotation", new))
        total += n
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(path, "removed", n, "annotations")

print("total removed:", total)

# verify: no annotation left in these files
left = 0
for path in files:
    with open(path, encoding="utf-8") as f:
        left += f.read().count(".annotation")
print("remaining annotations:", left)
assert left == 0
print("OK")
