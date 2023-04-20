# SI507_FinalProject_ziruipng

Run the code in the following order:

1. Access_Covid19Data.py: Need to apply for a personal API key on the Covid Act Now API official website (https://apidocs.covidactnow.org/) first, and then download the required data according to the instructions on the official website.

2. Access_CensusData.py: The original compressed file is directly downloaded from the official website, no API key is required. The code decompresses the file and filters out the data to use based on the header files in the geodatabase.

3. Access_News.py: Need to apply for a personal API key on News API official website (https://newsapi.org/) first, and then filter covid-related news based on headline content.

4. CombineData_Cencus_Covid19.py: Merge the data obtained by Access_Covid19Data.py and Access_CensusData.py according to the same attribute, and store it as a final JSON file, named CombinedData.json.

5. Interactive_Tree.py: Store the JSON data in a tree structure and make it into an interactive page. The interactive interface is realized with streamlit package.

Run "streamlit run Interactive_App.py" in the termina, then go to http://localhost:8501/ on a browser for the interactive website.
