from collections import deque
import random
import time
import streamlit as st
import dashboard

from detectors import detect_low_voltage, detect_high_voltage, detect_overtemperature, detect_undertemperature, detect_communication_loss
from subsystems import PowerSubsystem, ThermalSubsystem, CommunicationSubsystem


HISTORY_LENGTH = 10
TICK_SECONDS = 0.2
TOTAL_TICKS = 30
FAULT_INJECTION_TICK = 10


def main():
    subsystems = {
        'power': PowerSubsystem(),
        'thermal': ThermalSubsystem(),
        'comms': CommunicationSubsystem()
    }
    histories = {name: deque(maxlen=HISTORY_LENGTH) for name in subsystems}

    placeholder = st.empty()

    for tick in range(TOTAL_TICKS):
        if tick == FAULT_INJECTION_TICK:
            subsystems['power'].fault_active = True

            subsystems['thermal'].fault_active = True
            if random.random() < 0.5:
                subsystems['thermal'].heater_on = True
            else:
                subsystems['thermal'].cooler_on = True

            subsystems['comms'].fault_active = True

        for name, subsystem in subsystems.items():
            subsystem.update()
            if name == 'power':
                histories[name].append(subsystem.voltage)
            if name == 'thermal':
                histories[name].append(subsystem.temperature)
            if name == 'comms':
                histories[name].append(subsystem.signal_strength)

        with placeholder.container():
            dashboard.display(subsystems, histories)

        time.sleep(TICK_SECONDS)

if __name__ == '__main__':
    main()