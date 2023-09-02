from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class SpooferPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.event_dispatcher.add_listener(
            COMMAND, self.spoof_request
        )

    def spoof_request(
            self,
            event: ConsoleCommandEvent,
            event_name: str,
            dispatcher: EventDispatcher
    ) -> None:
        command = event.command
        if not isinstance(command, EnvCommand):
            return

        io = event.io

        if io.is_debug():
            io.write_line(
                "<debug>Loading environment variables.</debug>"
            )

        load_dotenv()
