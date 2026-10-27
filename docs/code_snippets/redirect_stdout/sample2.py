from argenta import App, Orchestrator
from argenta.repl import REPLConfig, StaticDividingLine

app = App()

# All routers will use static line with length 50 by default
Orchestrator().run_repl(app, REPLConfig(dividing_line=StaticDividingLine(length=50)))
