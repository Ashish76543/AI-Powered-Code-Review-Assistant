def extract_added_code(patch):
    ##if the patch is empty return
    if not patch:
        return ""

    lines = []

    for line in patch.splitlines():
        ##take each line from patch,splitlines based on \n
        if line.startswith("+"):
            ##if line starts with +,we only use addedd lines for further process
            if not line.startswith("+++"):##if +++ it indicates metadat is it is ignored
                lines.append(line[1:])##we append everything after +

    return "\n".join(lines)##combine all lines to 1 string