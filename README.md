
#### Tasks

- [x] Use selenium for scraping  
    - [ ] Try seleniumbase for scraping
- [x] scrape hdfc netbanking site to download daily transaction sheet.  
- [x] parse transaction sheet   
- [x] make DB schema  
- [x] store transactions in db  
    - [ ] upload transactions to cloud db (maybe ?), so that app can read off it and list it to  user  
- [ ] user can add/remove tags, add description (text) to the transactions  
- [ ] transactions that don't have tags added to them should be up on the list  
- [ ] screen to show split of expenses on each tag  


#### how to run the scrape process daily ?
- cron job
- cloud function (can we schedule this ?)
- spin up container every night, process, and kill container

## _Safely_ using credentials 
- On local machine - use environment variables or files (variables are better, because we can use them for runtime only)
    - Eg. `VAR1=value1 VAR2=value2 command` `VAR1` and `VAR2` are used only for running the `command`
- On cloud - can use AWS Secrets Manager to securely retreive netbanking credentials. 

