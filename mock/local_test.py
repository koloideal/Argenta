from argenta.command.flag.defaults import PredefinedFlags

router = Router()
flag = PredefinedFlags.SHORT_HELP

@router.command(Command('test', flags=flag))
def test(args: InputFlags):
    print(f'help for {args.get_flag('h').get_name()} flag')

app = App(override_system_messages=True,
          print_func=print)
app.include_router(router)
app.run_polling()