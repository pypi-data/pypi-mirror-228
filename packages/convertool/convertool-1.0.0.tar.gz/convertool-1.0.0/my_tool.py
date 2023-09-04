import click
from app.application import convert_to_grayscale


@click.group()
def cli():
    pass


@cli.command()
def hello_world():
    click.echo("Hello World!")


@cli.command()
@click.option('-n', '--name', type=str, help='Name to greet', default='World')
def hello(name):
    click.echo(f'Hello {name}')


@cli.command()
@click.option('--input', type=str, help='Input image path', default='')
@click.option('--output', type=str, help='Output image path', default='')
def convert(input, output):
    convert_to_grayscale(input, output)
    click.echo(f'input: {input}, output: {output}')
