from array import array
from datetime import datetime

import akshare as ak
import numpy
import numpy as np

from bigan_data.db.PostgresqlAdapter import PostgresqlAdapter
from bigan_data.math.GreyRelationAnalyzer import GreyRelationAnalyzer
from bigan_data.model.AKShareSyncModel import get_akshare_stock_info_a_code_name, get_akshare_stock_zh_a_hist
from bigan_data.model.AKShareSyncModelClean import clean_akshare_stock_info_a_code_name
from bigan_data.model.GreyResult import GreyRelationAnalyzerResMonthly


def cal_relation(calculate_range: int):
    array = stock_zh_index_daily_em_df["close"].to_numpy()
    time_arr = stock_zh_index_daily_em_df["date"].to_numpy()
    # array = array[:-5]
    # time_arr = time_arr[:-5]
    arr_len = len(array)
    cal = list()
    for i in range(arr_len - 1):
        cal.append(array[i])
    # calculate range 20
    arr_len = arr_len - 1
    reference_seq = list()
    for i in range(arr_len - calculate_range, arr_len):
        reference_seq.append(cal[i])
    gra = GreyRelationAnalyzer(resolution_factor=0.5, reference_seq=reference_seq)
    for i in range(arr_len - calculate_range):
        sub_seq = cal[i:i + calculate_range]
        gra.add_analysis_seq(sub_seq)
    res = gra.analysis_res()
    # print(res)
    max_index = np.argmax(res)
    max_val = np.max(res)
    print("--------------------------")
    print("calculate_range:", calculate_range)
    print("max_index:", max_index, ",max_val:", max_val)
    print(time_arr[max_index + calculate_range - 1])


def cal_similarity(dataFrame, code: str, pg: PostgresqlAdapter):
    ## clean
    sql = "delete from akshare_stock_info_a_code_name where code = \'" + code + "\'"
    pg.execute(sql)
    # get data
    close_val_arr = dataFrame["close"].to_numpy()
    time_arr = dataFrame["date"].to_numpy()
    index_val_dict = {}
    for i in range(len(close_val_arr)):
        time_val = time_arr[i].replace("-", "")
        index_val_dict[time_val] = i

    trade_date_dict = get_trade_date_dict()
    analysis_ym = []
    analysis_ym_dict = {}
    analysis_ym_index = 0
    for year in range(2017, 2024):
        for month in range(1, 13):
            ym_str = str(year) + str(month).rjust(2, '0')
            analysis_ym.append(ym_str)
            analysis_ym_dict[ym_str] = analysis_ym_index
            analysis_ym_index = analysis_ym_index + 1
    for year in range(2019, 2024):
        for month in range(1, 13):
            if year == 2023 and month >= 8:
                break
            ym_str = str(year) + str(month).rjust(2, '0')
            trade_date_arr = trade_date_dict[ym_str]
            curr_month_trade_day_len = len(trade_date_arr)
            reference_seq = []
            trade_date_last = trade_date_arr[len(trade_date_arr) - 1]
            close_val_arr_last_index = index_val_dict.get(trade_date_last)
            for i in range(close_val_arr_last_index - curr_month_trade_day_len, close_val_arr_last_index + 1):
                reference_seq.append(close_val_arr[i])
            gra = GreyRelationAnalyzer(resolution_factor=0.5, reference_seq=reference_seq)
            analysis_ym_index = analysis_ym_dict.get(ym_str)
            for analysis_index in range(0, analysis_ym_index):
                analysis_ym_val = analysis_ym[analysis_index]
                analysis_ym_trade_date_arr = trade_date_dict[analysis_ym_val]
                analysis_seq = []
                analysis_ym_trade_date_arr_last = analysis_ym_trade_date_arr[len(analysis_ym_trade_date_arr) - 1]
                analysis_ym_trade_date_arr_last_index = index_val_dict.get(analysis_ym_trade_date_arr_last)
                for i in range(analysis_ym_trade_date_arr_last_index - curr_month_trade_day_len,
                               analysis_ym_trade_date_arr_last_index + 1):
                    analysis_seq.append(close_val_arr[i])
                gra.add_analysis_seq(analysis_seq)
            res = gra.analysis_res()

            res_list = res.copy()
            max_index_arr = np.argpartition(res_list, -5)[-5:].tolist()
            max_values = np.array(res_list)[max_index_arr].tolist()

            # get 1 2 3 4 5
            first_index = np.argmax(max_values)
            first_similarity = max_values[first_index]
            first_ym = analysis_ym[max_index_arr[first_index]]
            max_values.remove(first_similarity)
            max_index_arr.remove(max_index_arr[first_index])

            second_index = np.argmax(max_values)
            second_similarity = max_values[second_index]
            second_ym = analysis_ym[max_index_arr[second_index]]
            max_values.remove(second_similarity)
            max_index_arr.remove(max_index_arr[second_index])

            third_index = np.argmax(max_values)
            third_similarity = max_values[third_index]
            third_ym = analysis_ym[max_index_arr[third_index]]
            max_values.remove(third_similarity)
            max_index_arr.remove(max_index_arr[third_index])

            fourth_index = np.argmax(max_values)
            fourth_similarity = max_values[fourth_index]
            fourth_ym = analysis_ym[max_index_arr[fourth_index]]
            max_values.remove(fourth_similarity)
            max_index_arr.remove(max_index_arr[fourth_index])

            fifth_index = np.argmax(max_values)
            fifth_similarity = max_values[fifth_index]
            fifth_ym = analysis_ym[max_index_arr[fifth_index]]
            max_values.remove(fifth_similarity)
            max_index_arr.remove(max_index_arr[fifth_index])

            greyRelationAnalyzerResMonthly = GreyRelationAnalyzerResMonthly()
            greyRelationAnalyzerResMonthly.code = code
            greyRelationAnalyzerResMonthly.current_month = ym_str
            greyRelationAnalyzerResMonthly.result_month = first_ym
            greyRelationAnalyzerResMonthly.similarity = first_similarity
            greyRelationAnalyzerResMonthly.result_month1 = first_ym
            greyRelationAnalyzerResMonthly.similarity1 = first_similarity
            greyRelationAnalyzerResMonthly.result_month2 = second_ym
            greyRelationAnalyzerResMonthly.similarity2 = second_similarity
            greyRelationAnalyzerResMonthly.result_month3 = third_ym
            greyRelationAnalyzerResMonthly.similarity3 = third_similarity
            greyRelationAnalyzerResMonthly.result_month4 = fourth_ym
            greyRelationAnalyzerResMonthly.similarity4 = fourth_similarity
            greyRelationAnalyzerResMonthly.result_month5 = fifth_ym
            greyRelationAnalyzerResMonthly.similarity5 = fifth_similarity
            greyRelationAnalyzerResMonthly.all_res = str(res_list)
            pg.add_entity(greyRelationAnalyzerResMonthly)


