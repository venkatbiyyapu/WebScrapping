import requests
import pdfkit
def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
url="http://www.legis.la.gov/Legis/ViewDocument.aspx?d=1256470"
if "pdf" in url.lower():
    downloadFile(url, "1.pdf")

# pdfkit.from_url("https://www.capitol.hawaii.gov/sessions/session2022/bills/HCR37_HD1_.htm","2.pdf")
