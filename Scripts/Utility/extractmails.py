import sys

def extract_mails(inlist):
    out_list = []
    in_file = open(inlist)
    in_lines = in_file.readlines()
    for line in in_lines:
        realine = line
        if realine[-1] == '\n':
            realine = realine[:-1]
        myfields = realine.split('\t')
        if len(myfields) >= 4:
            if myfields[3] != ' ' and '@' in myfields[3]:
                out_list.append(myfields[3])
    return out_list



def main(argv):
    return extract_mails(argv)

if __name__ == "__main__":
    feed = list(sys.argv)
    if len(feed) < 2:
        inargs = input('Enter file name: ')
        outlines = extract_mails(inargs)
        for line in outlines:
            print(line)
