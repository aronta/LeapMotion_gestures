from os import path

f = None


def time_convert(sec, msg):
    global f
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print(msg + "\t\t{0}:{1}:{2:.2f}".format(int(hours), int(mins), sec))
    f.write(msg + "\t\t{0}:{1}:{2:.2f}\n".format(int(hours), int(mins), sec))


def create_file(directory):
    global f
    for i in range(1, 20):
        if path.exists(directory + "test_" + str(i) + ".txt"):
            continue
        f = open(directory + "test_" + str(i) + ".txt", "w")
        break

