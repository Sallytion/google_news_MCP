"""GNews MCP Server - Provides Google News search capabilities via Model Context Protocol"""

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession
from gnews import GNews
from typing import Optional, List
import json
import contextlib
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

# Initialize FastMCP server
mcp = FastMCP(
    "GNews Server",
    instructions="A server that provides Google News search capabilities including keyword search, top news, news by topic, location, and site.",
)


@mcp.tool()
def search_news(
    keyword: str,
    language: str = "en",
    country: str = "US",
    period: str = "7d",
    max_results: int = 10,
    exclude_websites: Optional[str] = None,
) -> str:
    """
    Search for news articles by keyword.
    
    Args:
        keyword: Search keyword for news
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        period: Time period (e.g., '7d', '12h', '1m', '1y')
        max_results: Maximum number of results (1-100)
        exclude_websites: Comma-separated list of websites to exclude (e.g., 'yahoo.com,cnn.com')
    
    Returns:
        JSON string containing news articles
    """
    try:
        exclude_list = exclude_websites.split(",") if exclude_websites else []
        
        google_news = GNews(
            language=language,
            country=country,
            period=period,
            max_results=max_results,
            exclude_websites=exclude_list,
        )
        
        news = google_news.get_news(keyword)
        return json.dumps({"status": "success", "keyword": keyword, "results": news}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_top_news(
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get top news headlines.
    
    Args:
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing top news articles
    """
    try:
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_top_news()
        return json.dumps({"status": "success", "type": "top_news", "results": news}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_topic(
    topic: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get news by topic.
    
    Args:
        topic: Topic name (e.g., 'WORLD', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH', 'POLITICS')
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles for the topic
    """
    try:
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_topic(topic.upper())
        return json.dumps({"status": "success", "topic": topic, "results": news}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_location(
    location: str,
    language: str = "en",
    max_results: int = 10,
) -> str:
    """
    Get news by geographic location (city/state/country).
    
    Args:
        location: Location name (e.g., 'London', 'California', 'Pakistan')
        language: Language code (e.g., 'en', 'es', 'fr')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles for the location
    """
    try:
        google_news = GNews(
            language=language,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_location(location)
        return json.dumps({"status": "success", "location": location, "results": news}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_site(
    site: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get news from a specific website.
    
    Args:
        site: Website domain (e.g., 'bbc.com', 'cnn.com', 'techcrunch.com')
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles from the site
    """
    try:
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_site(site)
        return json.dumps({"status": "success", "site": site, "results": news}, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_available_countries() -> str:
    """
    Get list of all supported countries.
    
    Returns:
        JSON string containing country names and codes
    """
    try:
        google_news = GNews()
        return json.dumps({
            "status": "success",
            "countries": google_news.AVAILABLE_COUNTRIES
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_available_languages() -> str:
    """
    Get list of all supported languages.
    
    Returns:
        JSON string containing language names and codes
    """
    try:
        google_news = GNews()
        return json.dumps({
            "status": "success",
            "languages": google_news.AVAILABLE_LANGUAGES
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


# Resource to expose configuration info
@mcp.resource("gnews://config")
def get_config() -> str:
    """Get GNews MCP server configuration information."""
    return json.dumps({
        "server": "GNews MCP Server",
        "version": "1.0.0",
        "capabilities": [
            "search_news",
            "get_top_news",
            "get_news_by_topic",
            "get_news_by_location",
            "get_news_by_site",
            "get_available_countries",
            "get_available_languages"
        ],
        "supported_topics": [
            "WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT",
            "SPORTS", "SCIENCE", "HEALTH", "POLITICS", "CELEBRITIES"
        ]
    }, indent=2)


async def root_handler(request):
    """Root endpoint to show server info"""
    return JSONResponse({
        "name": "GNews MCP Server",
        "version": "1.0.0",
        "status": "running",
        "mcp_endpoint": "/mcp",
        "description": "Model Context Protocol server for Google News",
        "tools": [
            "search_news",
            "get_top_news", 
            "get_news_by_topic",
            "get_news_by_location",
            "get_news_by_site",
            "get_available_countries",
            "get_available_languages"
        ]
    })

# Configure MCP to handle root path
mcp.settings.streamable_http_path = "/"

# Create lifespan context to manage MCP session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

# Create Starlette app with root route and MCP mounted
app = Starlette(
    routes=[
        Route("/", root_handler),
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan
)

# Main entry point
if __name__ == "__main__":
    import os
    import uvicorn
    
    # Get port from environment variable (Heroku sets PORT)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Run with uvicorn - use string import for production
    uvicorn.run("gnews_mcp_server:app", host=host, port=port, log_level="info")
