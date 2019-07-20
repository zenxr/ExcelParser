# module imports
import pandas as pd
import json
import webbrowser
from flask import Flask, request, render_template
app = Flask(__name__)

# config import
import config

colsToSearchTitles = []
organisms = []
title = config.PageTitle
url = "127.0.0.1:5000"

def getSearchResults(searchQuery, itemsToSearch):
    results = []
    for dataKey, dataValue in searchQuery:
        if not dataValue == "":
            # if "Search everything"
            if dataKey == "search_all":
                for item in itemsToSearch:
                    for key, value in item.items():
                        if dataValue.lower() in str(value).lower():
                            results.append(item)
            # else search by key given
            else:
                for item in itemsToSearch:
                    for key, value in item.items():
                        if key.lower() == dataKey:
                            if (dataValue).lower() in str(value).lower():
                                results.append(item)
    return results

@app.route("/")
@app.route("/index")
def homepage():
    return render_template(
        "index.html", 
        title = title, 
        columns = [name.lower() for name in config.ColumnNamesToSearch],
        organismColumns = organisms[0].keys(), 
        organisms = organisms )

@app.route("/", methods=['POST'])
def searchPost():
    data = request.form.to_dict()

    results = getSearchResults(data.items(), organisms)

    return render_template(
        "index.html",
        title = title,
        columns = [name.lower() for name in config.ColumnNamesToSearch],
        organismColumns = organisms[0].keys(),
        organisms = results )

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
