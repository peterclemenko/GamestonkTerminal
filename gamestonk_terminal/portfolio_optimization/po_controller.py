""" Portfolio Optimization Controller Module """
__docformat__ = "numpy"

import argparse
from typing import List
import matplotlib.pyplot as plt
from prompt_toolkit.completion import NestedCompleter
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair, parse_known_args_and_warn
from gamestonk_terminal.menu import session
from gamestonk_terminal.portfolio_optimization import optimizer_view


class PortfolioOptimization:

    CHOICES = [
        "help",
        "q",
        "quit",
        "select",
        "add",
        "equal",
        "mktcap",
        "dividend",
        "property",
        "maxsharpe",
        "minvol",
        "effret",
        "effrisk",
        "maxquadutil",
        "ef",
        "ca",
        "yolo",
    ]

    # pylint: disable=dangerous-default-value
    def __init__(self, tickers: List[str] = []):
        """
        Construct Portfolio Optimization
        """

        self.po_parser = argparse.ArgumentParser(add_help=False, prog="po")
        self.po_parser.add_argument("cmd", choices=self.CHOICES)
        self.tickers = list(set(tickers))
        # These will allow the ca menu to be re-access
        self.ca_ticker = None
        self.ca_similar = None

    @staticmethod
    def print_help(tickers: List[str]):
        """Print help"""
        print("\nPortfolio Optimization:")
        print("   help          show this menu again")
        print("   q             quit this menu, and shows back to main menu")
        print("   quit          quit to abandon program")
        print(f"\nCurrent Tickers: {('None', ', '.join(tickers))[bool(tickers)]}")
        print("")
        print("   add           add ticker to optimize")
        print("   select        overwrite current tickers with new tickers")
        print("")
        print("Optimization:")
        print("   equal         equally weighted")
        print("   mktcap        weighted according to market cap (property marketCap)")
        print(
            "   dividend      weighted according to dividend yield (property dividendYield)"
        )
        print("   property      weight according to selected info property")
        print("")
        print("Mean Variance Optimization:")
        print(
            "   maxsharpe     optimizes for maximal Sharpe ratio (a.k.a the tangency portfolio)"
        )
        print("   minvol        optimizes for minimum volatility")
        print(
            "   maxquadutil   maximises the quadratic utility, given some risk aversion"
        )
        print("   effret        maximises return for a given target risk")
        print("   effrisk       minimises risk for a given target return")
        print("")
        print("   ef            show the efficient frontier")
        print("")
        if tickers:
            print("   > ca          comparison analysis for selected tickers")
            print("")

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """
        (known_args, other_args) = self.po_parser.parse_known_args(an_input.split())

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help(self.tickers)

    def call_q(self, _):
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_add(self, other_args: List[str]):
        """Process add command"""
        self.add_stocks(other_args)

    def call_select(self, other_args: List[str]):
        """Process select command"""
        self.tickers = []
        self.add_stocks(other_args)

    def call_equal(self, other_args: List[str]):
        """Process equal command"""
        optimizer_view.equal_weight(self.tickers, other_args)

    def call_mktcap(self, other_args: List[str]):
        """Process mktcap command"""
        other_args.insert(0, "marketCap")
        optimizer_view.property_weighting(self.tickers, other_args)

    def call_dividend(self, other_args: List[str]):
        """Process dividend command"""
        other_args.insert(0, "dividendYield")
        optimizer_view.property_weighting(self.tickers, other_args)

    def call_property(self, other_args: List[str]):
        """Process property command"""
        optimizer_view.property_weighting(self.tickers, other_args)

    def call_maxsharpe(self, other_args: List[str]):
        """Process maxsharpe command"""
        optimizer_view.max_sharpe(self.tickers, other_args)

    def call_minvol(self, other_args: List[str]):
        """Process minvol command"""
        optimizer_view.min_volatility(self.tickers, other_args)

    def call_maxquadutil(self, other_args: List[str]):
        """Process maxquadutil command"""
        optimizer_view.max_quadratic_utility(self.tickers, other_args)

    def call_effrisk(self, other_args: List[str]):
        """Process effrisk command"""
        optimizer_view.efficient_risk(self.tickers, other_args)

    def call_effret(self, other_args: List[str]):
        """Process effret command"""
        optimizer_view.efficient_return(self.tickers, other_args)

    def call_ef(self, other_args):
        """Process ef command"""
        optimizer_view.show_ef(self.tickers, other_args)

    def call_yolo(self, _):
        # Easter egg :)
        print("DFV YOLO")
        print({"GME": 200})
        print("")

    def add_stocks(self, other_args: List[str]):
        """ Add ticker or Select tickes for portfolio to be optimized """
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="add/select",
            description="""Add/Select tickers for portfolio to be optimized.""",
        )
        parser.add_argument(
            "-t",
            "--tickers",
            dest="add_tickers",
            type=lambda s: [str(item).upper() for item in s.split(",")],
            default=[],
            help="tickers to be used in the portfolio to optimize.",
        )
        try:
            if other_args:
                if "-" not in other_args[0]:
                    other_args.insert(0, "-t")

            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return
            tickers = set(self.tickers)
            for ticker in ns_parser.add_tickers:
                tickers.add(ticker)

            if self.tickers:
                print(
                    f"\nCurrent Tickers: {('None', ', '.join(tickers))[bool(tickers)]}"
                )

            self.tickers = list(tickers)

        except Exception as e:
            print(e)

        print("")


def menu(tickers: List[str]):
    """Portfolio Optimization Menu"""
    if tickers == [""]:
        tickers = []
    plt.close("all")
    po_controller = PortfolioOptimization(tickers)
    po_controller.call_help(tickers)

    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in po_controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (po)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (po)> ")

        try:
            plt.close("all")

            process_input = po_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
