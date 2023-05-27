from game import Game


if __name__ == "__main__":
    w, h = 20, 20

    game = Game.generate_random("square", (w, h))
    game.shape.print_ascii()
