import os
import sys

# Setup stdout for UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def find_matches():
    target_products = [
        "DYK-PAD GOLD YELLOW", "BOOST OXY", "DYK -COAT KR", "DYK-ACID ANT",
        "BIOPIL AT", "DYK-ACID NTR", "BIOPIL ATM", "DYK-ACID OLL", "DYK-ACID TG",
        "DYK-ACID TPR", "DYK-ACID BF", "DYK-ACTIV CL", "DYK-ACTIV CS",
        "DYK-ACTIV PM", "DYK-ACTIV PP", "DYK-BND HD", "DYK-BND HRD",
        "DYK-BND MD", "DYK-BND MDL", "DYK-BND SFF", "DYK-BND SFT",
        "DYK-BND SRR", "DYK-BUFFER DF", "DYK-BND SRT", "DYK-BUFFER ASH",
        "DYK-BUFFER SA", "DYK-BUFFER YSS", "DYK-CARRIER ECO", "DYK-CARRIER PS",
        "DYK-BUFFER TA", "DYK-BUFFER TAK", "DYK-CLEAN 11", "DYK-CLEAN ROLL",
        "DYK-COAT EYP", "DYK-COAT EYP-B", "DYK-CLEAN OK", "DYK-CLEAN PL4",
        "DYK-COAT HD", "DYK-COAT HDD", "DYK-COAT HR", "DYK-COAT KMR",
        "DYK-COAT KMR-D", "DYK-COAT KR", "DYK-COAT KRR", "DYK-COAT MR",
        "DYK-COAT MRD", "DYK-COAT MRD-N"
    ]

    folders = ['DYK-PAD YHG', 'DYK-WET CAN01', 'DYN-BLEACH SBX01', 'PRD-ZYME STN01']
    all_files = []
    for folder in folders:
        if os.path.exists(folder):
            for fn in os.listdir(folder):
                all_files.append((folder, fn))

    for target in target_products:
        print(f"\nSearching for: {target}")
        matches = []
        target_norm = target.upper().replace(' ', '').replace('-', '')
        
        # Split target into keywords
        keywords = target.upper().replace('-', ' ').split()
        
        for folder, fn in all_files:
            fn_upper = fn.upper().replace(' ', '').replace('-', '')
            fn_raw = fn.upper()
            
            # Look for exact or fuzzy matches
            if target_norm in fn_upper or fn_upper in target_norm:
                matches.append((folder, fn))
                continue
            
            # Keyword matching
            matched_keywords = [kw for kw in keywords if kw in fn_raw]
            if len(matched_keywords) >= 2: # At least 2 keywords match
                 matches.append((folder, fn))

        if matches:
            for m in list(set(matches)):
                print(f"  MATCH: {m[0]}/{m[1]}")
        else:
            print("  No matches found.")

if __name__ == "__main__":
    find_matches()
