import bot
import conf
import click


@click.group()
def cli():
    """
    Take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.
    """


@cli.command(
    'snapshot',
    short_help = "Take a snapshot of your wallet",
    help = "Take a snapshot of the binance wallet and save it for further plotting"
)
@click.option(
    '--debug/--no-debug',
    default=False,
    help="Prints debug data"
)
def snapshot(debug):
    crypto_report = bot.crypto.get_report(debug)
    crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
    print('Snapshot saved')


@cli.command(
    'output',
    short_help = 'Output the previously stored data',
    help = "Output the previously stored data with 'snapshot'"
)
@click.option(
    '--type',
    default='print',
    help="The way the data is shown. Options : print, http"
)
@click.option(
    '--relative/--no-relative',
    default = False,
    help = "If the graph should be plotted relative to its initial value"
)
@click.option(
    '--port',
    default=8080,
    help="The port to send the data. To be used with --type http"
)
@click.option(
    '--symbol',
    default=conf.CURRENCY,
    help="""The currency the graph will be plotted on.
To plot several symbols on the same graph, separate them by a coma.
If plotting several symbols, the --relative option is enabled.
To plot all symbols, use '*'.
Default : FIAT"""
)
def output(type, relative, port, symbol):
    if symbol == '*':
        symbol = conf.COINS
    else:
        symbol = symbol.split(',')
        for s in symbol:
            assert s in conf.COINS+[conf.CURRENCY]
    if len(symbol) > 1:
        relative = True
    reports = bot.crypto.get_previous_reports()
    if len(reports) == 0:
        msg = "No snapshot in database. Run at least once main.py --snapshot"
        figname = None
    else:
        msg = "*** \n### Crypto report 📈 : \n***\n\n"
        msg += bot.crypto.format_report(reports[-1])
        figname = bot.crypto.plot_symbol(reports, symbol, relative)

    bot.io.output(msg, figname, type, port)


if __name__ == "__main__":
    cli()
