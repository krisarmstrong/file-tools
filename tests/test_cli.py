from file_tools import __main__ as cli


def test_build_parser():
    parser = cli.build_parser()
    assert parser.description.startswith("Swiss-army")