def get_trade_date_dict():
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    time_arr = tool_trade_date_hist_sina_df["trade_date"].to_numpy()
    res_dict = {}
    for i in range(len(time_arr)):
        curr_date = time_arr[i].strftime("%Y%m%d")
        curr_date_ym = curr_date[0:6].replace("-", "")
        arr = res_dict.get(curr_date_ym)
        if arr is None:
            arr = []
        arr.append(curr_date)
        res_dict[curr_date_ym] = arr
    return res_dict


if __name__ == '__main__':
    postgresqlAdapter = PostgresqlAdapter()
    # print("test")
    # start_date = "20230101"
    # today = datetime.today().strftime('%Y%m%d')
    # print(today)
    # pg = PostgresqlAdapter()
    # clean_akshare_stock_info_a_code_name(pg, today)
    # stocks = get_akshare_stock_info_a_code_name()
    # #pg.add_entities(stocks)
    # for stock in stocks:
    #     stock_zh_a_hist = get_akshare_stock_zh_a_hist(stock.code, start_date, today)
    #     print(stock_zh_a_hist)
    #     pg.add_entities(stock_zh_a_hist)
    # stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol="sh000001")
    # print(stock_zh_index_daily_tx_df)

    # gra = GreyRelationAnalyzer(reference_seq=[1988, 2062, 2335, 2750, 3356, 3806])
    # gra.add_analysis_seq([386, 408, 422, 482, 511, 561])
    # gra.add_analysis_seq([839, 846, 960, 1258, 1577, 1893])
    # gra.add_analysis_seq([763, 808, 953, 1010, 1268, 1352])
    # print( gra.analysis_res())
    symbol = "sz399106"
    stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol=symbol, start_date="20170101",
                                                            end_date="20230831")

    cal_similarity(stock_zh_index_daily_em_df, symbol, postgresqlAdapter)
    # stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sh000001")
    # for range_val in range(5, 41):
    #     cal_relation(range_val)
