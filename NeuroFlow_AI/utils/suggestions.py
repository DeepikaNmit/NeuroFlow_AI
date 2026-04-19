import streamlit as st


def get_suggestions(traffic):
    if traffic > 4000:
        return [
            "🚨 Heavy traffic expected",
            "Leave 30 mins earlier",
            "Use public transport",
            "Try carpool"
        ]
    elif traffic > 2000:
        return [
            "⚠ Moderate traffic",
            "Leave 10-15 mins early",
            "Check alternate routes"
        ]
    else:
        return ["✅ Traffic is smooth"]