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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)


def build_prompt(product: str, feedback: str) -> str:
    """Create a short action plan prompt."""
    logger.debug("Building prompt for product=%s with feedback=%s", product, feedback)
    prompt = (
        f"Generate a fun action plan for improving {product} "
        f"based on user feedback: {feedback}"
    )
    logger.debug("Generated prompt: %s", prompt)
    return prompt


def read_log_file(path: str, max_lines: int | None = None) -> str:
    """Read the last ``max_lines`` from ``path``.

    Returns a helpful message if the file does not exist.
    """
    logger.debug("Reading log file at %s", path)
    if not os.path.exists(path):
        logger.debug("Log file %s does not exist", path)
        return "Log file does not exist."
    with open(path, "r") as f:
        lines = f.readlines()
        logger.debug("Read %d lines from log file", len(lines))
    if max_lines is not None:
        lines = lines[-max_lines:]
        logger.debug("Truncated log to last %d lines", max_lines)
    result = "".join(lines)
    logger.debug("Returning %d characters from log file", len(result))
    return result


# Minimal Streamlit demo so that the module can be executed directly
if __name__ == "__main__":
    logger.debug("Executing module as __main__")
    if st is not None:
        st.write("test app")
    else:
        logger.debug("Streamlit not available")
        print("Streamlit not available")
