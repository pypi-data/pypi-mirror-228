#!python

"""
Run the http spec tests in an arbitrary YAML file or files.
Why would you want to do this? You most likely want to run your tests
with pytest instead. That is why a `conftest.py` file is provided.

There are other use cases where you might want to run tests programmatically,
perhaps from another existing python program or script. In such case, this
small script provides a starting point for how to invoke the `http_test.runner`
module.
"""

import click

from http_test.runner import run_specfiles


@click.command()
@click.option(
    "test_files",
    "--test-file",
    "-f",
    required=True,
    multiple=True,
    type=click.Path(exists=True),
    help="Path to the YAML test file",
)
@click.option(
    "verbose",
    "--verbose",
    "-v",
    is_flag=True,
    help="Print verbose output",
)
def run_tests(test_files, verbose=False):
    run_specfiles(test_files, verbose=verbose)


if __name__ == "__main__":
    fail_count = run_tests()
    exit(fail_count)
