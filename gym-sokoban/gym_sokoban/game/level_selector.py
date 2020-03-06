def read_levels_from_file(filename: str):
    # path = os.path.join(LEVEL_DIR, filename)

    levels = []
    level_idx = -1

    with open(filename, 'r') as data:
        for cnt, line in enumerate(data):
            if line.startswith(';'):
                level_idx += 1
                levels.append([])
            else:
                levels[level_idx].append(list(line.rstrip()))

    return levels
