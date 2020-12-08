def main():
    file = open("proba.txt", "a+")
    flag = 0
    old_seconds = 0
    left_click = 0
    right_click = 0
    double_click = 0
    scroll = 0
    go_forward = 0
    go_back = 0
    windows = 0

    lines = file.readlines()

    for line in lines:
        print line

        if "---------- Test end! ----------" in line:
            break

        if(flag):
            polje_linija = line.split('		')
            numbers = polje_linija[1].split(":")
            seconds = numbers[2]

            # !!!!!!!!!!!!! FOR EviacamTest and MouseDefault !!!!!!!!!
            # DON'T FORGET TO comment Double Click if statement
            # if old_seconds == seconds or abs(float(seconds) - float(old_seconds)) <= 0.5:
            #     double_click += 1
            #     continue

            if "Left Click" in line:
                left_click += 1
            if "Right Click" in line:
                right_click += 1
            if "Double Click" in line:
                double_click += 1
            if "Windows + Tab" in line:
                windows += 1
            if "Scroll" in line:
                scroll += 1
            if "Back" in line:
                go_back += 1
            if "Go Forward" in line:
                go_forward += 1

            old_seconds = seconds

        if "----------Test start!----------" in line:
            flag = 1

    file.write("Sume rezultata testa: \n")
    file.write("Left click = %d\n" % left_click)
    file.write("Right click = %d\n" % right_click)
    file.write("Double click = %d\n" % double_click)
    file.write("Windows + Tab = %d\n" % windows)
    file.write("Scroll = %d\n" % scroll)
    file.write("Go Back = %d\n" % go_back)
    file.write("Go Forward = %d\n" % go_forward)

    print "Left click =", left_click
    print "Right click =", right_click
    print "Double click =", double_click
    print "Windows + Tab =", windows
    print "Scroll =", scroll
    print "Go Back =", go_back
    print "Go Forward =", go_forward

    file.close()

if __name__ == "__main__":
    main()