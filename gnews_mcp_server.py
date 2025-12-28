#!/usr/bin/env python3
"""
Google News MCP Server with Streamable HTTP Transport
Provides Google News search and trending topics via MCP protocol
"""

import os
import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

# Core dependencies
from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Google News scraper
from gnews import GNews

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Google News MCP Server")

# Global GNews instance
gnews_client: Optional[GNews] = None

@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager"""
    global gnews_client
    
    # Startup
    logger.info("Starting Google News MCP Server...")
    try:
        gnews_client = GNews(
            language='en',
            country='US',
            period='7d',
            max_results=10
        )
        logger.info("GNews client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize GNews client: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Google News MCP Server...")
    gnews_client = None

# Tool: Search Google News
@mcp.tool()
async def search_news(
    query: str,
    max_results: int = 10,
    period: str = "7d",
    country: str = "US",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Search Google News for articles matching a query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
        period: Time period for search (e.g., '1d', '7d', '1m')
        country: Country code for news (default: 'US')
        language: Language code (default: 'en')
    
    Returns:
        Dictionary containing search results and metadata
    """
    global gnews_client
    
    try:
        # Update client settings
        gnews_client.period = period
        gnews_client.max_results = max_results
        gnews_client.country = country
        gnews_client.language = language
        
        # Perform search
        logger.info(f"Searching news for query: {query}")
        results = gnews_client.get_news(query)
        
        # Format results
        formatted_results = []
        for article in results:
            formatted_results.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "publisher": article.get("publisher", {}).get("title", ""),
                "published_date": article.get("published date", ""),
            })
        
        return {
            "success": True,
            "query": query,
            "count": len(formatted_results),
            "articles": formatted_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "timestamp": datetime.utcnow().isoformat()
        }

# Tool: Get Trending News
@mcp.tool()
async def get_trending(
    max_results: int = 10,
    country: str = "US",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Get trending news articles from Google News.
    
    Args:
        max_results: Maximum number of results to return (default: 10)
        country: Country code for news (default: 'US')
        language: Language code (default: 'en')
    
    Returns:
        Dictionary containing trending articles and metadata
    """
    global gnews_client
    
    try:
        # Update client settings
        gnews_client.max_results = max_results
        gnews_client.country = country
        gnews_client.language = language
        
        # Get trending news
        logger.info("Fetching trending news")
        results = gnews_client.get_top_news()
        
        # Format results
        formatted_results = []
        for article in results:
            formatted_results.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "publisher": article.get("publisher", {}).get("title", ""),
                "published_date": article.get("published date", ""),
            })
        
        return {
            "success": True,
            "count": len(formatted_results),
            "articles": formatted_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching trending news: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Tool: Get News by Topic
@mcp.tool()
async def get_news_by_topic(
    topic: str,
    max_results: int = 10,
    country: str = "US",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Get news articles for a specific topic.
    
    Args:
        topic: Topic to search for (e.g., 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH')
        max_results: Maximum number of results to return (default: 10)
        country: Country code for news (default: 'US')
        language: Language code (default: 'en')
    
    Returns:
        Dictionary containing topic articles and metadata
    """
    global gnews_client
    
    try:
        # Update client settings
        gnews_client.max_results = max_results
        gnews_client.country = country
        gnews_client.language = language
        
        # Get topic news
        logger.info(f"Fetching news for topic: {topic}")
        results = gnews_client.get_news_by_topic(topic)
        
        # Format results
        formatted_results = []
        for article in results:
            formatted_results.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "publisher": article.get("publisher", {}).get("title", ""),
                "published_date": article.get("published date", ""),
            })
        
        return {
            "success": True,
            "topic": topic,
            "count": len(formatted_results),
            "articles": formatted_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching topic news: {e}")
        return {
            "success": False,
            "error": str(e),
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat()
        }

# Tool: Get News by Location
@mcp.tool()
async def get_news_by_location(
    location: str,
    max_results: int = 10,
    period: str = "7d",
    language: str = "en"
) -> Dict[str, Any]:
    """
    Get news articles for a specific location.
    
    Args:
        location: Location to search for (city, country, region)
        max_results: Maximum number of results to return (default: 10)
        period: Time period for search (e.g., '1d', '7d', '1m')
        language: Language code (default: 'en')
    
    Returns:
        Dictionary containing location-based articles and metadata
    """
    global gnews_client
    
    try:
        # Update client settings
        gnews_client.period = period
        gnews_client.max_results = max_results
        gnews_client.language = language
        
        # Get location news
        logger.info(f"Fetching news for location: {location}")
        results = gnews_client.get_news_by_location(location)
        
        # Format results
        formatted_results = []
        for article in results:
            formatted_results.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "publisher": article.get("publisher", {}).get("title", ""),
                "published_date": article.get("published date", ""),
            })
        
        return {
            "success": True,
            "location": location,
            "count": len(formatted_results),
            "articles": formatted_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching location news: {e}")
        return {
            "success": False,
            "error": str(e),
            "location": location,
            "timestamp": datetime.utcnow().isoformat()
        }

# Resource: Server Info
@mcp.resource("info://server")
async def get_server_info() -> str:
    """Get information about the Google News MCP Server"""
    info = {
        "name": "Google News MCP Server",
        "version": "1.0.0",
        "description": "MCP server providing Google News search and trending topics",
        "capabilities": [
            "search_news",
            "get_trending",
            "get_news_by_topic",
            "get_news_by_location"
        ],
        "status": "operational" if gnews_client else "initializing",
        "timestamp": datetime.utcnow().isoformat()
    }
    return json.dumps(info, indent=2)

# Configure MCP settings
mcp.settings.streamable_http_path = "/mcp"

# Create ASGI application
app = mcp.get_asgi_app(lifespan=lifespan)

# Add CORS middleware
app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id", "Mcp-Session-Id"],
)

# Add TrustedHost middleware to fix "Invalid Host header" error
app = TrustedHostMiddleware(app, allowed_hosts=["*"])

# Run server
def run_server():
    """Run the MCP server"""
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"MCP endpoint available at http://{host}:{port}/mcp")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()
