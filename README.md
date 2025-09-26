# Helios Prime AI Prompter

Automated AI prompt generation system based on trend analysis through ComfyUI

## Project Description

Helios Prime AI Prompter is an intelligent system for automatic generation of high-quality prompts for AI image generators. The system uses Google Trends analysis to create relevant and popular topics.

## Main Components

### Custom ComfyUI Nodes:

- **HeliosFreeCrawler** - data collection from free APIs (Pexels, Pixabay)
- **HeliosTrendAnalyzer** - trend analysis via Google Trends API
- **HeliosPromptGenerator** - prompt generation based on trends
- **HeliosQualityChecker** - prompt quality verification
- **HeliosFileWriter** - automatic results recording with timestamps
- **HeliosKnowledgeBase** - knowledge base management

## Installation and Launch

### Prerequisites:
- Docker
- Python 3.11+
- Git

### Quick Start:

1. **Clone the repository:**
```bash
git clone https://github.com/3dleonardo/Helios-Prime-AI-Prompter.git
cd Helios-Prime-AI-Prompter
```

2. **Launch ComfyUI:**
```bash
# Build and run the container
docker build -t helios-comfyui ComfyUI/
docker run -d -p 8188:8188 -v $(pwd)/custom_nodes:/ComfyUI/custom_nodes -v $(pwd)/prompts:/ComfyUI/prompts --name helios-comfyui helios-comfyui
```

3. **Open ComfyUI:**
Navigate to http://localhost:8188

4. **Load workflow:**
Load `helios_free_workflow.json` and run it

## Architecture

```
Data Crawling → Trend Analysis → Prompt Generation → Quality Check → File Output
     ↓              ↓              ↓              ↓              ↓
HeliosFreeCrawler → HeliosTrendAnalyzer → HeliosPromptGenerator → HeliosQualityChecker → HeliosFileWriter
```

## Features

- ✅ **Free APIs** - uses Pexels and Pixabay instead of paid services
- ✅ **Real trend analysis** - integrates with Google Trends for current topics
- ✅ **Automatic saving** - timestamped files for history tracking
- ✅ **Modular architecture** - easily extensible with new nodes
- ✅ **Docker support** - simple deployment

## Configuration

### API Keys (optional):
- Gemini API key for enhanced prompt generation
- Pinecone API key for vector knowledge base

### Workflow Files:
- `helios_free_workflow.json` - main workflow with free APIs
- `helios_workflow.json` - extended workflow
- `simple_workflow.json` - simple test workflow

## Project Structure

```
Helios-Prime-AI-Prompter/
├── custom_nodes/           # Custom ComfyUI nodes
│   ├── HeliosFreeCrawler/
│   ├── HeliosTrendAnalyzer/
│   ├── HeliosPromptGenerator/
│   ├── HeliosQualityChecker/
│   ├── HeliosFileWriter/
│   └── HeliosKnowledgeBase/
├── ComfyUI/               # ComfyUI Docker image
├── prompts/               # Generated prompts
├── *.json                 # Workflow files
└── README.md             # This file
```

## Development

To add new nodes:
1. Create a folder in `custom_nodes/`
2. Implement the node class in `nodes.py`
3. Add `__init__.py` for import
4. Restart the ComfyUI container

## License

MIT License - see LICENSE file

## Author

[3dleonardo](https://github.com/3dleonardo)