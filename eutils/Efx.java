package zenxveld.loader;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.animation.ObjectAnimator;
import android.animation.ValueAnimator;
import android.graphics.Canvas;
import android.graphics.ColorFilter;
import android.graphics.LinearGradient;
import android.graphics.PixelFormat;
import android.graphics.Shader;
import android.graphics.drawable.Drawable;
import android.view.View;
import android.view.animation.LinearInterpolator;
import android.widget.ImageView;

/**
 * E — FX helpers v2: liquid-glass sheen sweep on panel strokes + banner pulse.
 */
public final class Efx {

    private Efx() {
    }

    /** Swap the banner to its pulsing glow animation and start it. */
    public static void startBannerPulse(ImageView iv) {
        if (iv == null) {
            return;
        }
        try {
            int id = iv.getResources().getIdentifier("banner_pulse", "drawable", iv.getContext().getPackageName());
            if (id == 0) {
                return;
            }
            iv.setImageResource(id);
            android.graphics.drawable.Drawable d = iv.getDrawable();
            if (d instanceof android.graphics.drawable.AnimationDrawable) {
                iv.post(new Runnable() {
                    @Override
                    public void run() {
                        android.graphics.drawable.Drawable d2 = iv.getDrawable();
                        if (d2 instanceof android.graphics.drawable.AnimationDrawable) {
                            ((android.graphics.drawable.AnimationDrawable) d2).start();
                        }
                    }
                });
            }
        } catch (Throwable t) {
            // never break the app over an effect
        }
    }

    /** liquid-glass sheen: a diagonal light band sweeping across the view's stroke. */
    public static void applyGlassSheen(final View v) {
        if (v == null) {
            return;
        }
        try {
            final GlassSheenDrawable sheen = new GlassSheenDrawable();
            sheen.setAlpha(0);
            v.getOverlay().add(sheen);
            final ValueAnimator va = ValueAnimator.ofFloat(0f, 1f);
            va.setDuration(2600L);
            va.setInterpolator(new LinearInterpolator());
            va.setRepeatCount(ValueAnimator.INFINITE);
            va.setRepeatMode(ValueAnimator.RESTART);
            va.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
                @Override
                public void onAnimationUpdate(ValueAnimator animation) {
                    sheen.setProgress(((Float) animation.getAnimatedValue()).floatValue());
                    v.invalidate();
                }
            });
            va.start();
            // pause the sweep while nothing is attached (avoid battery burn)
            v.addOnAttachStateChangeListener(new View.OnAttachStateChangeListener() {
                @Override
                public void onViewAttachedToWindow(View view) {
                    if (!va.isStarted()) {
                        va.start();
                    }
                }

                @Override
                public void onViewDetachedFromWindow(View view) {
                    va.cancel();
                }
            });
        } catch (Throwable t) {
            // never break the app over an effect
        }
    }

    /** Diagonal shine band: appears at one edge, sweeps across, disappears. */
    static final class GlassSheenDrawable extends Drawable {
        private float mProgress = 0f;

        void setProgress(float p) {
            mProgress = p;
        }

        @Override
        public void draw(Canvas canvas) {
            android.graphics.Rect b = getBounds();
            if (b.isEmpty() || mProgress <= 0f || mProgress >= 1f) {
                return;
            }
            float band = Math.max(b.width(), b.height()) * 0.35f;
            float travel = b.width() + band * 2f;
            float x = b.left - band + mProgress * travel;
            // ease the shine: fade in first 20%, out last 20%
            float alpha = 1f;
            if (mProgress < 0.2f) {
                alpha = mProgress / 0.2f;
            } else if (mProgress > 0.8f) {
                alpha = (1f - mProgress) / 0.2f;
            }
            int a = (int) (110 * alpha);
            if (a <= 0) {
                return;
            }
            LinearGradient lg = new LinearGradient(
                    x - band, b.top, x + band, b.bottom,
                    new int[]{0x00000000, (a << 24) | 0xffffff, 0x00000000},
                    new float[]{0f, 0.5f, 1f},
                    Shader.TileMode.CLAMP);
            android.graphics.Paint paint = new android.graphics.Paint();
            paint.setShader(lg);
            canvas.drawRect(b.left, b.top, b.right, b.bottom, paint);
        }

        @Override
        public void setAlpha(int alpha) {
        }

        @Override
        public void setColorFilter(ColorFilter colorFilter) {
        }

        @Override
        public int getOpacity() {
            return PixelFormat.TRANSLUCENT;
        }
    }
}
