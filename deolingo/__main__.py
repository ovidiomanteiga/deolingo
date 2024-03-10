
import clingo
import sys

from deolingo._application import DeolingoApplication
from deolingo.control import DeolingoControl


def main():
    """
    Run the deolingo application.
    """
    app = DeolingoApplication()
    sys.exit(int(clingo.clingo_main(app)))


if __name__ == '__main__':
    main()

