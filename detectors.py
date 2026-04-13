def detect_low_voltage(voltage_history):
    recent = list(voltage_history)[-5:]
    return all(v < 26.0 for v in recent)

def detect_high_voltage(voltage_history):
    recent = list(voltage_history)[-5:]
    return all(v > 30.0 for v in recent)

def detect_overtemperature(temperature_history):
    recent = list(temperature_history)[-5:]
    return all(t > 40.0 for t in recent)

def detect_undertemperature(temperature_history):
    recent = list(temperature_history)[-5:]
    return all(t < 10.0 for t in recent)

def detect_communication_loss(signal_history):
    recent = list(signal_history)[-5:]
    return all(s < 20.0 for s in recent)