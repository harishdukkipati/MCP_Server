from fastapi import FastAPI, Query
from wikepedia_utils import search_wikipedia, get_summary
from llm_utils import ask_llm

app = FastAPI()

@app.get("/wikipedia/search")
def wikipedia_search(q: str = Query(..., description="Search query")):
    return {"results": search_wikipedia(q)}

@app.get("/wikipedia/summary")
def wikipedia_summary(title: str):
    summary = get_summary(title)
    return {"title": title, "summary": summary}

@app.get("/chat")
def chat_with_wiki_assistant(query: str):
    print(f"Received query: {query}")
    
    titles = search_wikipedia(query)
    print(f"Wikipedia search results: {titles}")
    
    if not titles:
        print("No Wikipedia titles found.")
        return {"answer": "I couldn't find anything on Wikipedia."}
    
    summary = get_summary(titles[0])
    print(f"Summary of top article '{titles[0]}': {summary[:200]}...")  # print first 200 chars
    
    prompt = f"{summary}\n\nUser question: {query}\n\nAnswer the question based on the text above."
    print(f"Prompt sent to LLM: {prompt[:300]}...")  # first 300 chars
    
    answer = ask_llm(prompt)
    print(f"LLM answer: {answer}")
    
    return {
        "related_article": titles[0],
        "wikipedia_summary": summary,
        "llm_answer": answer
    }