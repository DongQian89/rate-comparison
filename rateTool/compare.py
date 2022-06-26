import re
import akshare as ak
import datetime
from pycnnum import cn2num

def compare_4lpr(mystr,year,month,day):
    """
    mystr:输入文本如“月利率0.2%”
    year,month,day:LPR参考的时间,格式为2022,2,21
    return:转换后相应的月利率monthly_rate,是否大于4倍LPR
    """
    
    # 1.提取给定时间的LPR
    lpr_df = ak.macro_china_lpr()
    # 一年期lpr
    lpr_1y = lpr_df.loc[lpr_df["TRADE_DATE"]==datetime.date(year,month,day)].LPR1Y.values[0]
    # 五年期lpr
    lpr_5y = lpr_df.loc[lpr_df["TRADE_DATE"]==datetime.date(year,month,day)].LPR5Y.values[0]
    # print("lpr_1y:",lpr_1y)
    
    # 2.提取文本中的数字部分、单位(%,‰,分，厘)及年月日
    
    # 把中文数字转为阿拉伯数字
    try:
        mynum=float(cn2num(mystr))
    except:
        number = re.compile(r'([一二三四五六七八九零十百千万亿]+|[,]*[0-9]+.[0-9]+|[,]*[0-9]+)')
        num_pattern = re.compile(number)
        mynum = num_pattern.findall(mystr)[0]
        mynum=float(mynum)
    # print("mynum:",mynum)
    
    rank = re.compile(r'([年月日]+)')
    rank_pattern = re.compile(rank)
    myrank = rank_pattern.findall(mystr)[0]
    # print("myrank:",myrank)
    
    unit = re.compile(r'([%‰分厘]+|[万分之]+[千分之])')
    unit_pattern = re.compile(unit)
    myunit = unit_pattern.findall(mystr)[0]
    # print("myunit:",myunit)
    
    # 创建词典便于转换为月利率(%)运算
    rank_dict = {"年":1/12,
             "月":1,
             "日":30}
    unit_dict = {"%":{"年":1,"月":1,"日":1},
                "‰":{"年":1/10,"月":1/10,"日":1/10},
                "分":{"年":10,"月":1,"日":1/10},
                "厘":{"年":1,"月":1/10,"日":1/100},
                "万分之":{"年":1/100,"月":1/100,"日":1/100},
                "千分之":{"年":1/10,"月":1/10,"日":1/10},}
    # print("rank_dict[myrank]:",rank_dict[myrank])
    # print("unit_dict[myunit[myrank]]:",unit_dict[myunit][myrank])
    # 将利率转为月利率，单位为百分比%
    monthly_rate = mynum * float(rank_dict[myrank]) * float(unit_dict[myunit][myrank])
    # print(mystr,"转换后的monthly_rate:", monthly_rate)
    # print("该利率大于4倍LPR:",monthly_rate > (lpr_1y/3))
    
    return monthly_rate > lpr_1y/3


def lpr_compare(mystr,year,month,day):
    try:
        return compare_4lpr(mystr,year,month,day)
    except:
        return None


def zw2num(mystr):
    try:
        return cn2num(mystr)
    except:
        return None


if __name__ == "__main__":
    # f=open('4倍LPR利率比较问题/test.txt')
    # for line in f:
        # print(line.strip())
        # mystr = line.strip()
        # print(lpr_compare(mystr,2022,2,21))
    print(zw2num("约两千元"))
        
