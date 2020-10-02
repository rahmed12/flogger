# flogger

To get this to connect to you database you must change the settings in the file .flaskenv \
\
SECRET_KEY='' <----- add any value here.  On your python command you can run: \
                                          import os \
                                          os.urandom(24) \
                                          and take the value between the single quotes '' as your secret key \
\
\
DB_USERNAME=''  <--- your username for the db \
DB_PASSWORD=''  <--- your password for the db \
\
\
BLOG_POST_IMAGES_PATH=''  <--- the static path you want to store assets like images, videos, etc... For example for me \
                               I set it to: /home/user/mlprojects/flogger/static/images/uploads \
                               Then I created the dir /home/user/mlprojects/flogger/static/images/uploads 
                               
