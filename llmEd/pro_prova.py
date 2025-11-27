import streamlit as st
import time

if 'disabledUDA' not in st.session_state:
    st.session_state.disabledUDA = False

def callback():
    st.session_state.disabledUDA = True

button1 = st.button('Button 1', disabled=st.session_state.disabledUDA, on_click=callback)
if button1:
    time.sleep(5) #simulated slow process
    st.session_state.disabledUDA = False
    st.rerun()
button2 = st.button('Button 2',  disabled=st.session_state.disabledUDA, on_click=callback)
if button2:
            time.sleep(5)  # simulated slow process
            st.session_state.success_message = True
            st.session_state.disabledUDA = False

if 'success_message' in st.session_state and st.session_state.success_message:
    st.success("Success")