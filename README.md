# GNews MCP Server

A Model Context Protocol (MCP) server that provides Google News search capabilities. This server enables AI assistants and other MCP clients to search and retrieve news articles from Google News.

## Features

- 🔍 **Keyword Search** - Search news articles by keyword
- 📰 **Top News** - Get top headlines
- 📂 **Topic-based News** - Browse news by category (Technology, Sports, Business, etc.)
- 🌍 **Location-based News** - Get news from specific geographic locations
- 🌐 **Site-specific News** - Retrieve news from specific websites
- 🗣️ **Multi-language Support** - Support for 30+ languages
- 🌎 **Multi-country Support** - Support for 40+ countries

## Tools Reference

### 1. `search_news`

Search for news articles by keyword.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keyword` | string | *required* | Search keyword for news |
| `language` | string | `"en"` | Language code (e.g., `en`, `es`, `fr`) |
| `country` | string | `"US"` | Country code (e.g., `US`, `GB`, `IN`) |
| `period` | string | `"7d"` | Time period (e.g., `7d`, `12h`, `1m`, `1y`) |
| `max_results` | integer | `10` | Maximum number of results (1-100) |
| `exclude_websites` | string | `""` | Comma-separated list of websites to exclude |

**Example:**
```json
{
  "keyword": "artificial intelligence",
  "language": "en",
  "country": "US",
  "period": "7d",
  "max_results": 10
}
```

### 2. `get_top_news`

Get top news headlines.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | string | `"en"` | Language code |
| `country` | string | `"US"` | Country code |
| `max_results` | integer | `10` | Maximum number of results (1-100) |

**Example:**
```json
{
  "language": "en",
  "country": "GB",
  "max_results": 5
}
```

### 3. `get_news_by_topic`

Get news by topic category.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | string | *required* | Topic name |
| `language` | string | `"en"` | Language code |
| `country` | string | `"US"` | Country code |
| `max_results` | integer | `10` | Maximum number of results (1-100) |

**Supported Topics:**
- `WORLD`
- `NATION`
- `BUSINESS`
- `TECHNOLOGY`
- `ENTERTAINMENT`
- `SPORTS`
- `SCIENCE`
- `HEALTH`
- `POLITICS`
- `CELEBRITIES`

**Example:**
```json
{
  "topic": "TECHNOLOGY",
  "language": "en",
  "country": "US",
  "max_results": 10
}
```

### 4. `get_news_by_location`

Get news by geographic location.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `location` | string | *required* | Location name (city, state, or country) |
| `language` | string | `"en"` | Language code |
| `max_results` | integer | `10` | Maximum number of results (1-100) |

**Example:**
```json
{
  "location": "London",
  "language": "en",
  "max_results": 10
}
```

### 5. `get_news_by_site`

Get news from a specific website.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `site` | string | *required* | Website domain |
| `language` | string | `"en"` | Language code |
| `country` | string | `"US"` | Country code |
| `max_results` | integer | `10` | Maximum number of results (1-100) |

**Example:**
```json
{
  "site": "techcrunch.com",
  "language": "en",
  "country": "US",
  "max_results": 5
}
```

### 6. `get_available_countries`

Get list of all supported countries with their codes.

**Parameters:** None

**Returns:** JSON object with country names and codes.

### 7. `get_available_languages`

Get list of all supported languages with their codes.

**Parameters:** None

**Returns:** JSON object with language names and codes.

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/google_news_MCP.git
   cd google_news_MCP
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   python gnews_mcp_server.py
   ```

   The server will start on `http://localhost:8000` by default.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port number for the server |
| `HOST` | `0.0.0.0` | Host address to bind to |

## Deploying to Heroku

### Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- A Heroku account

### Deployment Steps

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set the Python runtime (optional):**
   The `.python-version` file specifies Python 3.11. Heroku will automatically use this version.

4. **Deploy the application:**
   ```bash
   git push heroku main
   ```

5. **Verify the deployment:**
   ```bash
   heroku open
   ```

   Your server should be running at `https://your-app-name.herokuapp.com`

### Heroku Configuration

The repository includes the necessary files for Heroku deployment:

- **`Procfile`** - Tells Heroku how to run the application
- **`requirements.txt`** - Python dependencies
- **`.python-version`** - Specifies Python 3.11

### Scaling

To scale your Heroku dyno:
```bash
heroku ps:scale web=1
```

### Viewing Logs

To view application logs:
```bash
heroku logs --tail
```

## Connecting to the MCP Server

### Server Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Root endpoint - returns server info and available tools |
| `/mcp` | MCP protocol endpoint for client connections |

### MCP Client Configuration

To connect an MCP client to this server, configure it with the server URL:

**Local:**
```
http://localhost:8000/mcp
```

**Heroku:**
```
https://your-app-name.herokuapp.com/mcp
```

### Example Client Configuration (Claude Desktop)

Add the following to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "gnews": {
      "url": "https://your-app-name.herokuapp.com/mcp"
    }
  }
}
```

## API Response Format

All tools return JSON responses with the following structure:

### Success Response
```json
{
  "status": "success",
  "results": [
    {
      "title": "Article Title",
      "description": "Article description...",
      "published date": "2024-01-15 10:30:00",
      "url": "https://example.com/article",
      "publisher": {
        "href": "https://example.com",
        "title": "Example News"
      }
    }
  ]
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Resources

The server also exposes a resource endpoint for configuration information:

- **`gnews://config`** - Returns server configuration and capabilities

## Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| `mcp` | ≥1.0.0 | Model Context Protocol SDK |
| `gnews` | 0.4.2 | Google News API wrapper |
| `newspaper3k` | 0.2.8 | Article extraction library |
| `uvicorn` | ≥0.30.0 | ASGI server |
| `starlette` | ≥0.37.0 | ASGI framework |

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
