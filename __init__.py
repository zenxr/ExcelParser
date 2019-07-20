# module imports
import pandas as pd
import json
import webbrowser
from flask import Flask, request, render_template
app = Flask(__name__)

# config import
import config

# contains a list of organisms, where each organism is a json of a row in the table
organisms = []
title = config.PageTitle
url = "127.0.0.1:5000"

def getAndSearchResults(searchQuery, itemsToSearch):
    '''
    Return a list of search results where returned
    items from itemToSearch matches as a positive result for all searchQuery values
    
    Parameters:
        JSon object : searchQuery
            example: 
            {
                "organism" : "oxo",
                "buzzwords" : "asdf"
            }
        JSon object : itemsToSearch
            example:
            {
                (a key, value for an organism where each key is each column in the table)
                column1Name : dataInColumn
            }
    '''
    results = []
    # get number of searchValues passed in
    searchFilterCount = 0
    for searchKey, searchValue in searchQuery:
        if (searchValue != "" and searchKey != "search_all"):
            searchFilterCount += 1
    if searchFilterCount == 0:
        return results
    for item in itemsToSearch:
        positiveResultCount = 0
        for key, value in item.items():
            # if the item is a match for all searchValues
            for searchKey, searchValue in searchQuery:
                if (key.lower() == searchKey.lower()):
                    if searchValue == "":
                        continue
                    searchWords = searchValue.split(",")
                    for searchWord in searchWords:
                        alreadyMatchedThisItem = False
                        searchWord = searchWord.strip()
                        if searchWord.lower() in str(value).lower():
                            if not alreadyMatchedThisItem:
                                positiveResultCount += 1
                                alreadyMatchedThisItem = True
        if positiveResultCount == searchFilterCount:
            results.append(item)
    return results
                #if not searchKey == "search_all":
                #    if not searchValue in 


def getOrSearchResults(searchQuery, itemsToSearch):
    '''
    Return a list of search results where any key in
    searchQuery gives a result in itemsToSearch

    Parameters:
        JSon object : searchQuery
            example: 
            {
                "organism" : "oxo",
                "buzzwords" : "asdf"
            }
        JSon object : itemsToSearch
            example:
            {
                (a key, value for an organism where each key is each column in the table)
                column1Name : dataInColumn
            }
    '''
    results = []
    # for each key, value in the searchQuery
    for searchKey, searchValue in searchQuery:
        # if the value is not empty
        if not searchValue == "":
            if searchKey != "search_all":
                # if not "Search everything"
                for item in itemsToSearch:
                    for key, value in item.items():
                        # if item's key is the searchKey
                        # ex: searchKey = "buzzword", item's key = "buzzword"
                        if key.lower() == searchKey:
                            alreadyMatchedThisItem = False
                            searchWords = searchValue.split(",")
                            for searchWord in searchWords:
                                searchWord = searchWord.strip()
                                if searchWord.lower() in str(value).lower():
                                    if not alreadyMatchedThisItem:
                                        results.append(item)
                                        alreadyMatchedThisItem = True
    return results

'''
Return a list of search results where any value in 
items.ToSearch.items()'s values match the searchValue
'''
def searchAll(searchValue, itemsToSearch):
    results = []
    # search every item
    for item in itemsToSearch:
        for key, value in item.items():
            alreadyMatchedThisItem = False
            searchWords = searchValue.split(",")
            for searchWord in searchWords:
                searchWord = searchWord.strip()
                if searchWord.lower() in str(value).lower():
                    if not alreadyMatchedThisItem:
                        results.append(item)
                        alreadyMatchedThisItem = True
            # if searchValue is a substring of value
            if searchValue.lower() in str(value).lower():
                results.append(item)
    return results


'''
When requesting GET "/", send back a list where each item is a row
of json data
'''
@app.route("/")
@app.route("/index")
def homepage():
    return render_template(
        "index.html", 
        title = title,
        github_repo_link = config.GitHubRepoLink, 
        columns = [name.lower() for name in config.ColumnNamesToSearch],
        organismColumns = organisms[0].keys(), 
        organisms = organisms )

'''
When POST "/", 
search using request.form's data, 
send back a list where each item fits the search and is a row
of json data
'''
@app.route("/", methods=['POST'])
def searchPost():
    data = request.form.to_dict()

    results = []
    if config.SearchAnd:
        results.extend(getAndSearchResults(data.items(), organisms))
    else:
        results.extend(getOrSearchResults(data.items(), organisms))

    if all(value is "" for key, value in data.items()):
        results.extend(organisms)

    if not data["search_all"] == "":
        searchAllResults = searchAll(data["search_all"], organisms)
        results.extend(searchAllResults)

    return render_template(
        "index.html",
        title = title,
        github_repo_link = config.GitHubRepoLink, 
        columns = [name.lower() for name in config.ColumnNamesToSearch],
        organismColumns = organisms[0].keys(),
        organisms = results )

'''
Main
    Convert .xlsx to json and start server
'''
if __name__ == "__main__":
    # load the file into pandas as xl
    xl = pd.ExcelFile(config.ExcelFilePath)

    # note - this only reads a single sheet. Easy enough to modify if needed
    # see pandas documentation
    dataframe = xl.parse(config.SheetToParse)

    # generate a list of json objects from the data
    # each row (organism currently) is added to a list with all of its columns
    for i in dataframe.index:
        organisms.append(json.loads(dataframe.loc[i].to_json()))
    
    # remove empty rows (discard junk rows)
    for row in organisms:
        if all(value is None for key, value in row.items()):
            organisms.remove(row)
    # open browser, change config to disable        
    if (config.OpenBrowser):
        webbrowser.open(url)

    app.run()
