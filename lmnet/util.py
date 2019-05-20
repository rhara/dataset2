import time


def prettysize(size):
    if size < 1024:
        sizestr = f'{size}b'
    elif size < 1024*1024:
        sizestr = f'{size/1024:.2f}kb'
    elif size < 1024*1024*1024:
        sizestr = f'{size/1024/1024:.2f}mb'
    else:
        sizestr = f'{size/1024/1024/1024:.2f}gb'
    return sizestr


def prettymtime(mtime):
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
    return timestr
