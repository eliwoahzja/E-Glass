package zenxveld.loader;

import android.content.Context;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * E — persistent download cache (v2).
 * Stored in filesDir (survives reboots AND Android's storage-pressure wipes,
 * unlike cacheDir). Migrates v1 cacheDir entries on first use so nothing
 * already downloaded is lost. Same public API as v1 — drop-in replacement.
 */
public final class EUtils {

    private static final String PREFIX = "e_";
    private static final String TARGET = "libexternal.so";

    private EUtils() {
    }

    private static File cacheRoot(Context context) {
        return context.getFilesDir();
    }

    public static File cacheFileFor(Context context, String str) {
        String name;
        if (str == null) {
            name = "unknown";
        } else {
            int i = str.lastIndexOf(47);
            name = (i < 0 || i + 1 >= str.length()) ? str : str.substring(i + 1);
            name = PREFIX + Integer.toHexString(str.hashCode()) + "_" + name;
        }
        return new File(cacheRoot(context), name);
    }

    public static boolean isCached(Context context, String str) {
        File f = cacheFileFor(context, str);
        if (f.exists() && f.length() > 1024) {
            return true;
        }
        // migrate v1 cacheDir entry if present
        File old = new File(context.getCacheDir(), f.getName());
        if (old.exists() && old.length() > 1024) {
            if (copyFile(old, f)) {
                old.delete();
                return true;
            }
        }
        return false;
    }

    public static boolean materializeIfCached(Context context, String str) {
        if (isCached(context, str)) {
            return copyFile(cacheFileFor(context, str), new File(cacheRoot(context), TARGET));
        }
        return false;
    }

    public static boolean stashAfterDownload(Context context, String str, boolean z) {
        if (z && str != null && str.length() != 0) {
            File file = new File(cacheRoot(context), TARGET);
            if (file.exists() && file.length() > 1024) {
                return copyFile(file, cacheFileFor(context, str));
            }
        }
        return false;
    }

    public static String decorate(Context context, String str, String str2) {
        return str + "  [" + (isCached(context, str2) ? "READY" : "NEW") + "]";
    }

    private static boolean copyFile(File file, File file2) {
        FileInputStream in = null;
        FileOutputStream out = null;
        try {
            in = new FileInputStream(file);
            out = new FileOutputStream(file2);
            byte[] buf = new byte[65536];
            int n;
            while ((n = in.read(buf)) > 0) {
                out.write(buf, 0, n);
            }
            out.flush();
            return true;
        } catch (Throwable t) {
            return false;
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException ignored) {
                }
            }
            if (out != null) {
                try {
                    out.close();
                } catch (IOException ignored) {
                }
            }
        }
    }
}
