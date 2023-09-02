from ofjustpy_plugins import format_code
from addict import Dict
import ofjustpy as oj
from py_tailwind_utils import *

code = """
                         text_input_ = oj.TextInput_("myTextInput",
                            value="initialValue",
                            placeholder="Enter something...",
                            autocomplete=True,
                            maxlength=20,
                            minlength=5,
                            pattern="^[a-zA-Z0-9]*$",
                            readonly=False,
                            required=True,
                            size=30,
                            debug=True,
                            pcp=[bg/blue/"100/50"])
                         """

#formatted code tree
# use no extrawhitespace style
oj.set_style("un")
fct = format_code(code)
oj.set_style("snow")
btn = oj.AC.Button(key="styled_button", text="abtn")
app = oj.load_app()

wp_endpoint = oj.create_endpoint(key="example_001",
                                 childs = [oj.PC.Title("Ofjustpy Formatted Code Demo",
                                                       twsty_tags=[mr/st/8, mr/sb/8]),
                                           fct,
                                           oj.PC.Hr(),
                                           oj.PC.TitledPara("Switching back to default styling", btn)
                                           ]
                                 )


oj.add_jproute("/", wp_endpoint)

