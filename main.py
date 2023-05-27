import generator.shapes as shapes
from slitherlink import Game


if __name__ == "__main__":
    w, h = 20, 20
    gen = shapes.Rectangle.generate(w, h)
    edges = gen.edges
    cells = gen.cells
    junctions = gen.junctions
    [c.update() for c in cells]
    [j.update() for j in junctions]
    game = Game(cells, junctions, edges)
    game.setup_variables()
    gen.foo([val.value for val in list(gen.gen_loop().values())])
