import datetime as dt

def saveToTxt(txt, log):
    with open(txt, 'r') as f:
        content = f.read()
    f.close()
    with open(txt, 'w') as f:
        f.write(content + '\n' + log)
    f.close()
def getTimestamp():
    current = dt.datetime.now()
    return str(f"[{current}]")

def logError(msg):
    logtype = "[ERROR]"
    ts = getTimestamp()
    log = str(f'{ts}{logtype} - {msg}')
    saveToTxt(txt='console-logs.txt', log=log)
    print(log)

def logInfo(msg):
    logtype = "[INFO]"
    ts = getTimestamp()
    log = str(f'{ts}{logtype} - {msg}')
    saveToTxt(txt='console-logs.txt', log=log)
    print(log)

