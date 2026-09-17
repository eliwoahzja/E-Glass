.class Lzenxveld/loader/Efx$2;
.super Ljava/lang/Object;
.source "Efx.java"

# interfaces
.implements Landroid/animation/ValueAnimator$AnimatorUpdateListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lzenxveld/loader/Efx;->applyGlassSheen(Landroid/view/View;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic val$sheen:Lzenxveld/loader/Efx$GlassSheenDrawable;

.field final synthetic val$v:Landroid/view/View;


# direct methods
.method constructor <init>(Lzenxveld/loader/Efx$GlassSheenDrawable;Landroid/view/View;)V
    .locals 0
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 67
    iput-object p1, p0, Lzenxveld/loader/Efx$2;->val$sheen:Lzenxveld/loader/Efx$GlassSheenDrawable;

    iput-object p2, p0, Lzenxveld/loader/Efx$2;->val$v:Landroid/view/View;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onAnimationUpdate(Landroid/animation/ValueAnimator;)V
    .locals 1

    .line 70
    iget-object v0, p0, Lzenxveld/loader/Efx$2;->val$sheen:Lzenxveld/loader/Efx$GlassSheenDrawable;

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->getAnimatedValue()Ljava/lang/Object;

    move-result-object p1

    check-cast p1, Ljava/lang/Float;

    invoke-virtual {p1}, Ljava/lang/Float;->floatValue()F

    move-result p1

    invoke-virtual {v0, p1}, Lzenxveld/loader/Efx$GlassSheenDrawable;->setProgress(F)V

    .line 71
    iget-object p1, p0, Lzenxveld/loader/Efx$2;->val$v:Landroid/view/View;

    invoke-virtual {p1}, Landroid/view/View;->invalidate()V

    return-void
.end method
