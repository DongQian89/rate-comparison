from rateTool import lpr_compare
from rateTool import zw2num


if __name__ == "__main__":
    f=open('4倍LPR利率比较问题/test.txt')
    for line in f:
        print(line.strip())
        mystr = line.strip()
        print(lpr_compare(mystr,2022,2,21))
    print(zw2num("约两千元"))