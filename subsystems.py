class PowerSubsystem:
    def __init__(self):
        self.battery = 100
        self.voltage = 28.0
        self.fault_active = False

    def update(self):
        if self.fault_active:
            self.battery -= 2
            self.voltage -= 0.2
        else:
            self.battery -= 0.2
            self.voltage -= 0.01
