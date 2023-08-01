#!/usr/bin/env python3

import os
import py7zr
import summarizer
import time

from itertools import islice

start_time = time.time()

SRC_DIR = "../sample2/"
DST_DIR = "summarized2/"

def batched(iterable, chunk_size):
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, chunk_size)):
        yield chunk

seven_z_files = os.listdir(SRC_DIR)
seven_z_file = py7zr.SevenZipFile(os.path.join(SRC_DIR, seven_z_files[0]))

# Change cwd
os.chdir(DST_DIR)

# divide files into batches
batches = batched(seven_z_file.getnames(), 20)

# iterate every file in the 7z file
for batch in batches:
    files = seven_z_file.read(batch)
    for msg_file in files:
        print(msg_file)

        # create directory
        os.makedirs(os.path.dirname(msg_file), exist_ok=True)

        # get file object for msg_file
        msg = files[msg_file]

        # summarize msg_file
        summarized_msg = summarizer.summarize_message(msg)

        # white the file in the same path as in the 7z file
        with open(msg_file, "w") as f:
            f.write(summarized_msg)
    print("finished batch")
    seven_z_file.reset()


seven_z_file.close()

print("--- %s seconds ---" % (time.time() - start_time))
print("done!")













