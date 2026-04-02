from collections import deque
from time import sleep

from detectors import detect_low_voltage
from subsystems import PowerSubsystem


HISTORY_LENGTH = 10
TICK_SECONDS = 0.2
TOTAL_TICKS = 30
FAULT_INJECTION_TICK = 10


def main():
    power = PowerSubsystem()
    voltage_history: deque[float] = deque(maxlen=HISTORY_LENGTH)
    alerts_triggered = False

    print('Starting spacecraft FDIR power sim\n')

    for tick in range(TOTAL_TICKS):
        if tick == FAULT_INJECTION_TICK:
            power.fault_active = True
            print(f'[T+{tick:02d}s] Injected fault: rapid battery drain')

        power.update()
        voltage_history.append(power.voltage)

        print(
            f'[T+{tick:02d}s] '
            f'battery={power.battery:6.2f}%  '
            f'voltage={power.voltage:5.2f}V  '
            f'fault_active={power.fault_active}'
        )

        if len(voltage_history) >= 5 and detect_low_voltage(list(voltage_history)):
            if not alerts_triggered:
                print(
                    f'[T+{tick:02d}s] ALERT: POWER_LOW_BUS - '
                    'voltage below 26.0V for 5 consecutive samples'
                )
                alerts_triggered = True

        sleep(TICK_SECONDS)

    print('\nSimulation complete.')


if __name__ == '__main__':
    main()