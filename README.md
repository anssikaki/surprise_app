# Press Release from the Future

This Streamlit application generates creative press releases set in the future for any company. It uses the OpenAI API for text generation and stores detailed logs of interactions.

## Features

- Input company name, future year, and optional details.
- Generates a futuristic press release with OpenAI's chat model.
- Logs events and generated content to `app.log` for troubleshooting.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Provide your OpenAI API key using one of the following methods:

- Create a `.streamlit/secrets.toml` file with:

```toml
[openai]
api_key = "YOUR_API_KEY"
```

- Or set the environment variable `OPENAI_API_KEY`.

## Running the App

Run the Streamlit app from the repository root:

```bash
streamlit run surprise_app.py
```

The application logs details to `app.log` in the project directory.
