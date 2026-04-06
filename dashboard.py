import streamlit as st
import time

def display(subsystems, histories):
    st.title('Spacecraft FDIR Dashboard')

    for name, subsystem in subsystems.items():
        st.subheader(name.capitalize())
        if name == 'power':
            st.metric('Battery (%)', f'{subsystem.battery:.2f}')
            st.metric('Voltage (V)', f'{subsystem.voltage:.2f}')
            st.line_chart(list(histories[name]))
        elif name == 'thermal':
            st.metric('Temperature (C)', f'{subsystem.temperature:.2f}')
            st.text(f'Heater: {subsystem.heater_on}  Cooler: {subsystem.cooler_on}')
            st.line_chart(list(histories[name]))
        elif name == 'comms':
            st.metric('Signal (%)', f'{subsystem.signal_strength:.2f}')
            st.text(f'Heartbeat: {'OK' if subsystem.heartbeat else 'LOST'}  Missed ticks: {subsystem.missed_ticks}')
            st.line_chart(list(histories[name]))

        st.text(f'Fault active: {subsystem.fault_active}')
    st.markdown('---')