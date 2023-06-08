from game import Game


if __name__ == "__main__":
    w, h = 12, 12
    screen_size = (900, 900)

    # game = Game.generate_random_shape("square", size2=(w, h))
    game = Game.generate_random_shape("hexagon", size1=4)
    game.populate_numbers()
    game.shape.print_ascii()
    game.shape.print_numbers()
    game.play(screen_size, font_size=40)
