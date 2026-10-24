import os
import re
import sys
from pathlib import Path

changed_file, output_file = sys.argv[1:3]
changed = {Path(line.strip()).as_posix() for line in open(changed_file) if line.strip()}

roots = sorted(Path("latex_files").glob("**/main.tex"))

commands = re.compile(
    r"""\\(?:input|include|subfile|bibliography|addbibresource|includegraphics)
    \s*(?:\[[^\]]*\]\s*)?\s*\{([^}]+)\}""",
    re.X,
)


def resolve(base, name):
    name = name.strip()
    if name.startswith("\\") or "#" in name:
        return []
    path = Path(name)
    if not path.suffix:
        candidates = [
            base / (name + ".tex"),
            base / (name + ".bib"),
            base / (name + ".pdf"),
            base / (name + ".png"),
            base / (name + ".jpg"),
            base / (name + ".jpeg"),
            base / (name + ".svg"),
            base / (name + ".eps"),
        ]
    else:
        candidates = [base / name]
    return [p for p in candidates if p.is_file()]


def dependencies(file, seen=None):
    if seen is None:
        seen = set()
    file = file.resolve()
    if file in seen or not file.is_file():
        return seen
    seen.add(file)

    try:
        text = file.read_text(errors="replace")
    except OSError:
        return seen

    text = re.sub(r"(?<!\\)%.*", "", text)  # Remove comments

    for name in commands.findall(text):
        for dep in resolve(file.parent, name):
            dependencies(dep, seen)

    return seen


affected = []
for root in roots:
    deps = dependencies(root)
    relative_deps = {
        p.relative_to(Path.cwd()).as_posix()
        for p in deps
        if p.is_relative_to(Path.cwd())
    }
    if changed & relative_deps:
        affected.append(root.as_posix())

with open(output_file, "a") as out:
    out.write("root_files<<EOF\n")
    out.write("\n".join(affected) + "\n")
    out.write("EOF\n")

if not affected:
    print("No affected main.tex documents.")
