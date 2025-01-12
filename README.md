# AI Essay Writer

An AI-powered essay writing assistant built with FastAPI and Gradio.

## Features
- AI-powered essay generation
- Research integration with Tavily
- Interactive UI for essay writing process
- State management and revision tracking

## Setup Instructions

### Prerequisites
- Python 3.8+
- Windows 10/11

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd essay-writer
```

2. Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
MODEL_NAME=gpt-3.5-turbo
MAX_REVISIONS=2
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

#### Starting the FastAPI Server
```bash
python -m app.main
```
This will start the FastAPI server at `http://localhost:8000`

#### Starting the Gradio UI (in a separate terminal)
```bash
python -m app.ui.gradio_ui
```
This will start the Gradio UI at `http://localhost:5000`

### API Documentation
Once the server is running, you can access:
- API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

### Testing
You can test the essay generation through either:
1. The Gradio UI at `http://localhost:5000`
2. Direct API calls to `http://localhost:8000/api/essay`

## Project Structure
```
app/
├── api/           # API endpoints and routes
├── core/          # Core business logic
├── models/        # Data models and schemas
├── services/      # External service integrations
├── state/         # State management
└── ui/            # Gradio UI components