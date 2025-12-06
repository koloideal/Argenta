from argenta import App, DataBridge, Response, Router
from argenta.di import FromDishka
from argenta.di.integration import setup_dishka, _auto_inject_handlers
from argenta.di.providers import SystemProvider
from dishka import make_container

container = make_container()

Response.patch_by_container(container)

app = App()
router = Router()

@router.command('command')
def handler(res: Response, data_bridge: FromDishka[DataBridge]):
    print(data_bridge)
    
_auto_inject_handlers(app)
_auto_inject_handlers(app)
