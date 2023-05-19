import Generate
from Slitherlink import Edge, Game
import data

if __name__ == "__main__":
    edges = [Edge(i) for i in range(220)]
    cells = data.cells(edges)
    junctions = data.junctions(edges)
    [c.update() for c in cells]
    [j.update() for j in junctions]
    game = Game(cells, junctions, edges)
    game.setup_variables()
    gen = Generate.Generate(game.data["cells"], game.data["junctions"])
    Generate.foo([val.value for val in list(gen.gen_loop().values())])
