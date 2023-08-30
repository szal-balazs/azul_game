from azul import game, player


def main():
    players = [player.Player('Alice'), player.Player('Bob'), player.SmarterPlayer('Larx')]
    g = game.Game(players)
    g.play()


if __name__ == '__main__':
    main()
