from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import crawl
from webDriver import ChromeDriver
from shopeenotify import job

# example
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    driver = ChromeDriver().driver
    scheduler.add_job(job, 'interval', args=[], seconds=10)
    scheduler.start()

   
   
