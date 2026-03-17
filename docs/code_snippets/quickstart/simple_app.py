from argenta import App, Command, Orchestrator, Router, Response
from argenta.command import Flag

# 1. Create app and orchestrator instances
app = App(
    prompt=">> ",
    initial_message="Simple App",
    farewell_message="Goodbye!",
    repeat_command_groups_printing=False,
)
orchestrator = Orchestrator()

# 2. Create router for grouping commands
main_router = Router(title="Main commands")


# 3. Define command and its handler
@main_router.command(Command("hello", description="Prints greeting message", flags=Flag("name")))
def hello_handler(response: Response):
    """This handler will be called for 'hello' command."""
    name = response.input_flags.get_flag_by_name("name")
    if name:
        print(f"Hello, {name.input_value}!")
    else:
        print("Hello, world!")


# 4. Include router to application
app.include_router(main_router)

# 5. Start application
if __name__ == "__main__":
    orchestrator.run_repl(app)
