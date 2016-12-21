#! usr/bin/env/python
# -*-coding:utf-8-*-
import pymssql
import json
def filter_sku():
    """get the sku should be purchased"""
    select_sql = [
        "select DISTINCT d.sku,t.addressowner,bgs.goodsskustatus",
        "from P_tradedtun as d LEFT JOIN P_tradeun as t on d.tradenid = t.nid LEFT JOIN B_Goodssku as bgs on d.sku = bgs.sku",
        "where t.PROTECTIONELIGIBILITYTYPE='缺货订单'",
        "and  bgs.goodsskustatus in ('停产', '停售', '清仓', '线上清仓')"
    ]
    select_query = " ".join(select_sql)
    check_status = "select d.StockOrderNID,d.GoodsSKUID, g.sku as sku from CG_StockOrderM  as m  LEFT JOIN CG_StockOrderD as d on m.nid = d.StockOrderNID LEFT JOIN B_Goodssku as g on d.GoodsSKUID= g.nid  where CheckFlag= 0 and DATEPART(month,MakeDate )=DATEPART(month,GETDATE() ) and  DATEPART(YEAR,MakeDate )=DATEPART(YEAR,GETDATE() ) "
    select_sku = 'wo_test_purchasingBill @chkNoShowPur=1'
    try:
        con = pymssql.connect(server='121.196.233.153', user='sa', password='allroot89739659', database='ShopElf', port='12580')
        cur = con.cursor(as_dict=True)
        cur.execute(select_sku)
        out_select_sku = cur.fetchall()
        cur.execute(select_query)
        out_select_query = cur.fetchall()
        cur.execute(check_status)
        out_check_status = cur.fetchall()
        unchecked_sku = [out["sku"] for out in out_check_status]
        out_sku = {}
        # all_sku = list()
        for out in out_select_sku:
            temp_sku = out['SKU']
            for row in out_select_query:
                sku = row['sku']
                if temp_sku == sku:
                    out_flag = count_flag(row['addressowner'], sku, row['goodsskustatus'])
                    if not out_flag['flag'] == '':
                        if out_flag['sku'] in out_sku.keys():
                            out_sku[sku] = out_sku[sku] + out_flag['flag']
                        else:
                            out_sku[sku] = out_flag['flag']

        sku_filter = [key for key, value in out_sku.items() if not value == 0 and key not in unchecked_sku]
        ret = json.dumps({'sku':sku_filter})
        return ret

    except Exception as e:
        error = json.dumps({'error':'no sku'})
        return error

    finally:
        cur.close()
        con.close()


def count_flag(plat, sku, status):
    flag = ''
    if status.encode('UTF-8') == '停产':
        flag = 0
    elif status.encode('UTF-8') == '停售':
        if plat == 'ebay':
            flag = 0
        elif plat == 'aliexpress':
            flag = 0
        elif plat == 'shopee':
            flag = 1
        elif plat == 'wish':
            flag = 1
        elif plat == 'amazon11':
            flag = 1

    elif status.encode('UTF-8') == '清仓':
        if plat == 'ebay':
            flag = 0
        elif plat == 'wish':
            flag = 1
        elif plat == 'amazon11':
            flag = 1
        elif plat == 'aliexpress':
            flag = 0
        elif plat == 'shopee':
            flag = 1
    elif status.encode('UTF-8') == '线上清仓':
        if plat == 'ebay':
            flag = 0
        elif plat == 'aliexpress':
            flag = 0
        elif plat == 'shopee':
            flag = 1
        elif plat == 'wish':
            flag = 1
        elif plat == 'amazon11':
            flag = 1

    return {'sku': sku, 'flag': flag}


if __name__ == '__main__':

    print filter_sku()
