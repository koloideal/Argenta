from argenta import App, Router, Command, Response


app = App(override_system_messages=True)
router = Router()

@router.command(Command('test', aliases={'alias', 'primer'}))
def handler(res: Response):
    pass
    
@router.command(Command('test2', aliases={'alias', 'primer'}))
def handler2(res: Response):
    pass

print(router.aliases)