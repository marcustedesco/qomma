import sys
import os
import qomma.core as core

def main(args=None):
    """main routine"""
    if args is None:
        args = sys.argv[1:]

    path: str = str(sys.argv[1])
    directory: str = os.path.basename(os.path.normpath(path))

    tables: dict = core.load_tables(path)
    core.print_tables_found(tables)
    core.handle_input_queries(directory, tables)

if __name__ == "__main__":
    sys.exit(main())
