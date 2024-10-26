from sconf.src.configuration.models.SwebConfiguration import SwebConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class SwebViewModel:
    _swebConfiguration: SwebConfiguration

    def __init__(self, swebConfiguration: SwebConfiguration):
        super().__init__()
        self._swebConfiguration = swebConfiguration

    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        setattr(self._swebConfiguration, attribute_name, value)
        print(f"Update complete new value is {getattr(self._swebConfiguration, attribute_name, value)}")
