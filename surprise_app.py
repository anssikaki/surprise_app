import os
import logging

try:
    import streamlit as st
except ModuleNotFoundError:
    st = None

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None

logging.basicConfig(level=logging.INFO)


def build_prompt(product: str, feedback: str) -> str:
    """Create a short action plan prompt."""
    return (
        f"Generate a fun action plan for improving {product} "
        f"based on user feedback: {feedback}"
    )


def read_log_file(path: str, max_lines: int | None = None) -> str:
    """Read the last ``max_lines`` from ``path``.

    Returns a helpful message if the file does not exist.
    """
    if not os.path.exists(path):
        return "Log file does not exist."
    with open(path, "r") as f:
        lines = f.readlines()
    if max_lines is not None:
        lines = lines[-max_lines:]
    return "".join(lines)


# Minimal Streamlit demo so that the module can be executed directly
if __name__ == "__main__":
    if st is not None:
        st.write("test app")
    else:
        print("Streamlit not available")
