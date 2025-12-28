"""GNews MCP Server - Provides Google News search capabilities via Model Context Protocol"""

from mcp.server.fastmcp import FastMCP
from gnews import GNews
from typing import Optional
import json
import contextlib
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from mcp.server. sse import SseServerTransport
from starlette.requests import Request
from starlette. responses import Response
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server without transport_security for simpler deployment
mcp = FastMCP(
    "GNews Server",
    instructions="A server that provides Google News search capabilities including keyword search, top news, news by topic, location, and site.",
)


@mcp.tool()
def search_news(
    keyword:  str,
    language: str = "en",
    country: str = "US",
    period:  str = "7d",
    max_results: int = 10,
    exclude_websites: str = "",
) -> str:
    """
    Search for news articles by keyword.
    
    Args:
        keyword: Search keyword for news
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        period: Time period (e. g., '7d', '12h', '1m', '1y')
        max_results:  Maximum number of results (1-100)
        exclude_websites:  Comma-separated list of websites to exclude (e.g., 'yahoo.com,cnn.com')
    
    Returns:
        JSON string containing news articles
    """
    try:
        logger.info(f"{datetime.now()} - Searching news for keyword: {keyword}")
        exclude_list = [x.strip() for x in exclude_websites.split(",") if x.strip()] if exclude_websites else []
        
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
        logger.error(f"Error searching news: {str(e)}")
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
        logger.info(f"{datetime.now()} - Getting top news")
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_top_news()
        return json.dumps({"status": "success", "type": "top_news", "results": news}, indent=2)
    except Exception as e:
        logger.error(f"Error getting top news: {str(e)}")
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_topic(
    topic: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get news by topic category.
    
    Args:
        topic: News topic (WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH, POLITICS, CELEBRITIES)
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles for the topic
    """
    try:
        logger.info(f"{datetime.now()} - Getting news by topic: {topic}")
        valid_topics = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", 
                       "SPORTS", "SCIENCE", "HEALTH", "POLITICS", "CELEBRITIES"]
        
        topic_upper = topic.upper()
        if topic_upper not in valid_topics:
            return json.dumps({
                "status": "error", 
                "message": f"Invalid topic.  Valid topics are: {', '.join(valid_topics)}"
            }, indent=2)
        
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_topic(topic_upper)
        return json.dumps({"status": "success", "topic": topic_upper, "results": news}, indent=2)
    except Exception as e:
        logger.error(f"Error getting news by topic:  {str(e)}")
        return json.dumps({"status":  "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_location(
    location: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get news by location/city/region.
    
    Args:
        location: Location name (city, state, or region)
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results:  Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles for the location
    """
    try: 
        logger.info(f"{datetime.now()} - Getting news by location: {location}")
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_location(location)
        return json.dumps({"status": "success", "location": location, "results": news}, indent=2)
    except Exception as e:
        logger.error(f"Error getting news by location: {str(e)}")
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_site(
    site:  str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """
    Get news from a specific website/source.
    
    Args:
        site: Website domain (e.g., 'cnn.com', 'bbc.com', 'reuters.com')
        language: Language code (e.g., 'en', 'es', 'fr')
        country: Country code (e.g., 'US', 'GB', 'IN')
        max_results: Maximum number of results (1-100)
    
    Returns:
        JSON string containing news articles from the site
    """
    try: 
        logger.info(f"{datetime.now()} - Getting news by site: {site}")
        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )
        
        news = google_news.get_news_by_site(site)
        return json. dumps({"status": "success", "site": site, "results":  news}, indent=2)
    except Exception as e:
        logger.error(f"Error getting news by site: {str(e)}")
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
        return json. dumps({
            "status": "success",
            "languages": google_news.AVAILABLE_LANGUAGES
        }, indent=2)
    except Exception as e:
        return json.dumps({"status":  "error", "message": str(e)}, indent=2)


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
        "mcp_endpoint":  "/sse",
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


# Create SSE transport for MCP
sse = SseServerTransport("/messages/")


async def handle_sse(request: Request) -> Response:
    """Handle SSE connections for MCP"""
    logger.info(f"{datetime.now()} - New SSE connection established")
    async with sse. connect_sse(
        request. scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )
    return Response()


async def handle_messages(request: Request) -> Response:
    """Handle POST messages for MCP"""
    logger. info(f"{datetime.now()} - Processing request of type {request.method}")
    await sse.handle_post_message(request. scope, request.receive, request._send)
    return Response()


# Create Starlette app with SSE transport
app = Starlette(
    routes=[
        Route("/", root_handler),
        Route("/sse", handle_sse),
        Route("/messages/", handle_messages, methods=["POST"]),
    ],
)

# Add CORS middleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Heroku sets PORT)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting GNews MCP Server on {host}:{port}")
    uvicorn.run("gnews_mcp_server:app", host=host, port=port, log_level="info")
