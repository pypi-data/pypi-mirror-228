# coding=utf-8
"""
sitec.cli.pth Module
"""
import click

# import sys, types, os
# has_mfs = sys.version_info > (3, 5);
# p = os.path.join(sys._getframe(1).f_locals['sitedir'], *('sphinxcontrib',))
# importlib = has_mfs and __import__('importlib.util')
# has_mfs and __import__('importlib.machinery')
# m = has_mfs and sys.modules.setdefault(
#     'sphinxcontrib',
#     importlib.util.module_from_spec(importlib.machinery.PathFinder.find_spec('sphinxcontrib', [os.path.dirname(p)])))
# m = m or sys.modules.setdefault('sphinxcontrib', types.ModuleType('sphinxcontrib'))
# mp = (m or[]) and m.__dict__.setdefault('__path__',[]);(p not in mp) and mp.append(p)


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def pth(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


if __name__ == '__main__':
    pth()
