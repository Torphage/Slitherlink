from game import Game


if __name__ == "__main__":
    w, h = 10, 10
    screen_size = (800, 800)

    game = Game.generate_random_shape("square", (w, h))
    game.populate_numbers()
    game.shape.print_ascii()
    game.shape.print_numbers()
    game.play(screen_size)
