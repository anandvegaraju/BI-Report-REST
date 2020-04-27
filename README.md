# BI-Report-REST
A simple script that allows access to Oracle Fusion BI reports via REST calls
# This is merely a demonstration of Oracle BI Report WSSS Services and isn't meant to be a solution
# Install Python and all the imported modules (refer to app.py) 
# Ensure to have the right roles/access privileges (Report folder access/Integration Specialist role)
# This example uses basic auth
# The method name is getReport

Install all the mentioned modules (pip install [module_name] in command prompt)

Run the script (py app.py in command prompt after navigating to the file directory)

Perform a GET request on http://127.0.0.1:5000/getReport

Pass the instanceURL (https://servername.fa.us2.oraclecloud.com), csvDelimiter (pipe symbol, comma symbol, etc) , reportXDOpath (/Custom/Human Capital Management/ReportName.xdo for instance) , dateParam (MM/DD/YYYY) as parameters in the GET request
