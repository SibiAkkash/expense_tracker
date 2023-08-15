
#### Tasks

[X] Use selenium for scraping  
[ ] Try seleniumbase for scraping
[X] scrape hdfc netbanking site to download daily transaction sheet. **This needs user Id and password for netbanking**  
[X] parse transaction sheet   
[ ] make DB schema  
[ ] store transactions in db  
[ ] upload transactions to cloud db (maybe ?), so that app can read off it and list it to user  
[ ] user can add/remove tags, add description (text) to the transactions  
[ ] transactions that don't have tags added to them should be up on the list  
[ ] screen to show split of expenses on each tag  


#### how to run the scrape process daily ?
1. cron job
2. cloud function (can we schedule this ?)
3. spin up container every night, process, and kill container

## _Safely_ using credentials 
1. On local machine - use environment variables or files (variables are better, because we can use them for runtime only)
2. On cloud - can use AWS Secrets Manager to securely retreive netbanking credentials. 

