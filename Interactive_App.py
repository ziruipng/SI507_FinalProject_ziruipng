import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import json


# +
# TreeNode and create_tree functions from previous example
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.data) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

def create_tree(data, root=None, level=0):
    if root is None:
        root = TreeNode(data[level])
        level += 1

    if level < len(data):
        child_node = TreeNode(data[level])
        root.add_child(child_node)
        create_tree(data, child_node, level + 1)

    return root

# Function to convert tree to list
def tree_to_list(node):
    result = [node.data]
    for child in node.children:
        result.extend(tree_to_list(child))
    return result



# -

# Load COVID-19 data
file = open("CombinedData.json")
data = json.load(file)
data = data[:2000]
tree = create_tree(data)
data_list = tree_to_list(tree)
df = pd.DataFrame(data_list)

# +
# Load news data
api_key = "baa39d60d9104b6c81cafdbb2ece674c"

def access_news(api_key, query):
    url = f"https://newsapi.org/v2/top-headlines?q={query}&apiKey={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)
    articles = data["articles"]
    output = []

    for article in articles:
        title = article["title"]
        author = article["author"]
        date = article["publishedAt"]
        description = article["description"]
        content = article["content"]
        url = article["url"]
        image = article["urlToImage"]
        
        article_data = {
            "title": title,
            "author": author,
            "date": date,
            "description": description,
            "content": content,
            "url": url,
            "image": image
        }
        output.append(article_data)
    return output

# Set up the app layout
st.set_page_config(page_title="COVID-19 Data Analysis and News", page_icon=":newspaper:")
st.title("COVID-19 Data Analysis and News")

## State selection
state = st.sidebar.selectbox("Select a state", df["state"].unique())

# Filter the data by state
filtered_df = df[df["state"] == state]

# Show the filtered data
st.write(f"Showing data for {state}")
st.dataframe(filtered_df)

# Visualization selection
visualization = st.sidebar.selectbox("Select a visualization", ["Case Percent", "White Percent", "Percent Vaccinated", "Vaccination vs. Death Percent"])

if visualization == "Case Percent":
    # Line chart of case percent over time
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("Case Percent")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x="name", y="percent_case", ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)
elif visualization == "White Percent":
    # Line chart of case percent over time
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("White Percent")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x="name", y="percent_white", ax=ax)
    plt.xticks(fontsize=6,rotation=90)
    st.pyplot(fig)   
elif visualization == "Percent Vaccinated":
    # Bar chart of percent vaccinated
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("Percent Vaccinated")
    sns.barplot(data=filtered_df, x="name", y="percent_vaccinated")
    plt.xticks(rotation=90)
    st.pyplot()
else:
    # Scatter plot of percent vaccinated vs percent death
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("Vaccination vs. Death Percent")
    sns.scatterplot(data=filtered_df, x="percent_vaccinated", y="percent_death")
    st.pyplot()




## News search
st.sidebar.header("News Search")
query = st.sidebar.text_input("Enter a key word to search news:")
if query:
    news_json = access_news(api_key, query)
    st.write(f"Showing top headlines for '{query}':")
    for article in news_json:
        st.write(f"{article['title']} ({article['date']})")
        st.write(article['description'])
        st.write(article['url'])
        st.image(article['image'], use_column_width=True)

# Footer
st.write("---")
st.write("This project was created using Streamlit.")
st.write("COVID-19 data source: https://covidactnow.org/?s=46183366")
st.write("News data source: https://newsapi.org/")

# -


