from enum import Enum


class QueuedJobJobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOWDEPENDENCIES = "flowdependencies"
    APPDEPENDENCIES = "appdependencies"
    FLOW = "flow"
    FLOWPREVIEW = "flowpreview"
    SCRIPT_HUB = "script_hub"
    IDENTITY = "identity"

    def __str__(self) -> str:
        return str(self.value)
