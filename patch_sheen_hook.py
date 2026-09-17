"""Hook applyGlassSheen onto START (login_button) + the main library spinner,
right after the existing banner-pulse hook in MainActivity.onCreate."""
PATH = "smali_classes2/zenxveld/loader/MainActivity.smali"

with open(PATH, encoding="utf-8") as f:
    lines = f.readlines()

anchor = None
for i, l in enumerate(lines):
    if "Efx;->startBannerPulse" in l:
        anchor = i
        break
assert anchor is not None, "banner pulse hook not found"

insert = """
    # E FX v2: liquid-glass sheen sweep on START button + library spinner
    sget v5, Lzenxveld/loader/R$id;->login_button:I

    invoke-virtual {p0, v5}, Lzenxveld/loader/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v5

    invoke-static {v5}, Lzenxveld/loader/Efx;->applyGlassSheen(Landroid/view/View;)V

    sget v5, Lzenxveld/loader/R$id;->my_spinner:I

    invoke-virtual {p0, v5}, Lzenxveld/loader/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v5

    invoke-static {v5}, Lzenxveld/loader/Efx;->applyGlassSheen(Landroid/view/View;)V
"""
lines[anchor+2:anchor+2] = insert

with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(lines)
print("sheen hooks inserted (START + library spinner)")
