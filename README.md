# Mock_Project

### The repository consists of codes for query no. - 6, 7 & 8, Encryption/Decryption of the data stored in mongoDB, Conversion of date field from string/INT to ISO format, Summary/State table creation, Data Visualization using matplotlib and Testing of API endpoints using unittest.

## Queries
### Query no. - 6
[API Used](https://covidfunding.eiu.com/api-docs/) <br/>
Request is sent to the above API, which returns JSON data for the response. <br/>
The data is ingested in a database named "twitter_db" with "donations" as collection name.

### Query no. - 7
[API Used](https://rapidapi.com/KishCom/api/covid-19-coronavirus-statistics/) <br/>
Request is sent to the above API, which returns JSON data for the response. <br/>
Country name is read from a CSV file which is then passed to the Base URL as parameter. <br/>
The fetched data is transformed in dictionary format and ingested in a database named "twitter_db" with "cases_data" as collection name. <br/>
Field of date is parsed using dateutil.

### Query no. - 8
[API Used](https://data.nasdaq.com/data/FRED-federal-reserve-economic-data) <br/>
Request is sent to the above API using quandl, which returns JSON data for the response. <br/>
Country code is read from a CSV file which is then passed to the Base URL as parameter. <br/>
The fetched data is cleaned and transformed in dictionary format. <br/>
The data is then ingested in a database named "twitter_db" with "global_economy" as collection name. <br/>
Since the API can handle only 20 requests in 10 minutes, necessary time delay is provided between each request.


## Date Conversion
Data fetched from Twitter API have date field "created_at" in form of String. <br/>
This field needs to be converted into ISO Date format to perform computation. <br/>
The operation is performed using dateutil.parser and later updated in the collection. <br/>
Data stored in collection "donations" also has fields "datePledged" and "dateConfirmed" in INT format which needs to be converted in ISO Date format. <br/>
The operation is carried out using datetime and later updated in the collection.

## Summary tables
Summary tables are created to optimize the performance of queries made by the user. <br/>
It aggregates twitter data on a daily basis. <br/>
Summary table1 consists of no. of tweets made from a location on a daily basis along with the date in consideration. <br/>
Summary table2 consists of frequency of words occurring in tweets on a daily basis along with the date in consideration. 

## Encryption/Decryption
To increase the security of the data stored in mongoDB, Client side field-level encryption is performed. <br/>
One field from each collection is encrypted using pymongo encryption (ClientEncryption and Algorithm). <br/>
Different local_master_key is generated using urandom function for every collection. <br/>
The encryption algorithm converts the field from string to binary format. <br/>
Same key must be used to decrypt the field.

## Data visualization
Data visualization is done using matplotlib. <br/>
Various bar graphs, line graphs, histograms, scatter-plots are created to visualize the data stored in twitter_db. <br/>
GDP growth of a country over the years is visualized on a scatter-plot. <br/>
Rise of covid cases and deaths in a country over a time period is visualized on a line graph. <br/>
Amount of donations made by top n country for covid relief fund is visualized on a bar graph.

## Testing
Unit test cases are written to validate the working of API endpoints. <br/>
One test case is written for each query. <br/>
Test will show passed status if the response from the server is 200 (ok response).
