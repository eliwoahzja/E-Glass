.class final Lzenxveld/loader/Efx$GlassSheenDrawable;
.super Landroid/graphics/drawable/Drawable;
.source "Efx.java"


# annotations


# instance fields
.field private mProgress:F


# direct methods
.method constructor <init>()V
    .locals 1

    .line 95
    invoke-direct {p0}, Landroid/graphics/drawable/Drawable;-><init>()V

    const/4 v0, 0x0

    .line 96
    iput v0, p0, Lzenxveld/loader/Efx$GlassSheenDrawable;->mProgress:F

    return-void
.end method


# virtual methods
.method public draw(Landroid/graphics/Canvas;)V
    .locals 20

    move-object/from16 v0, p0

    .line 104
    invoke-virtual/range {p0 .. p0}, Lzenxveld/loader/Efx$GlassSheenDrawable;->getBounds()Landroid/graphics/Rect;

    move-result-object v1

    .line 105
    invoke-virtual {v1}, Landroid/graphics/Rect;->isEmpty()Z

    move-result v2

    if-nez v2, :cond_4

    iget v2, v0, Lzenxveld/loader/Efx$GlassSheenDrawable;->mProgress:F

    const/4 v3, 0x0

    cmpg-float v3, v2, v3

    if-lez v3, :cond_4

    const/high16 v3, 0x3f800000    # 1.0f

    cmpl-float v2, v2, v3

    if-ltz v2, :cond_0

    goto/16 :goto_1

    .line 108
    :cond_0
    invoke-virtual {v1}, Landroid/graphics/Rect;->width()I

    move-result v2

    invoke-virtual {v1}, Landroid/graphics/Rect;->height()I

    move-result v4

    invoke-static {v2, v4}, Ljava/lang/Math;->max(II)I

    move-result v2

    int-to-float v2, v2

    const v4, 0x3eb33333    # 0.35f

    mul-float v2, v2, v4

    .line 109
    invoke-virtual {v1}, Landroid/graphics/Rect;->width()I

    move-result v4

    int-to-float v4, v4

    const/high16 v5, 0x40000000    # 2.0f

    mul-float v5, v5, v2

    add-float/2addr v4, v5

    .line 110
    iget v5, v1, Landroid/graphics/Rect;->left:I

    int-to-float v5, v5

    sub-float/2addr v5, v2

    iget v6, v0, Lzenxveld/loader/Efx$GlassSheenDrawable;->mProgress:F

    mul-float v4, v4, v6

    add-float/2addr v5, v4

    const v4, 0x3e4ccccd    # 0.2f

    cmpg-float v7, v6, v4

    if-gez v7, :cond_1

    div-float v3, v6, v4

    goto :goto_0

    :cond_1
    const v7, 0x3f4ccccd    # 0.8f

    cmpl-float v7, v6, v7

    if-lez v7, :cond_2

    sub-float/2addr v3, v6

    div-float/2addr v3, v4

    :cond_2
    :goto_0
    const/high16 v4, 0x42dc0000    # 110.0f

    mul-float v3, v3, v4

    float-to-int v3, v3

    if-gtz v3, :cond_3

    return-void

    .line 122
    :cond_3
    new-instance v4, Landroid/graphics/LinearGradient;

    sub-float v7, v5, v2

    iget v6, v1, Landroid/graphics/Rect;->top:I

    int-to-float v8, v6

    add-float v9, v5, v2

    iget v2, v1, Landroid/graphics/Rect;->bottom:I

    int-to-float v10, v2

    shl-int/lit8 v2, v3, 0x18

    const v3, 0xffffff

    or-int/2addr v2, v3

    const/4 v3, 0x0

    filled-new-array {v3, v2, v3}, [I

    move-result-object v11

    const/4 v2, 0x3

    new-array v12, v2, [F

    fill-array-data v12, :array_0

    sget-object v13, Landroid/graphics/Shader$TileMode;->CLAMP:Landroid/graphics/Shader$TileMode;

    move-object v6, v4

    invoke-direct/range {v6 .. v13}, Landroid/graphics/LinearGradient;-><init>(FFFF[I[FLandroid/graphics/Shader$TileMode;)V

    .line 127
    new-instance v2, Landroid/graphics/Paint;

    invoke-direct {v2}, Landroid/graphics/Paint;-><init>()V

    .line 128
    invoke-virtual {v2, v4}, Landroid/graphics/Paint;->setShader(Landroid/graphics/Shader;)Landroid/graphics/Shader;

    .line 129
    iget v3, v1, Landroid/graphics/Rect;->left:I

    int-to-float v15, v3

    iget v3, v1, Landroid/graphics/Rect;->top:I

    int-to-float v3, v3

    iget v4, v1, Landroid/graphics/Rect;->right:I

    int-to-float v4, v4

    iget v1, v1, Landroid/graphics/Rect;->bottom:I

    int-to-float v1, v1

    move-object/from16 v14, p1

    move/from16 v16, v3

    move/from16 v17, v4

    move/from16 v18, v1

    move-object/from16 v19, v2

    invoke-virtual/range {v14 .. v19}, Landroid/graphics/Canvas;->drawRect(FFFFLandroid/graphics/Paint;)V

    :cond_4
    :goto_1
    return-void

    :array_0
    .array-data 4
        0x0
        0x3f000000    # 0.5f
        0x3f800000    # 1.0f
    .end array-data
.end method

.method public getOpacity()I
    .locals 1

    const/4 v0, -0x3

    return v0
.end method

.method public setAlpha(I)V
    .locals 0

    return-void
.end method

.method public setColorFilter(Landroid/graphics/ColorFilter;)V
    .locals 0

    return-void
.end method

.method setProgress(F)V
    .locals 0

    .line 99
    iput p1, p0, Lzenxveld/loader/Efx$GlassSheenDrawable;->mProgress:F

    return-void
.end method
