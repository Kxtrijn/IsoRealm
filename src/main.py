import traceback
from engine.game import Game


def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print('Error running game:', e)
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()