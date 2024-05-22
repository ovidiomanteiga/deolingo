
import clingo
import sys

from dotenv import load_dotenv

from deolingo._application import DeolingoApplication


def main():
    """Run the deolingo application."""
    load_dotenv()
    app = DeolingoApplication()
    sys.exit(int(clingo.clingo_main(app)))


if __name__ == '__main__':
    main()
