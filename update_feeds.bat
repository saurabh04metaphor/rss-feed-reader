@echo off
cd c:\Users\Saurabh Bharti\Desktop\rss_reader
call venv\Scripts\activate
python manage.py update_feeds > task_log.txt 2>&1