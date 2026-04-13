class Subsystem:
    def __init__(self, name: str):
        self.name = name
        self.fault_active = False
    
    def update(self):
        '''Update the subsystem state. To be implemented by subclasses.'''
        raise NotImplementedError('update() must be implemented by subclasses')
    
    def inject_fault(self):
        '''Activate the fault condition for this subsystem.'''
        self.fault_active = True
    
    def clear_fault(self):
        '''Deactivate the fault condition for this subsystem.'''
        self.fault_active = False

class PowerSubsystem(Subsystem):
    def __init__(self):
        super().__init__('Power')
        self.battery = 100
        self.voltage = 28.0

    def update(self):
        self.voltage = max(0.0, self.voltage)
        if self.fault_active:
            self.battery -= 2
            self.voltage -= 0.2
        else:
            self.battery -= 0.2
            self.voltage -= 0.01
    
    def current_value(self):
        return self.voltage

class ThermalSubsystem(Subsystem):
    def __init__(self):
        super().__init__('Thermal')
        self.temperature = 25.0
        self.heater_on = False
        self.cooler_on = False
    
    def update(self):
        self.temperature = max(-10.0, min(self.temperature, 100.0))
        if self.fault_active and self.heater_on:
            self.temperature += 2.0
        elif self.heater_on:
            self.temperature += 0.5
        elif self.fault_active and self.cooler_on:
            self.temperature -= 2.0
        elif self.cooler_on:
            self.temperature -= 0.5
    
    def current_value(self):
        return self.temperature

class CommunicationSubsystem(Subsystem):
    def __init__(self):
        super().__init__('Communications')
        self.heartbeat = True
        self.signal_strength = 100.0
        self.missed_ticks = 0
    
    def update(self):
        self.signal_strength = max(0.0, min(self.signal_strength, 100.0))
        if self.fault_active:
            self.heartbeat = False
            self.signal_strength -= 10.0
            self.missed_ticks += 1
        else:
            self.heartbeat = True
            self.signal_strength = max(0.0, self.signal_strength - 1.0)
    
    def current_value(self):
        return self.signal_strength
        