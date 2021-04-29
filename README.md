# Web_Scraping using Beautiful soup

https://agmarknet.gov.in/ is an Indian government web portal to deliver the basic information of all the commodities publicly sold in India.

### Problem statements:
Lets say you want to perform the data analysis on the crop price data, for that you would need the data to be in your system or database or remote database, i.e.. some accessible form, but accessing directly from website is not sort of feasible. So the simple solution is to download the data in XLS as offered on the portal and convert to csv or store to database. But, there are 344 different commodities, will you download each and every commodity separately?

The better option is Web Scraping. through web scraping and beautiful soup, we can scrape the desired data from the website and use as we want.

So, in this repo I'll explain how i scraped the data for all 344 commodities for date ranging from 2015 to 2021.

---

The basic technic to Web scraping is by toggling the URL and sending the request to server, storing the response and then using the `BeautifulSoup` we get the html code of the site. So, to get started, select any commodity and any date and click search and the URL will change to
> ###### https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=325&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom=01-Mar-2015&DateTo=01-Apr-2015&Fr_Date=01-Mar-2015&To_Date=01-Apr-2015&Tx_Trend=0&Tx_CommodityHead=Almond(Badam)&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--"

This is our base URL, here if you try to read carefully, you will find all the values of all the attributes such as `commodity`, `state`, `district`, `market`, `date from` and `date to` and these attribute are first present with numeric value and then string value, we will need to alter the numeri's only.


**First**, In the portal, the total entries to be displayed on page are set to 50, and the `next page` button cant be handled by html request in this case, which means using web scraping we cant direct to next page and get 50-100 or so on entries. However we can set the date range so small that the number of entries are guaranteed to be less than 50. And for that I've made a list of list with size 73x2, which means 73 list containing 2 values, `date from` and `date to`, are stored in one list. the gap between `date from` to `date to` is 15 days, but you can change for yourself by toggling the `day_diff_15 = dt.timedelta(days = 15)` value.

**Second**, getting all the commodity values. Here we will use the web scraping for the first time. I've used the base URL and got the response, saved as html in `soup` variable of type bs4.BeautifulSoup. Now we need to get the idea of where the HTML code for the commodity values is located, for that we'll inspect the page by pressing the `F12` key.
![screen shot](http://github.com/DpHaRtUeVl/Web_Scraping--agmarknet.gov.in/images/agmarknet.png)
