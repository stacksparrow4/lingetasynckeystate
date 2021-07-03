mapping = []

with open("win_keycodes.txt", "r") as f:
    xna_lines = [l.strip() for l in f.readlines() if l.strip()]

with open("x_syms.txt", "r") as f:
    x_lines = [l.strip().split()[1:] for l in f.readlines() if "#define " in l]

added_chars = []

for cs_line in xna_lines:
    name, num_raw = cs_line.split(' = ')
    num = int(num_raw, 16) if num_raw.startswith("0x") else int(num_raw)

    # find the correct sym
    match = "XK_" + (name[3:] if name.startswith("VK_") else name)
    if name == "VK_LCONTROL" or name == "VK_LSHIFT" or name == "VK_LWIN" or name == "VK_LMENU" or name == "VK_RCONTROL" or name == "VK_RSHIFT" or name == "VK_RWIN" or name == "VK_RMENU":
        match = "XK_" + name[4:] + "_" + name[3]
    elif name == "VK_OEM_PLUS":
        match = "XK_equal"
    elif name == "VK_OEM_4":
        match = "XK_bracketleft"
    elif name == "0xDD":
        match = "XK_bracketright"
    elif name == "VK_OEM_MINUS":
        match = "XK_minus"
    elif name == "VK_BACK":
        match = "XK_BackSpace"
    for sym in x_lines:
        if sym[0].lower() == match.lower():
            while len(mapping) <= num:
                mapping.append("-1")
            mapping[num] = sym[1]
            added_chars.append(name)

print("Characters added: ", added_chars)

print("\nINSERT THE FOLLOWING LINE:\n")

print("int xna_keycode_to_x11_sym[] = {" + ", ".join(mapping) + "};")