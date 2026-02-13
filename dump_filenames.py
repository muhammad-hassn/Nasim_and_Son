import os
import sys

# Reconfigure stdout for UTF-8 to prevent character mapping errors in some environments
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def dump():
    folders = ['DYK-PAD YHG', 'DYK-WET CAN01', 'DYN-BLEACH SBX01', 'PRD-ZYME STN01']
    all_files = []
    for folder in folders:
        if os.path.exists(folder):
            for fn in os.listdir(folder):
                all_files.append(f"{folder}/{fn}")
    
    with open('all_filenames.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_files))
    print(f"Dumped {len(all_files)} filenames to all_filenames.txt")

if __name__ == "__main__":
    dump()
