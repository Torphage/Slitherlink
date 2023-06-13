import sys

from game import Game


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "square":
        game = Game.generate_random_shape("square", size2=(8, 8))
    else:
        game = Game.generate_random_shape("hexagon", size1=12)

    game.populate_numbers()
    game.shape.print_ascii()
    game.shape.print_numbers()
    game.play((900, 900), font="arial", font_size=20, stretch=False)
