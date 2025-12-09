from fastmcp import FastMCP
import feedparser

mcp = FastMCP(name="Teradata University Content Searcher")

@mcp.tool()
def search_teradata_university(query: str, max_results: int = 3):
    """Search Teradata University content via RSS by title/description.
    
    Args:
        query (str): Search term to find in article titles or descriptions
        max_results (int): Maximum number of results to return (default: 3)
    
    Returns:
        list: Matching articles with title and URL
    """
    feed = feedparser.parse("https://www.teradata.com/university/rss")
    results = []
    query_lower = query.lower()
    
    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")
        
        if query_lower in title.lower() or query_lower in description.lower():
            results.append({
                "title": title,
                "url": entry.get("link", ""),
                "published": entry.get("published", "")
            })
        
        if len(results) >= max_results:
            break
    
    return results if results else [{"message": "No content found matching your query"}]


@mcp.tool()
def get_latest_teradata_content(count: int = 5):
    """Get the latest content from Teradata University.
    
    Args:
        count (int): Number of recent articles to retrieve (default: 5)
    
    Returns:
        list: Recent articles with title, URL, and publish date
    """
    feed = feedparser.parse("https://www.teradata.com/university/rss")
    results = []
    
    for entry in feed.entries[:count]:
        results.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", "")[:200] + "..."  # First 200 chars
        })
    
    return results


@mcp.tool()
def get_content_by_category(category: str, max_results: int = 5):
    """Filter Teradata University content by category/topic.
    
    Args:
        category (str): Category keyword (e.g., 'analytics', 'cloud', 'AI', 'SQL')
        max_results (int): Maximum number of results to return (default: 5)
    
    Returns:
        list: Articles matching the category
    """
    feed = feedparser.parse("https://www.teradata.com/university/rss")
    results = []
    category_lower = category.lower()
    
    for entry in feed.entries:
        title = entry.get("title", "").lower()
        description = entry.get("description", "").lower()
        tags = " ".join([tag.get("term", "").lower() for tag in entry.get("tags", [])])
        
        if category_lower in title or category_lower in description or category_lower in tags:
            results.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "category_match": category,
                "published": entry.get("published", "")
            })
        
        if len(results) >= max_results:
            break
    
    return results if results else [{"message": f"No content found for category '{category}'"}]


@mcp.tool()
def teradata_secret_message():
    """Returns a special message for demo attendees."""
    return "🎓 Thank you for joining us for this demo! Keep learning with Teradata University!"


if __name__ == "__main__":
    mcp.run(transport="http")  # HTTP transport for FastMCP Cloud
