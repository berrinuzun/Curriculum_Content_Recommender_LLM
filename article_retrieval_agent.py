article_retrieval_agent = """
            # GOAL:
            As an Article Retrieval Agent, your goal is to retrieve academic articles related to the requested topic or query. You will use the SerpAPI service to perform Google Scholar searches and ensure that the articles retrieved are relevant and up to academic standards.

            # GENERAL RULES:
            Use the provided query from the professor to search for academic articles. Focus on retrieving articles that are recent, relevant, and high-quality. Your results must include the article title, a brief snippet, and a link to the full article when possible.

            Example:

            Query: "Machine Learning in Education"

            Search Results:
            1. Title: "Applications of Machine Learning in Modern Education"
               Snippet: "This paper explores how machine learning is revolutionizing educational methodologies..."
               Link: "https://example.com/machine-learning-education"

            2. Title: "AI and Adaptive Learning Systems"
               Snippet: "Adaptive learning systems powered by AI are reshaping personalized education..."
               Link: "https://example.com/ai-adaptive-learning"

            # ACTING RULES:
            1. Use the SerpAPI to perform a Google Scholar search with the given query.
                - Ensure the API key is configured correctly.
                - Use appropriate query parameters to limit results to academic articles.
            2. Validate the relevance of each article by ensuring the query keywords appear in the title or snippet.
                - Articles that do not match the query context should be excluded.
            3. Extract the following details for each relevant article:
                - Title
                - Snippet
                - Link
            4. Return the search results as a JSON object containing the list of articles.
                - If no articles are found or an error occurs, return an appropriate error message.

            # FINAL REPORT FORMAT:
            Article Retrieval Output:
            - Query: [The academic topic or query provided by the user.]
            - Articles:
                1. Title: [Title of the first article.]
                   Snippet: [Brief summary or snippet of the article.]
                   Link: [URL to the full article.]
                2. [Repeat for additional articles.]

            Summary:
            - [Briefly summarize the search results, including the total number of articles retrieved and their relevance to the query.]
            - [If applicable, provide suggestions for improving the query to get better results.]

            It is essential that the retrieved articles are accurate, relevant, and of high academic value, ensuring that they can be used effectively by other agents and professors.

            Now, review the current conversation below and determine whether the query has been provided or if you need to initiate the article retrieval process.

            -------------------------
            The current conversation:
            -------------------------
"""
from agent import Agent
import os
import json
from serpapi import GoogleSearch

class ArticleRetrievalAgent(Agent):
    
    prompt = article_retrieval_agent

    def __init__(self, name, role):
        super().__init__(name, role)
        self.api_key = os.environ.get("SERPAPI_API_KEY")
        if not self.api_key:
            raise Exception("SERPAPI_API_KEY environment variable not set.")

    def search_articles(self, query):
       
        search = GoogleSearch({
            "q": query,
            "location": "Turkey",
            "api_key": self.api_key
        })
        
        try:
            results = search.get_dict()
            articles = []
            for result in results.get('organic_results', []):
                title = result.get('title')
                snippet = result.get('snippet')
                link = result.get('link')
                if title and snippet and link:
                    articles.append({
                        "title": title,
                        "snippet": snippet,
                        "link": link
                    })
            return articles
        except Exception as e:
            return {"error": str(e)}

    def retrieve_and_validate_articles(self, query):
    
        articles = self.search_articles(query)

        if isinstance(articles, dict) and "error" in articles:
            return json.dumps({
                "status": "error",
                "message": articles["error"]
            }, indent=4)

        validated_articles = [
            article for article in articles
            if self.validate_article_relevance(article, query)
        ]

        return json.dumps({
            "status": "success",
            "articles": validated_articles
        }, indent=4)

    def validate_article_relevance(self, article, query):
 
        return query.lower() in article['title'].lower() or query.lower() in article['snippet'].lower()

