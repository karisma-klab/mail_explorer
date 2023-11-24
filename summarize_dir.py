#!/usr/bin/env python

from summarizer import *


# Do not end the file names with a / - it's ugly but works'
SRC_DIR = "../sample2"
DST_DIR = "summarized2"

counter = None
total_files = None
session_file = None

def get_files(src_dir):
    src_dir_len = len(src_dir) + 1 # the + 1 for eliminate first slash
    files = []
    for (s_dir, dir_names, file_names) in os.walk(src_dir):
        if file_names:
            for name in file_names:
                files.append(os.path.join(s_dir[src_dir_len:],  name))
    return files

def restore_session(src_dir, dst_dir):
    session = None
    # get files completly summarized
    with open('session') as f:
        session = f.read().splitlines()
    # Find files which are not a complete file summarized
    return [filename for filename in get_files(src_dir) if filename not in session]


def init(args, args2, args3):
    ''' store the counter for later use '''
    global counter
    global total_files
    global session_file
    counter = args
    total_dirs = args2
    session_file = args3


def summarize_file(msg_file, src_dir, dst_dir):
    global counter
    global total_files
    global session_file
    summarized_message = ''
    file_path = os.path.dirname(msg_file)
    os.makedirs(os.path.join(dst_dir, file_path), exist_ok=True)
    with open(os.path.join(src_dir, msg_file), 'rb') as mail:
        try:
            summarized_message = summarize_message(mail)
        except:
            error_log = open("error.log", "a")
            error_log.write(os.path.join(dst_dir, msg_file))
            error_log.write("\n")
            error_log.close()
    summarized_file = os.path.join(dst_dir, msg_file[:-4])
    with open(summarized_file, 'w') as sm:
        sm.write(summarized_message)
    with counter.get_lock():
        counter.value += 1
        printProgressBar(counter.value, total_files.value, prefix = 'Progress:', suffix = 'Complete', length = 50)
        with open(session_file.value, 'a') as session:
            session.write(msg_file + '\n')


def summarize_file_list(files_list, src_dir, dst_dir, threads_num):
    global counter
    global total_files
    global session_file
    total_files = Value('i', len(files_list))
    counter = Value('i', total_files.value - len(files_list))
    session_file = Array(c_char, b'session')
    printProgressBar(counter.value, total_files.value, prefix = 'Progress:', suffix = 'Complete', length = 50)
    with Pool(processes=threads_num, initializer=init, initargs=(counter,total_files,session_file)) as pool:
        pool.starmap(
            summarize_file,
            [(dir_name, src_dir, dst_dir) for dir_name in files_list]
            )


def main(src_dir, dst_dir, threads_num):
    start_time = time.time()
    if os.path.isfile('session'):
        files_list = restore_session(src_dir, dst_dir)
    else:
        with open('session', 'w'):
           print("creating new session file: session")
        files_list = get_files(src_dir)
    summarize_file_list(files_list, src_dir, dst_dir, threads_num)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main(SRC_DIR, DST_DIR, 3)

