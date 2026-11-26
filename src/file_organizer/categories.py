"""Extension-to-category mapping used by category mode."""

from __future__ import annotations

CATEGORY_EXTENSIONS: dict[str, frozenset[str]] = {
    "Images": frozenset(
        {
            "jpg",
            "jpeg",
            "png",
            "gif",
            "bmp",
            "tif",
            "tiff",
            "webp",
            "svg",
            "ico",
            "heic",
            "heif",
            "raw",
            "cr2",
            "nef",
            "arw",
            "dng",
        }
    ),
    "Documents": frozenset(
        {
            "pdf",
            "doc",
            "docx",
            "txt",
            "rtf",
            "odt",
            "xls",
            "xlsx",
            "ods",
            "ppt",
            "pptx",
            "odp",
            "epub",
            "mobi",
            "md",
            "pages",
            "numbers",
            "key",
        }
    ),
    "Audio": frozenset(
        {
            "mp3",
            "wav",
            "flac",
            "aac",
            "ogg",
            "oga",
            "wma",
            "m4a",
            "opus",
            "aiff",
            "alac",
            "mid",
            "midi",
        }
    ),
    "Video": frozenset(
        {
            "mp4",
            "mkv",
            "avi",
            "mov",
            "wmv",
            "flv",
            "webm",
            "m4v",
            "mpg",
            "mpeg",
            "3gp",
            "ts",
        }
    ),
    "Archives": frozenset(
        {"zip", "rar", "7z", "tar", "gz", "bz2", "xz", "zst", "tgz", "tbz2", "iso", "cab"}
    ),
    "Code": frozenset(
        {
            "py",
            "pyw",
            "js",
            "mjs",
            "cjs",
            "ts",
            "tsx",
            "jsx",
            "java",
            "c",
            "h",
            "cpp",
            "hpp",
            "cc",
            "cs",
            "go",
            "rs",
            "rb",
            "php",
            "swift",
            "kt",
            "kts",
            "scala",
            "sh",
            "bash",
            "ps1",
            "bat",
            "cmd",
            "html",
            "htm",
            "css",
            "scss",
            "sass",
            "less",
            "sql",
            "json",
            "yaml",
            "yml",
            "toml",
            "ini",
            "cfg",
            "xml",
            "ipynb",
            "r",
            "lua",
            "pl",
            "dart",
            "vue",
            "svelte",
        }
    ),
    "Executables": frozenset(
        {"exe", "msi", "app", "dmg", "pkg", "deb", "rpm", "apk", "jar", "bin", "run"}
    ),
    "Fonts": frozenset({"ttf", "otf", "woff", "woff2", "eot", "fon"}),
    "Data": frozenset(
        {
            "csv",
            "tsv",
            "db",
            "sqlite",
            "sqlite3",
            "parquet",
            "feather",
            "dat",
            "log",
            "bak",
            "sav",
            "dta",
            "h5",
            "hdf5",
            "npy",
            "npz",
            "pkl",
            "pickle",
        }
    ),
    "Design": frozenset(
        {"psd", "ai", "xd", "fig", "sketch", "indd", "blend", "obj", "fbx", "stl", "3ds", "dwg"}
    ),
}

EXTENSION_TO_CATEGORY: dict[str, str] = {
    extension: category
    for category, extensions in CATEGORY_EXTENSIONS.items()
    for extension in extensions
}

UNKNOWN_CATEGORY = "Other"
NO_EXTENSION = "No Extension"


def category_for(extension: str) -> str:
    """Return the category for an extension written without a leading dot."""
    return EXTENSION_TO_CATEGORY.get(extension.lower(), UNKNOWN_CATEGORY)
