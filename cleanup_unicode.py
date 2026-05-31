import os, re

root = r"D:\DSA_Training"
fixed = 0

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d != ".git"]
    for f in filenames:
        if f.endswith((".py", ".md", ".yml", ".yaml")):
            fp = os.path.join(dirpath, f)
            try:
                with open(fp, "r", encoding="utf-8") as fh:
                    content = fh.read()

                original = content
                content = content.replace("\u2014", "--")
                content = content.replace("\u2013", "-")
                content = content.replace("\u2018", "'").replace("\u2019", "'")
                content = content.replace("\u201C", '"').replace("\u201D", '"')
                content = content.replace("\u2022", "-")
                content = content.replace("\u2026", "...")
                content = content.replace("\u00D7", "x")

                def replace_non_ascii(m):
                    c = m.group(0)
                    cp = ord(c)
                    if 0x2500 <= cp <= 0x2593 or cp == 0x20B9:
                        return c
                    if 0x00A0 <= cp <= 0x00FF:
                        return c
                    return ""

                content = re.sub(r"[^\x00-\x7F]", replace_non_ascii, content)

                if content != original:
                    with open(fp, "w", encoding="utf-8") as fh:
                        fh.write(content)
                    fixed += 1
                    print(f"Fixed: {os.path.relpath(fp, root)}")
            except Exception as e:
                print(f"Error: {fp}: {e}")

print(f"\nTotal files cleaned: {fixed}")
