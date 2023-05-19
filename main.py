import Generate
from Slitherlink import Edge, Game
import data

if __name__ == "__main__":
    w, h = 20, 20
    edges = [Edge(i) for i in range(2 * w * h + w + h)]
    gen = Generate.Rectangle.generate(w, h)
    cells = gen.cells
    junctions = gen.junctions
    [c.update() for c in cells]
    [j.update() for j in junctions]
    game = Game(cells, junctions, edges)
    game.setup_variables()
    Generate.foo([val.value for val in list(gen.gen_loop().values())])
