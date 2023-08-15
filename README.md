* Use selenium for scraping
* Try seleniumbase for scraping



1. scrape hdfc netbanking site to download daily transaction sheet. **This needs user Id and password for netbanking**
2. parse transaction sheet and store transactions in db
3. upload transactions to cloud db (maybe ?), so that app can read off it and list it to user
4. user can add/remove tags, add description (text) to the transactions
5. transactions that don't have tags added to them should be up on the list
6. screen to show split of expenses on each tag


1. how to run the scrape process daily ?
    cron job, cloud function (can we schedule this ?)
    
can use AWS Secrets Manager to securely retreive netbanking credentials. 


first steps
---
1. get scraper to work on local machine
2. set daily cronjob and check
3. how to work in the UI ? Lots of work on this UI is left too
4. 


db design
---
could run the 