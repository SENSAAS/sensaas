import numpy as np


def save_trans_sdf(SDFfile, tran, output):
    with open(SDFfile, 'r') as f:
        lines = f.readlines()

    header_line = lines[3].strip()
    parts = header_line.split()

    # Fix for unusual spacing cases
    if len(parts[0]) > 2:
        # Re-split based on custom logic in original code
        # Attempt to parse nbatom and nbbond from header_line directly
        # This logic assumes the first token has nbatom and some extra characters
        # Safer approach:
        # Extract numeric parts by parsing substrings as int
        # But since original is a bit unclear, do a fallback
        # We'll parse first 3 chars as nbatom, then the rest as nbbond
        try:
            nbatom = int(parts[0][:2])
            nbbond = int(parts[0][2:])
            if len(parts) > 1:
                nbbond = int(parts[1])  # fallback to second token if exists
        except ValueError:
            # fallback to standard parsing
            nbatom = int(parts[0])
            nbbond = int(parts[1])
    else:
        nbatom = int(parts[0])
        nbbond = int(parts[1])

    # Read atom coordinates lines
    atom_lines = lines[4:4 + nbatom]

    xyz = np.array([list(map(float, line.split()[:3])) for line in atom_lines], dtype=np.float64)

    # Create homogeneous coords for matrix multiplication (Nx4)
    ones_col = np.ones((nbatom, 1), dtype=np.float64)
    xyz_hom = np.hstack([xyz, ones_col])

    # Apply transformation matrix: tran shape should be (4,4)
    xyz_tran = (tran @ xyz_hom.T).T[:, :3]

    # Prepare output lines
    out_lines = []
    for i, line in enumerate(lines):
        if 4 <= i < 4 + nbatom:
            tokens = line.split()
            # Format transformed coords with 5.3f and width 10
            coords_str = ''.join(f"{c:10.3f}" for c in xyz_tran[i - 4])
            # Keep element symbol and rest of the line as is
            rest = ' '.join(tokens[3:])
            if rest:
                out_line = f"{coords_str} {rest}"
            else:
                out_line = coords_str
            out_lines.append(out_line.rstrip() + '\n')
        else:
            out_lines.append(line)

    # Write transformed SDF file
    with open(output, 'w') as f:
        f.writelines(out_lines)
