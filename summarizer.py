#!/usr/bin/env python3

from ctypes import c_char
from email import message_from_binary_file
from email import policy
from optparse import OptionParser
from multiprocessing import Pool, Value, Array
from shutil import rmtree
import os
import time
import zipfile

ZIP_FILES_PATH="../sample/"
TARGET_DIR="summarized/"

counter = None
total_zip_files = None
session_file = None

def init(args, args2, args3):
    ''' store the counter for later use '''
    global counter
    global total_zip_files
    global session_file
    counter = args
    total_zip_files = args2
    session_file = args3
    

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% ({iteration}/{total}) {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        

def restore_session(src_dir, dst_dir):
    session = None
    # get zip file completly summarized
    with open('session') as f:
        session = f.read().splitlines()
    # Find directories which are not a complete zip file summarized
    left_over_dirs = [directory for directory in os.listdir(dst_dir) if directory + '.zip' not in session]
    # delete found directories with not a complete zip file summarized
    for directory in left_over_dirs:
        rmtree(os.path.join(dst_dir, directory))
    # return all files in src_dir but the ones in session
    return [zip_file for zip_file in os.listdir(src_dir) if zip_file not in session]
    

def summarize_message(mail):
    """
    Summarizes an email message in binary format by extracting key fields such as the date, sender, 
    recipients, subject, body content, and attachment filenames.
    
    Parameters:
        mail (binary): A binary file or file-like object containing an email message.
    
    Returns:
        str: A summary of the email message in the format of 
        "date\nsender\nrecipients\nsubject\nbody_content\nattachment_filenames\n"
    """
    
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
            summarized_message += attachment_filename + "\n"
    return summarized_message


def summarize_eml_file(filename, src_dir):
    zip_filename, eml_file = os.path.split(filename)
    zip_filename = os.path.join(src_dir, "{}.zip".format(zip_filename))
    print("testing with: {} -> {}".format(zip_filename, eml_file))
    with zipfile.ZipFile(zip_filename) as zip_file:
        with zip_file.open(filename) as mail:
            summarized_message = summarize_message(mail)
    return summarized_message
            

def summarize_zip_file(zip_filename, src_dir, dst_dir):
    global counter
    global zip_files_list
    global session_file
    # print("Summarizing {}...".format(zip_filename))
    zip_dir = zip_filename[:-4]
    os.mkdir(os.path.join(dst_dir, zip_dir))
    with zipfile.ZipFile(os.path.join(src_dir, zip_filename)) as zip_file:
            for eml_file in zip_file.namelist()[1:]:
                # print(eml_file)
                with zip_file.open(eml_file) as mail:
                    try:
                        summarized_message = summarize_message(mail)
                    except:
                        error_log = open("error.log", "a")
                        error_log.write(os.path.join(dst_dir, eml_file))
                        error_log.wirte("\n")
                        error_log.close()
                summarized_file = os.path.join(dst_dir, eml_file[:-4])
                with open(summarized_file, 'w') as sm:
                    sm.write(summarized_message)
    with counter.get_lock():
        counter.value += 1
        printProgressBar(counter.value, total_zip_files.value, prefix = 'Progress:', suffix = 'Complete', length = 50)
        with open(session_file.value, 'a') as session:
            session.write(zip_filename + '\n')

    
def summarize_zip_files_list(zip_files_list, src_dir, dst_dir, threads_num):
    total_zip_files = Value('i', len(os.listdir(src_dir)))
    counter = Value('i', total_zip_files.value - len(zip_files_list))
    session_file = Array(c_char, b'session')
    printProgressBar(counter.value, total_zip_files.value, prefix = 'Progress:', suffix = 'Complete', length = 50)
    with Pool(processes=threads_num, initializer=init, initargs=(counter,total_zip_files,session_file)) as pool:
        pool.starmap(
            summarize_zip_file, 
            [(zip_filename, src_dir, dst_dir) for zip_filename in zip_files_list]
            )
    

def main(src_dir, dst_dir, threads_num):
    start_time = time.time()
    if os.path.isfile('session'):
        zip_files_list = restore_session(src_dir, dst_dir)
    else:
        with open('session', 'w'):
            print("creating new session file: session")
        zip_files_list = os.listdir(src_dir)
    summarize_zip_files_list(zip_files_list, src_dir, dst_dir, threads_num)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-f", "--file", 
        dest="filename", 
        help="Run test on this eml file", 
        metavar="FILE"
        )
    parser.add_option(
        "-z", "--zip", 
        dest="zip_filename", 
        help="Run test on this zip file", 
        metavar="FILE"
        )
    parser.add_option(
        "-s", 
        dest="src_dir", 
        help="source directory", 
        metavar="DIR", 
        default=ZIP_FILES_PATH
        )
    parser.add_option(
        "-d", 
        dest="dst_dir", 
        help="destination directory", 
        metavar="DIR", 
        default=TARGET_DIR
        )
    parser.add_option(
        "-t", 
        dest="threads_num", 
        help="threads number", 
        type="int", 
        metavar="NUM", 
        default=1
        )
    parser.add_option(
        "-q", 
        action="store_false", 
        dest="verbose", 
        default=True, 
        help="don't print status messages to stdout"
        )
    (options, args) = parser.parse_args()
    
    if not os.path.isdir(options.src_dir):
        print(
            "error: specify a valid soruce directory (where ZIP files are) using the -s option"
            )
        exit(0)

    if options.filename is not None:
        print(summarize_file(options.filename, options.src_dir))
    elif options.zip_filename is not None:
        start_time = time.time()
        summarize_zip_file(options.zip_filename, options.src_dir, options.dst_dir)
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        main(options.src_dir, options.dst_dir, options.threads_num)
    
    


    
