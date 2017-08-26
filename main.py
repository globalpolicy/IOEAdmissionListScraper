import json
import bs4 as beautifulsoup
import requests

collegeid = 1  # upto 14
url = "https://admission.ioe.edu.np/AllApplicantList"

for collegeid in range(1, 15):
    endofpages = False
    pagenumber = 1
    outputfile = "D:\\College" + str(collegeid) + ".csv"
    while not endofpages:
        payload = {"Page": pagenumber, "collegeId": collegeid}
        res = requests.post(url, data=payload)

        data = json.loads(res.text)["Data"]
        souped = beautifulsoup.BeautifulSoup(data)

        if souped.find("thead") is None:  # if empty result was returned
            endofpages = True
            break

        with open(outputfile, "a") as file:

            if pagenumber == 1:  # only retrieve the table headers once for a college
                outputline = ""
                toprow = souped.find("thead")
                for column in toprow.find_all("th"):
                    outputline = outputline + column.text + ","
                outputline = outputline[:-1] + "\n"
                file.write(outputline)

            for row in souped.find_all("tr"):
                outputline = ""
                for column in row.find_all("td"):
                    outputline = outputline + column.text + ","
                if outputline != "":  # skips out the column data for the header row
                    outputline = outputline[:-1] + "\n"
                    file.write(outputline)
        print("Page #" + str(pagenumber) + " of College #" + str(collegeid))
        pagenumber = pagenumber + 1  # increment page number for the next iteration
