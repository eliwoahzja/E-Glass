.class Lzenxveld/loader/Efx$3;
.super Ljava/lang/Object;
.source "Efx.java"

# interfaces
.implements Landroid/view/View$OnAttachStateChangeListener;


# annotations


# instance fields
.field final synthetic val$va:Landroid/animation/ValueAnimator;


# direct methods
.method constructor <init>(Landroid/animation/ValueAnimator;)V
    .locals 0

    .line 76
    iput-object p1, p0, Lzenxveld/loader/Efx$3;->val$va:Landroid/animation/ValueAnimator;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onViewAttachedToWindow(Landroid/view/View;)V
    .locals 0

    .line 79
    iget-object p1, p0, Lzenxveld/loader/Efx$3;->val$va:Landroid/animation/ValueAnimator;

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->isStarted()Z

    move-result p1

    if-nez p1, :cond_0

    .line 80
    iget-object p1, p0, Lzenxveld/loader/Efx$3;->val$va:Landroid/animation/ValueAnimator;

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->start()V

    :cond_0
    return-void
.end method

.method public onViewDetachedFromWindow(Landroid/view/View;)V
    .locals 0

    .line 86
    iget-object p1, p0, Lzenxveld/loader/Efx$3;->val$va:Landroid/animation/ValueAnimator;

    invoke-virtual {p1}, Landroid/animation/ValueAnimator;->cancel()V

    return-void
.end method
