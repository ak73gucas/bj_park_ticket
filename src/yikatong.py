#!/bin/python
#encoding:utf-8
import csv
import re

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring
 

class JingJinJiNianKa(object):
    def __init__(self, fname):
        self.fields = ["name", "price", "use_count", "description"]
        self.min_colum_num = len(self.fields)
        self.fname = fname
        self.dct = {}

    def load_data(self):
        c = CsvParser()
        self.dct = c.load_dct_from_csv(self.fname, 3, [0], [0,1,2,3])
        return self.dct



class YiKaTong(object):
    def __init__(self, fname):
        self.fields = ["row_num", "name", "price", "use_count", "description"]
        self.min_colum_num = len(self.fields)
        self.fname = fname
        self.dct = {}

    def load_data(self):
        c = CsvParser()
        self.dct = c.load_dct_from_csv(self.fname, 3, [1], [1, 2,3,4])
        return self.dct

    def print_row(self):
        c = CsvParser()
        c.load_row_data_from_csv(self.fname, 3)


class CsvParser(object):
    def __init__(self):
        pass
    
    def load_row_data_from_csv(self, fname, min_colum_num):
        with open(fname, 'r') as f:
            ff = csv.reader(f)
            
            for ln in ff:
                if "景区名称" in "".join(ln):
                    continue
                ln = [k.replace("\n", " ") for k in ln]
                if len(ln) < min_colum_num:
                    continue
                if ln[1] =="" and ln[2] == "":
                    continue
                print "\t".join(ln)
        
    def load_dct_from_csv(self, fname, min_colum_num, colum_index_list, value_index_list):
        dct = {}
        if min_colum_num < max(colum_index_list):
            min_colum_num = max(colum_index_list)
            
        if min_colum_num < max(value_index_list):
            min_colum_num = max(value_index_list)
        with open(fname, 'r') as f:
            ff = csv.reader(f)
            for ln in ff:
                if "景区名称" in "".join(ln):
                    continue
                ln = [k.replace("\n", " ").replace("\r", " ") for k in ln]

                if len(ln) < min_colum_num:
                    continue
                if ln[1] =="" and ln[2] == "":
                    continue
                key_str = "".join([ln[k] for k in colum_index_list])
                value_str = [ln[k] for k in value_index_list]
                dct[key_str] = value_str

        return dct


def clear_name(name_list):
    name_map = {}
    zazhi = ["自然风景区", "风景区", "十渡", "景区", "3A", "2A", "4A","5A", " ", "北京市", "北京", "国家森林公园", "森林公园"]
    for v in name_list:
        v_ori = v
        v = strQ2B(v.decode("utf-8")).encode("utf-8")
        vv  = v.split("(")
        v = vv[0]
        vv  = v.split(" ")
        v = vv[0]
        vv  = v.split("（")
        v = vv[0]
        for zz in zazhi:
            v = v.replace(zz, "", -1)
        if v == "":
            name_map[v_ori] = v_ori
            continue
        name_map[v] = v_ori
    return name_map




def diff_dict_keys(dct1, dct2):
    if not dct1:
        print "null dct1"
        return
    if not dct2:
        return [v for _, v in dct1]
    v_list = []
    name_map1 = clear_name(dct1.keys())
    name_map2 = clear_name(dct2.keys())

    for k, v in name_map1.items():
        if k not in name_map2.keys():
            v_list.append(dct1[v])
            # print k
            # print "\n".join(["\t".join(k) for k in v_list])
            # print "\t".join(name_map2.keys())
            # break
            continue
    return v_list

def parser():
    pass

def main():
    fname = "data/jingjinjinianka/jingjinjink_beijing.csv"
    jk = JingJinJiNianKa(fname)
    jk_dct = jk.load_data()

    fname = "data/jingjinjiykt/jingjinjiyktpt_beijing.csv"
    ykt = YiKaTong(fname)
    ykt_dct = ykt.load_data()

    jk_more_than_ykt_fname = "output/nk_more_than_ykt.txt"
    jk_more_than_ykt = diff_dict_keys(jk_dct, ykt_dct)
    with open(jk_more_than_ykt_fname, "w") as fp:
        fp.write("\n".join(["\t".join(k) for k in jk_more_than_ykt]))

    ykt_more_than_jk_fname = "output/ykt_more_than_nk.txt"
    ykt_more_than_jk = diff_dict_keys(ykt_dct, jk_dct)
    with open(ykt_more_than_jk_fname, "w") as fp:
        fp.write("\n".join(["\t".join(k) for k in ykt_more_than_jk]))

if __name__=="__main__":
    main()