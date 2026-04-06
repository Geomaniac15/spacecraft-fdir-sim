from collections import deque
from time import sleep

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
    alerts_triggered = {name: False for name in subsystems}

    print('Starting spacecraft FDIR power sim\n')

    for tick in range(TOTAL_TICKS):
        if tick == FAULT_INJECTION_TICK:
            subsystems['power'].fault_active = True
            print(f'[T+{tick:02d}s] Injected fault: rapid battery drain')

        for name, subsystem in subsystems.items():
            subsystem.update()
            if name == 'power':
                histories[name].append(subsystem.voltage)
                print(
                    f'[T+{tick:02d}s] '
                    f'battery={subsystem.battery:6.2f}%  '
                    f'voltage={subsystem.voltage:5.2f}V  '
                    f'fault_active={subsystem.fault_active}'
                )
                if len(histories[name]) >= 5 and detect_low_voltage(list(histories[name])):
                    if not alerts_triggered[name]:
                        print(
                            f'[T+{tick:02d}s] ALERT: POWER_LOW_BUS - '
                            'voltage below 26.0V for 5 consecutive samples'
                        )
                        alerts_triggered[name] = True
            if name == 'thermal':
                histories[name].append(subsystem.temperature)
                print(
                    f'[T+{tick:02d}s] '
                    f'temperature={subsystem.temperature:5.2f}C  '
                    f'heater_on={subsystem.heater_on}  '
                    f'cooler_on={subsystem.cooler_on}  '
                    f'fault_active={subsystem.fault_active}'
                )
                if len(histories[name]) >= 5 and detect_overtemperature(list(histories[name])):
                    if not alerts_triggered[name]:
                        print(
                            f'[T+{tick:02d}s] ALERT: THERMAL_OVER - '
                            'temperature above 40.0C for 5 consecutive samples'
                        )
                        alerts_triggered[name] = True
                elif len(histories[name]) >= 5 and detect_undertemperature(list(histories[name])):
                    if not alerts_triggered[name]:
                        print(
                            f'[T+{tick:02d}s] ALERT: THERMAL_UNDER - '
                            'temperature below 10.0C for 5 consecutive samples'
                        )
                        alerts_triggered[name] = True
            if name == 'comms':
                histories[name].append(subsystem.signal_strength)
                print(
                    f'[T+{tick:02d}s] '
                    f'signal_strength={subsystem.signal_strength:5.2f}%  '
                    f'heartbeat={"OK" if subsystem.heartbeat else "LOST"}  '
                    f'missed_ticks={subsystem.missed_ticks}  '
                    f'fault_active={subsystem.fault_active}'
                )
                if len(histories[name]) >= 5 and detect_communication_loss(list(histories[name])):
                    if not alerts_triggered[name]:
                        print(
                            f'[T+{tick:02d}s] ALERT: COMMS_LOSS - '
                            'signal strength below 20.0% for 5 consecutive samples'
                        )
                        alerts_triggered[name] = True

        sleep(TICK_SECONDS)

    print('\nSimulation complete.')


if __name__ == '__main__':
    main()