COVID-19

We here try to predict the COVID-19 confirmed of every country in 7 days by deep learning.

I used last 30 days COVID-19 data including 'confirmed', 'cured' and 'dead' to train my deep learning model which is developed by pytorch.

I predict all related countries(or area), for now, it's 185.

To be clear, I put the top 10 country figures on the website top.

Here is my code structure:

1.I get raw data from github manually, it's a html file downloaded from web address like "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/07-25-2020.csv";

2.Using BS4, we get the raw data of the world covid-19 by spider.py, and save the raw data in "raw" directory;

3.Handle the raw data into list data as a file in "list_data" directory;

4.Handle the list data into csv file in "csv_all" directory;

5.handle the list data into js data, saved in "data" directory, those will be used by "index.php" to show figures at websit;

6.Prediction by the trained model and draw figure one by one.

7.Put them on my website. Still, the index.html is open source.

---
GOD BLESS THE WORLD!