with open(r'd:\peach_store\peach_admin\src\viewmodels\AdminViewModel.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'fetchstats' in line.lower():
        print(f"Line {i+1}: {line.strip()}")
