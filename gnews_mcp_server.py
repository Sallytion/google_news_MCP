"""
GNews MCP Server
Provides Google News search capabilities via Model Context Protocol
"""

import json
import os
import logging
import contextlib
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from gnews import GNews

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request


# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# MCP Server Initialization
# -------------------------------------------------------------------

mcp = FastMCP(
    name="GNews Server",
    instructions=(
        "A server that provides Google News search capabilities including "
        "keyword search, top news, topic-based news, location-based news, "
        "and site-specific news."
    ),
    stateless_http=True,
)


# -------------------------------------------------------------------
# MCP Tools
# -------------------------------------------------------------------

@mcp.tool()
def search_news(
    keyword: str,
    language: str = "en",
    country: str = "US",
    period: str = "7d",
    max_results: int = 10,
    exclude_websites: str = "",
) -> str:
    """Search for news articles by keyword."""
    try:
        logger.info("%s - Searching news for keyword: %s", datetime.now(), keyword)

        exclude_list = [
            site.strip()
            for site in exclude_websites.split(",")
            if site.strip()
        ]

        google_news = GNews(
            language=language,
            country=country,
            period=period,
            max_results=max_results,
            exclude_websites=exclude_list,
        )

        news = google_news.get_news(keyword)
        return json.dumps(
            {"status": "success", "keyword": keyword, "results": news},
            indent=2,
        )

    except Exception as e:
        logger.error("Error searching news: %s", str(e))
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_top_news(
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """Get top news headlines."""
    try:
        logger.info("%s - Fetching top news", datetime.now())

        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )

        news = google_news.get_top_news()
        return json.dumps(
            {"status": "success", "type": "top_news", "results": news},
            indent=2,
        )

    except Exception as e:
        logger.error("Error getting top news: %s", str(e))
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_topic(
    topic: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """Get news by topic category."""
    valid_topics = {
        "WORLD",
        "NATION",
        "BUSINESS",
        "TECHNOLOGY",
        "ENTERTAINMENT",
        "SPORTS",
        "SCIENCE",
        "HEALTH",
        "POLITICS",
        "CELEBRITIES",
    }

    topic_upper = topic.upper()
    if topic_upper not in valid_topics:
        return json.dumps(
            {
                "status": "error",
                "message": f"Invalid topic. Valid topics: {', '.join(sorted(valid_topics))}",
            },
            indent=2,
        )

    try:
        logger.info("%s - Fetching news by topic: %s", datetime.now(), topic_upper)

        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )

        news = google_news.get_news_by_topic(topic_upper)
        return json.dumps(
            {"status": "success", "topic": topic_upper, "results": news},
            indent=2,
        )

    except Exception as e:
        logger.error("Error getting news by topic: %s", str(e))
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_location(
    location: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """Get news by location."""
    try:
        logger.info("%s - Fetching news for location: %s", datetime.now(), location)

        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )

        news = google_news.get_news_by_location(location)
        return json.dumps(
            {"status": "success", "location": location, "results": news},
            indent=2,
        )

    except Exception as e:
        logger.error("Error getting news by location: %s", str(e))
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_news_by_site(
    site: str,
    language: str = "en",
    country: str = "US",
    max_results: int = 10,
) -> str:
    """Get news from a specific website."""
    try:
        logger.info("%s - Fetching news from site: %s", datetime.now(), site)

        google_news = GNews(
            language=language,
            country=country,
            max_results=max_results,
        )

        news = google_news.get_news_by_site(site)
        return json.dumps(
            {"status": "success", "site": site, "results": news},
            indent=2,
        )

    except Exception as e:
        logger.error("Error getting news by site: %s", str(e))
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_available_countries() -> str:
    """Get supported countries."""
    try:
        google_news = GNews()
        return json.dumps(
            {"status": "success", "countries": google_news.AVAILABLE_COUNTRIES},
            indent=2,
        )
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
def get_available_languages() -> str:
    """Get supported languages."""
    try:
        google_news = GNews()
        return json.dumps(
            {"status": "success", "languages": google_news.AVAILABLE_LANGUAGES},
            indent=2,
        )
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


# -------------------------------------------------------------------
# MCP Resources
# -------------------------------------------------------------------

@mcp.resource("gnews://config")
def get_config() -> str:
    """Server configuration."""
    return json.dumps(
        {
            "server": "GNews MCP Server",
            "version": "1.0.0",
            "capabilities": [
                "search_news",
                "get_top_news",
                "get_news_by_topic",
                "get_news_by_location",
                "get_news_by_site",
                "get_available_countries",
                "get_available_languages",
            ],
        },
        indent=2,
    )


# -------------------------------------------------------------------
# Starlette App
# -------------------------------------------------------------------

async def root_handler(request: Request):
    return JSONResponse(
        {
            "name": "GNews MCP Server",
            "version": "1.0.0",
            "status": "running",
            "mcp_endpoint": "/mcp",
        }
    )


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        logger.info("MCP session manager started")
        yield
        logger.info("MCP session manager stopped")


mcp.settings.streamable_http_path = "/mcp"

app = Starlette(
    routes=[
        Route("/", root_handler),
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id", "Mcp-Session-Id"],
)


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    logger.info("Starting GNews MCP Server on %s:%s", host, port)
    uvicorn.run("gnews_mcp_server:app", host=host, port=port, log_level="info")
