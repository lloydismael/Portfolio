from pathlib import Path

from PIL import Image

src = Path(__file__).resolve().parent / "static" / "img" / "avatar-linkedin.png"
img_dir = src.parent
im = Image.open(src).convert("RGBA")

w, h = im.size
side = min(w, h)
left = (w - side) // 2
# Bias the crop toward the face so the tab icon stays readable.
top = max(0, (h - side) // 5)
sq = im.crop((left, top, left + side, top + side))


def save_png(size: int, name: str) -> Image.Image:
    out = sq.resize((size, size), Image.Resampling.LANCZOS)
    path = img_dir / name
    out.save(path, "PNG", optimize=True)
    print(f"{path.name}: {path.stat().st_size} bytes ({size}x{size})")
    return out


save_png(32, "favicon-32.png")
save_png(48, "favicon-48.png")
save_png(180, "apple-touch-icon.png")
save_png(192, "favicon-192.png")

ico_path = img_dir / "favicon.ico"
sq.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print(f"favicon.ico: {ico_path.stat().st_size} bytes")
