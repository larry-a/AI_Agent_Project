
import streamlit as st
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# Step 1: Define the function to search the internet using Serper API
def search_internet(query: str) -> str:
    """Search the internet using Serper API and return formatted results."""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'content-type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        
        if 'organic' not in response.json():
            return """Apologies, I couldn't locate any results for that query. 
                      The problem might be with your Serper API key."""
        else:
            results = response.json()['organic']
            formatted_results = []
            
            for result in results[:top_result_to_return]:
                try:
                    formatted_result = f"""
**{result['title']}**
🔗 {result['link']}
📝 {result['snippet']}
---
"""
                    formatted_results.append(formatted_result)
                except KeyError:
                    continue
            
            return '\n'.join(formatted_results)
    
    except Exception as e:
        return f"Search failed: {str(e)}"

# Step 2: Streamlit UI
def main():
    st.title("🔍 Internet Search Tool")
    st.markdown("Enter a search query to get the top results from the internet using Serper API.")
    
    # Add some styling
    st.markdown("""
    <style>
    .search-box {
        padding: 10px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create input field
    query = st.text_input("🔎 Enter your search query:", placeholder="e.g., Python programming tutorials")
    
    # Create search button
    if query and st.button("🚀 Search", type="primary"):
        with st.spinner("Searching the internet..."):
            result = search_internet(query)
        
        # Display results
        st.subheader("📊 Search Results:")
        st.markdown(result)
    
    # Add sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("This search tool uses the Serper API to fetch search results from Google.")
        st.write("**Features:**")
        st.write("• Top 4 search results")
        st.write("• Real-time web search")
        st.write("• Clean, formatted output")
        
        st.header("🛠️ How to use:")
        st.write("1. Enter your search query")
        st.write("2. Click the Search button")
        st.write("3. View the results below")

# Step 3: Run the Streamlit app
if __name__ == "__main__":

    main()


