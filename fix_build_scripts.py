#!/usr/bin/env python3
import glob
import os

target_dir = os.path.dirname(os.path.abspath(__file__))
py_files = glob.glob(os.path.join(target_dir, "*.py"))

for py_file in py_files:
    if os.path.basename(py_file) == 'fix_build_scripts.py':
        continue
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace hardcoded absolute path with relative path code
    old_target = "/Users/shivanshinigam/.gemini/antigravity-ide/scratch/commerceos/index.html"
    if old_target in content:
        new_code = "os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')"
        content = content.replace(f"'{old_target}'", new_code)
        content = content.replace(f'"{old_target}"', new_code)

        with open(py_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed paths in {os.path.basename(py_file)}")
