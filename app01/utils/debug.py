import datetime


def create_log(cont):
    with open('logs.txt', "a") as f:
        f.write(f"\n{cont} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


