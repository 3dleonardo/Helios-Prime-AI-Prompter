# Helios Prime AI Prompter

Automated AI prompt generation system based on comprehensive trend analysis through ComfyUI

## Project Description

Helios Prime AI Prompter is an intelligent system for automatic generation of high-quality prompts for AI image generators. The system uses multiple data sources including Google Trends, Pinterest social trends, and web scraping to create relevant and popular topics.

## Main Components

### Custom ComfyUI Nodes:

- **HeliosFreeCrawler** - Multi-source data collection (Google Trends, Pinterest, Web Scraping)
- **HeliosTrendAnalyzer** - Advanced trend analysis with scoring algorithms
- **HeliosPromptGenerator** - AI-powered prompt generation based on trends
- **HeliosQualityChecker** - Prompt quality verification and filtering
- **HeliosFileWriter** - Automatic results recording with timestamps
- **HeliosKnowledgeBase** - Knowledge base management and learning

## Data Sources

### 🔍 **Google Trends API**
- Search volume analysis
- Related queries and topics
- Geographic trend variations
- Real-time trending searches

### 📌 **Pinterest APIs**
- Social media trend analysis
- Visual content trends
- Community engagement metrics
- Aesthetic and design trends

### 🌐 **Web Scraping**
- Reddit community discussions
- Twitter/X trending topics
- Additional analytics sources
- Real-time social sentiment

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
docker run -d -p 8189:8189 -v $(pwd)/custom_nodes:/ComfyUI/custom_nodes -v $(pwd)/prompts:/ComfyUI/prompts --name helios-comfyui helios-comfyui
```

3. **Open ComfyUI:**
Navigate to http://localhost:8189

4. **Load workflow:**
Load `helios_free_workflow.json` and run it

## Architecture

```
Multi-Source Data Collection → Advanced Trend Analysis → AI Prompt Generation → Quality Control → Automated Output
         ↓                              ↓                          ↓                    ↓                    ↓
Google Trends API + Pinterest APIs + Web Scraping → Scoring Algorithms → Gemini/Ollama → Filtering → Timestamped Files
```

## Features

- ✅ **Multi-Source Trend Analysis** - Combines search, social, and web data
- ✅ **Real-time Data Collection** - Fresh trend data from multiple platforms
- ✅ **Advanced Scoring Algorithms** - Growth rates, engagement metrics, popularity scores
- ✅ **AI-Powered Generation** - Gemini and Ollama integration for creative prompts
- ✅ **Automated Quality Control** - Built-in filtering and validation
- ✅ **Docker Support** - Easy deployment and scaling

## Configuration

### Data Source Selection:
- `google_trends` - Google search trends only
- `pinterest` - Pinterest social trends only
- `web_scraping` - Web scraping analytics only
- `all` - All sources combined (recommended)

### Geographic Settings:
- Google Trends supports country-specific analysis (US, UK, DE, etc.)
- Pinterest trends are global with regional variations

### API Keys (optional):
- Gemini API key for enhanced prompt generation
- Pinterest API key for deeper social analytics
- Pinecone API key for vector knowledge base

### Workflow Files:
- `helios_free_workflow.json` - Main workflow with all data sources
- `helios_workflow.json` - Extended workflow with additional features
- `simple_workflow.json` - Basic test workflow

## Project Structure

```
Helios-Prime-AI-Prompter/
├── custom_nodes/           # Custom ComfyUI nodes
│   ├── HeliosFreeCrawler/      # Multi-source data collection
│   ├── HeliosTrendAnalyzer/    # Advanced trend analysis
│   ├── HeliosPromptGenerator/  # AI prompt generation
│   ├── HeliosQualityChecker/   # Quality control
│   ├── HeliosFileWriter/       # Automated file output
│   └── HeliosKnowledgeBase/    # Knowledge management
├── ComfyUI/               # ComfyUI Docker image
├── prompts/               # Generated prompts with timestamps
├── *.json                 # Workflow files
└── README.md             # This documentation
```

## Trend Analysis Algorithm

The system uses a sophisticated scoring algorithm that combines:

1. **Search Volume** - Google Trends search interest
2. **Growth Rate** - Recent vs historical trends
3. **Social Engagement** - Pinterest saves, likes, shares
4. **Community Sentiment** - Reddit and Twitter discussions
5. **Content Freshness** - Recent activity indicators

## Development

To add new nodes:
1. Create a folder in `custom_nodes/`
2. Implement the node class in `nodes.py`
3. Add `__init__.py` for import
4. Restart the ComfyUI container

To add new data sources:
1. Extend `HeliosFreeCrawler` with new collection methods
2. Update the trend analysis algorithms
3. Test with the workflow system

## Dependencies

- **Core**: requests, pytrends, beautifulsoup4
- **AI**: google-generativeai, sentence-transformers
- **Social**: pinterest-api, tweepy, instabot
- **Web**: selenium, webdriver-manager, scrapy
- **Storage**: pinecone-client, GitPython

## License

MIT License - see LICENSE file

## Author

[3dleonardo](https://github.com/3dleonardo)