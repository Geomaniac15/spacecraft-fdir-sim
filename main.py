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


def inject_faults(tick, subsystems):
    if tick >= FAULT_INJECTION_TICK:
        if random.random() < 0.3:  # 30% chance power fails
            subsystems['power'].fault_active = True

        if random.random() < 0.2:  # 20% chance thermal fails
            subsystems['thermal'].fault_active = True
            if random.random() < 0.5:
                subsystems['thermal'].heater_on = True
            else:
                subsystems['thermal'].cooler_on = True

        if random.random() < 0.1:  # 10% chance comms fails
            subsystems['comms'].fault_active = True


def run_simulation(subsystems, histories, placeholder):
    for tick in range(TOTAL_TICKS):
        inject_faults(tick, subsystems)

        alerts = {}

        for name, subsystem in subsystems.items():
            subsystem.update()
            value = subsystem.current_value()
            histories[name].append(value)

            alerts[name] = []

            if name == 'power':
                if detect_low_voltage(histories[name]):
                    alerts[name].append('LOW_VOLTAGE')
                if detect_high_voltage(histories[name]):
                    alerts[name].append('HIGH_VOLTAGE')
            
            elif name == 'thermal':
                if detect_overtemperature(histories[name]):
                    alerts[name].append('OVER_TEMP')
                if detect_undertemperature(histories[name]):
                    alerts[name].append('UNDER_TEMP')
            
            elif name == 'comms':
                if detect_communication_loss(histories[name]):
                    alerts[name].append('COMMS_LOSS')

        with placeholder.container():
            dashboard.display(subsystems, histories)

        time.sleep(TICK_SECONDS)


def main():
    subsystems = {
        'power': PowerSubsystem(),
        'thermal': ThermalSubsystem(),
        'comms': CommunicationSubsystem()
    }
    histories = {name: deque(maxlen=HISTORY_LENGTH) for name in subsystems}
    placeholder = st.empty()

    run_simulation(subsystems, histories, placeholder)


if __name__ == '__main__':
    main()