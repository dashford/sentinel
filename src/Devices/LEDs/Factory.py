from src.Devices.LEDs.RGB import RGB


class Factory:

    @staticmethod
    def create_led(device, configuration, notification_manager):
        if device == 'rgb':
            return RGB(configuration=configuration, notification_manager=notification_manager)
