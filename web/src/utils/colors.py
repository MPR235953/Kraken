def css_to_dict(path: str):
    css_dict = {}
    with open(path, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            if "--" in line:
                key, value = line.split(": ")
                css_dict[key.strip()] = value.split(';')[0]
            else: continue
    return css_dict

colors = {}
if not colors:
    colors = css_to_dict(path="src/assets/css/colors.css")
