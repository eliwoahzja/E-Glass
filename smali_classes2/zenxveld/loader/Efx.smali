.class public final Lzenxveld/loader/Efx;
.super Ljava/lang/Object;
.source "Efx.java"


# annotations


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 22
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static applyGlassSheen(Landroid/view/View;)V
    .locals 4

    if-nez p0, :cond_0

    return-void

    .line 59
    :cond_0
    :try_start_0
    new-instance v0, Lzenxveld/loader/Efx$GlassSheenDrawable;

    invoke-direct {v0}, Lzenxveld/loader/Efx$GlassSheenDrawable;-><init>()V

    const/4 v1, 0x0

    .line 60
    invoke-virtual {v0, v1}, Lzenxveld/loader/Efx$GlassSheenDrawable;->setAlpha(I)V

    .line 61
    invoke-virtual {p0}, Landroid/view/View;->getOverlay()Landroid/view/ViewOverlay;

    move-result-object v1

    invoke-virtual {v1, v0}, Landroid/view/ViewOverlay;->add(Landroid/graphics/drawable/Drawable;)V

    const/4 v1, 0x2

    new-array v1, v1, [F

    .line 62
    fill-array-data v1, :array_0

    invoke-static {v1}, Landroid/animation/ValueAnimator;->ofFloat([F)Landroid/animation/ValueAnimator;

    move-result-object v1

    const-wide/16 v2, 0xa28

    .line 63
    invoke-virtual {v1, v2, v3}, Landroid/animation/ValueAnimator;->setDuration(J)Landroid/animation/ValueAnimator;

    .line 64
    new-instance v2, Landroid/view/animation/LinearInterpolator;

    invoke-direct {v2}, Landroid/view/animation/LinearInterpolator;-><init>()V

    invoke-virtual {v1, v2}, Landroid/animation/ValueAnimator;->setInterpolator(Landroid/animation/TimeInterpolator;)V

    const/4 v2, -0x1

    .line 65
    invoke-virtual {v1, v2}, Landroid/animation/ValueAnimator;->setRepeatCount(I)V

    const/4 v2, 0x1

    .line 66
    invoke-virtual {v1, v2}, Landroid/animation/ValueAnimator;->setRepeatMode(I)V

    .line 67
    new-instance v2, Lzenxveld/loader/Efx$2;

    invoke-direct {v2, v0, p0}, Lzenxveld/loader/Efx$2;-><init>(Lzenxveld/loader/Efx$GlassSheenDrawable;Landroid/view/View;)V

    invoke-virtual {v1, v2}, Landroid/animation/ValueAnimator;->addUpdateListener(Landroid/animation/ValueAnimator$AnimatorUpdateListener;)V

    .line 74
    invoke-virtual {v1}, Landroid/animation/ValueAnimator;->start()V

    .line 76
    new-instance v0, Lzenxveld/loader/Efx$3;

    invoke-direct {v0, v1}, Lzenxveld/loader/Efx$3;-><init>(Landroid/animation/ValueAnimator;)V

    invoke-virtual {p0, v0}, Landroid/view/View;->addOnAttachStateChangeListener(Landroid/view/View$OnAttachStateChangeListener;)V
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :catchall_0
    return-void

    :array_0
    .array-data 4
        0x0
        0x3f800000    # 1.0f
    .end array-data
.end method

.method public static startBannerPulse(Landroid/widget/ImageView;)V
    .locals 4

    if-nez p0, :cond_0

    return-void

    .line 31
    :cond_0
    :try_start_0
    invoke-virtual {p0}, Landroid/widget/ImageView;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    const-string v1, "banner_pulse"

    const-string v2, "drawable"

    invoke-virtual {p0}, Landroid/widget/ImageView;->getContext()Landroid/content/Context;

    move-result-object v3

    invoke-virtual {v3}, Landroid/content/Context;->getPackageName()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v1, v2, v3}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    if-nez v0, :cond_1

    return-void

    .line 35
    :cond_1
    invoke-virtual {p0, v0}, Landroid/widget/ImageView;->setImageResource(I)V

    .line 36
    invoke-virtual {p0}, Landroid/widget/ImageView;->getDrawable()Landroid/graphics/drawable/Drawable;

    move-result-object v0

    .line 37
    instance-of v0, v0, Landroid/graphics/drawable/AnimationDrawable;

    if-eqz v0, :cond_2

    .line 38
    new-instance v0, Lzenxveld/loader/Efx$1;

    invoke-direct {v0, p0}, Lzenxveld/loader/Efx$1;-><init>(Landroid/widget/ImageView;)V

    invoke-virtual {p0, v0}, Landroid/widget/ImageView;->post(Ljava/lang/Runnable;)Z
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    :catchall_0
    :cond_2
    return-void
.end method
