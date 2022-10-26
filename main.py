#!/usr/bin/env python3

from email import message_from_binary_file
from email import policy
import os
import time
import zipfile

ZIP_FILES_PATH="../sample/"
TARGET_DIR="summarized/"

def summarize_message(mail):
    message = message_from_binary_file(mail, policy=policy.default)
    # print(message.keys())
    summarized_message = ""
    if "date" in message:
        summarized_message += message['date'] + "\n"
    if "from" in message:
        summarized_message += message['from'] + "\n"
    if "to" in message:
        summarized_message += message['to'] + "\n"
    if "cc" in message:
        summarized_message += message['cc'] + "\n"
    if  "subject" in message:
        summarized_message += message['subject'] + "\n"
    body = message.get_body(preferencelist=('plain', 'html'))
    try:
        summarized_message += body.get_content()
    except Exception as e: print(e)
    for attachment in message.iter_attachments():
        try:
            summarized_message += attachment.get_filename() + "\n"
        except Exception as e: print(e)
    return summarized_message
    
    
if __name__ == "__main__":
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))
    zip_files_list = os.listdir(ZIP_FILES_PATH)
    for zip_filename in zip_files_list:
        print(zip_filename)
        zip_dir = zip_filename[:-4]
        os.mkdir(os.path.join(TARGET_DIR, zip_dir))
        with zipfile.ZipFile(os.path.join(ZIP_FILES_PATH, zip_filename)) as zip_file:
            for eml_file in zip_file.namelist()[1:]:
                print(eml_file)
                with zip_file.open(eml_file) as mail:
                    summarized_message = summarize_message(mail)
                summarized_file = os.path.join(TARGET_DIR, eml_file[:-4])
                with open(summarized_file, 'w') as sm:
                    sm.write(summarized_message)
    print("--- %s seconds ---" % (time.time() - start_time))


    
