def detect_low_voltage(voltage_history):
    recent = voltage_history[-5:]
    return all(v < 26.0 for v in recent)