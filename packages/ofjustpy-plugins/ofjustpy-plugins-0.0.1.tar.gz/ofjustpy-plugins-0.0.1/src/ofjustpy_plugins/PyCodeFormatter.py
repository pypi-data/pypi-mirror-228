"""
leverage pygments to build ofjustpy component to display formatted python code

"""
import ofjustpy as oj
from ofjustpy.SHC_types import ActiveComponents as AC
from ofjustpy.SHC_types import PassiveComponents as PC
from py_tailwind_utils import bg
from py_tailwind_utils import fc
from py_tailwind_utils import gray
from py_tailwind_utils import green
from py_tailwind_utils import tstr
from pygments import highlight
from pygments.formatter import Formatter
from pygments.formatters import HtmlFormatter as pygHtmlFormatter
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import STANDARD_TYPES

from .EmacsStyle import EmacsTailwindStyle as TokenStyle


class HtmlFormatter(pygHtmlFormatter):
    def __init__(
        self,
        *args,
        twsty_tags=[],
        span_hc_gen=PC.Span,
        code_hc_gen=PC.Code,
        pre_hc_gen=PC.Pre,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # class style for top level div
        self.twsty_tags = twsty_tags
        self.span_hc_gen = span_hc_gen
        self.code_hc_gen = code_hc_gen
        self.pre_hc_gen = pre_hc_gen

        # we will think about styles in some time
        # self.style = get_style_by_name('default')  # use 'emacs' style

    def _format_lines(self, tokensource):
        for ttype, value in tokensource:
            style_class = self.style.styles.get(ttype)
            style_class = style_class.strip() if style_class else ""
            style_label = STANDARD_TYPES.get(ttype, "")
            css_class = self.ttype2class.get(ttype)
            pcp = [fc / green / 1]
            if ttype in TokenStyle:
                twsty_tags = TokenStyle[ttype]
            else:
                print(f"{ttype} not found in TokenStyle mapping")
            # print ("----------------------------------------")

            # print(f"Type: {ttype}, \n Value: {value}, \n CSS-class: {css_class},  \n CSS-Label: {style_label}, \n Style-Class: {style_class}")
            # print ("------------------DONE----------------------")
            # print ("pcp = ", pcp, " ", tstr(*pcp))
            yield self.span_hc_gen(
                text=value, twsty_tags=twsty_tags
            )  # oj.Span_(text=value, pcp=pcp)
        # yield oj.Span_(text="Stand in for code")

    def _wrap_code(self, inner):
        """
        wrap the code content within code block
        """
        print("=======================> add childs ")
        yield self.code_hc_gen(
            childs=[_ for _ in inner]
        )  # oj.Code_(cgens= [_ for _ in inner])

    def _wrap_pre(self, inner):
        """
        wrap code block within pre so that new line/whitespaces are renderecd
        """
        yield self.pre_hc_gen(
            childs=[_ for _ in inner]
        )  # oj.Pre_(cgens= [_ for _ in inner], pcp=self.pcp)

    def format_unencoded(self, tokensource, outfile):
        """
        for each token generate a oj.htmlcomponent instance
        """

        # generator for all the code-token-components
        source = self._format_lines(tokensource)

        # --------------------We will open this one by one -----------

        # As a special case, we wrap line numbers before line highlighting
        # so the line numbers get wrapped in the highlighting tag.
        # if not self.nowrap and self.linenos == 2:
        #     source = self._wrap_inlinelinenos(source)

        # if self.hl_lines:
        #     source = self._highlight_lines(source)

        # will think about this
        # if self.lineanchors:
        #     source = self._wrap_lineanchors(source)
        # if self.linespans:
        #     source = self._wrap_linespans(source)

        # wrap the code around pre and code
        source = self.wrap(source)

        # Note: will get back to this
        # if self.linenos == 1:
        #     source = self._wrap_tablelinenos(source)
        # source = self._wrap_div(source)

        # wrap full is removed
        #
        # ------------------------------------------------------------

        # for t, piece in source:
        #     outfile.write(piece)
        return source


def format_code(code, twsty_tags=[], **kwargs):
    lexer = PythonLexer()
    oj.set_style("un")
    formatter = HtmlFormatter(wrap_code=True, twsty_tags=twsty_tags, **kwargs)
    tokens = lexer.get_tokens(code)
    # everything is wrapped with pre component
    source = [_ for _ in formatter.format(tokens, None)][0]

    return source
