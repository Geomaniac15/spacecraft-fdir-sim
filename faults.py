# subsystems = [
#     PowerSubsystem(),
#     ThermalSubsystem(),
#     CommunicationSubsystem()
# ]

faults = {
    'power': [
        'Battery Drain',
        'Overvoltage',
        'Bus Short'
    ],
    'thermal': [
        'Overtemperature',
        'Undertemperature',
        'Heater Stuck On'
    ],
    'comms': [
        'Heartbeat Loss',
        'Signal Drop'
    ]
}