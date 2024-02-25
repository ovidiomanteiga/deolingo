
import clingo
import sys

from _application import DeolingoApplication


def main():
    """
    Run the deolingo application.
    """
    app = DeolingoApplication()
    sys.exit(int(clingo.clingo_main(app)))


if __name__ == '__main__':
    main()

