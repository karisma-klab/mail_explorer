#!/usr/bin/env python3

from email import message_from_binary_file
from email import policy
from optparse import OptionParser
from numpy import array_split
from threading import Thread
import os
import time
import zipfile

ZIP_FILES_PATH="../sample/"
TARGET_DIR="summarized/"

def summarize_message(mail):
    message = message_from_binary_file(mail, policy=policy.default)
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
    if body is not None:
        summarized_message += body.get_content()
    for attachment in message.iter_attachments():
        attachment_filename = attachment.get_filename()
        if attachment_filename is not None:
            summarized_message += attachment.get_filename() + "\n"
    return summarized_message


def run_on_file(filename, src_dir):
    zip_filename, eml_file = os.path.split(filename)
    zip_filename = os.path.join(src_dir, "{}.zip".format(zip_filename))
    print("testing with: {} -> {}".format(zip_filename, eml_file))
    with zipfile.ZipFile(zip_filename) as zip_file:
        with zip_file.open(filename) as mail:
            summarized_message = summarize_message(mail)
            print(summarized_message)
            

def main(src_dir, dst_dir, threads_num):
    start_time = time.time()
    zip_files_list = os.listdir(src_dir)
    # create array of threads with splited zip files lists according to threads num
    threads = [Thread(target=summarize_zip_files_list, 
                      args=(file_list, src_dir, dst_dir)) for file_list in array_split(zip_files_list, threads_num)]
    # start threads
    print("starting {} threads.".format(len(threads)))
    for thread in threads:
        print("start_thread")
        thread.start()
    # join threads
    for thread in threads:
        print("join thread")
        thread.join()
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
def summarize_zip_files_list(zip_files_list, src_dir, dst_dir):
    for zip_filename in zip_files_list:
        # print(zip_filename)
        zip_dir = zip_filename[:-4]
        os.mkdir(os.path.join(dst_dir, zip_dir))
        with zipfile.ZipFile(os.path.join(src_dir, zip_filename)) as zip_file:
            for eml_file in zip_file.namelist()[1:]:
                # print(eml_file)
                with zip_file.open(eml_file) as mail:
                    summarized_message = summarize_message(mail)
                summarized_file = os.path.join(dst_dir, eml_file[:-4])
                with open(summarized_file, 'w') as sm:
                    sm.write(summarized_message)
    print("bye!")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", 
                      help="Run test on this file", metavar="FILE")
    parser.add_option("-s", dest="src_dir", 
                      help="source directory", metavar="DIR", default=ZIP_FILES_PATH)
    parser.add_option("-d", dest="dst_dir", 
                      help="destination directory", metavar="DIR", default=TARGET_DIR)
    parser.add_option("-t", dest="threads_num", 
                      help="threads number", type="int", metavar="NUM", default=1)
    parser.add_option("-q", action="store_false", dest="verbose", 
                      default=True, help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    if not os.path.isdir(options.src_dir):
        print("error: specify a valid soruce directory (where ZIP files are) using the -s option")
        exit(0)
    if options.filename is not None:
        run_on_file(options.filename, options.src_dir)
    else:
        main(options.src_dir, options.dst_dir, options.threads_num)
    
    


    
