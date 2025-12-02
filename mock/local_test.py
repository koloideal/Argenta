from argenta import Router, Command

router = Router()
@router.command(Command('some', aliases=['test', 'case']))
def handler(response): # pyright: ignore[reportUnusedFunction]
    pass
@router.command(Command('ext', aliases=['more', 'foo']))
def handler2(response): # pyright: ignore[reportUnusedFunction]
    pass
    
print(router.aliases)