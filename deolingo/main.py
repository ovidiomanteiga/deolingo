
import clingo
from _application import DeolingoApplication
import sys


def main():
    """
    Run the deolingo application.
    """
    sys.exit(int(clingo.clingo_main(DeolingoApplication(), sys.argv[1:])))


if __name__ == '__main__':
    main()
