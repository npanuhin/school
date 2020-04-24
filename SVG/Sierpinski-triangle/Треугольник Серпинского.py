# from os import system as show


def draw_serpinsky(x, y, width, height, n):
    if n == 1:
        return """<polygon points="{},{} {},{} {},{}" fill="{}" />""".format(
            x, y + height,
            x + width / 2, y,
            x + width, y + height,
            color
        )

    top = draw_serpinsky(x + width / 4, y, width / 2, height / 2, n - 1)
    left = draw_serpinsky(x, y + height / 2, width / 2, height / 2, n - 1)
    right = draw_serpinsky(x + width / 2, y + height / 2, width / 2, height / 2, n - 1)

    return """\t{}\n\t{}\n\t{}""".format(top, left, right).strip()


width = 1000
height = width * 3**(1 / 2) / 2
color = "#0053e0"

n = int(input("n = "))

svg = """
<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {} {}">
{content}
</svg>
""".format(width, height, content=draw_serpinsky(0, 0, width, height, n))

with open("Треугольник Серпинского.svg", 'w', encoding="utf-8") as file:
    file.write(svg.strip())

# Show result:
# show("Треугольник Серпинского.svg")
