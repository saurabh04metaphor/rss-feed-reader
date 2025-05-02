@echo off
echo Task started at: %date% %time% >> task_log.txt
cd c:\Users\Saurabh Bharti\Desktop\rss_reader
call venv\Scripts\activate
python manage.py update_feeds >> task_log.txt 2>&1
echo Task completed at: %date% %time% >> task_log.txt
echo ---------------------------------------- >> task_log.txt