from enum import Enum


class DeleteCompletedJobResponse200JobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWDEPENDENCIES = "flowdependencies"
    APPDEPENDENCIES = "appdependencies"
    FLOWPREVIEW = "flowpreview"
    SCRIPT_HUB = "script_hub"
    IDENTITY = "identity"

    def __str__(self) -> str:
        return str(self.value)
