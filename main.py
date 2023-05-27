from game import Game


if __name__ == "__main__":
    w, h = 20, 20

    game = Game.generate_random_shape("square", (w, h))
    game.populate_numbers()
    game.shape.print_ascii()
    game.shape.print_numbers()
