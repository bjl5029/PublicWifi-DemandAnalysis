import schedule
import time
import requests
import pandas as pd


def main_job():
    param_list = pd.read_excel("./params.xlsx", header=None).iloc[:, 0].tolist()
    kor_param_list = pd.read_excel("./params.xlsx", header=None).iloc[:, 1].tolist()
    param_index = [1, 3, 4, 6, 7, 18, 19, 21]
    param_list = [param_list[index - 1] for index in param_index]
    kor_param_list = [kor_param_list[index - 1] for index in param_index]

    name_list = pd.read_excel("./loc.xlsx")["AREA_NM"].tolist()

    for name in name_list:
        print(name_list.index(name))

        try:
            file_path = f"./output/{name}.csv"
            temp_df = pd.read_csv(file_path, encoding='euc-kr')
        except:
            columns = [
                "핫스팟 장소명", "실시간 인구현황", "장소 혼잡도 지표", "실시간 인구 지표 최소값",
                "실시간 인구 지표 최대값", "상주 인구 비율", "비상주 인구 비율", "실시간 인구 데이터 업데이트 시간"
            ]
            temp_df = pd.DataFrame(columns=columns)

        url = f"http://openapi.seoul.go.kr:8088/5974435479626a6c36305765436673/json/citydata_ppltn/1/5/{name}"
        response = requests.get(url).json()

        extracted_data = {}
        for key in param_list:
            extracted_data[key] = response['SeoulRtd.citydata_ppltn'][0].get(key, None)

        key_map = dict(zip(param_list, kor_param_list))

        transformed_dict = {
            key_map.get(k, k): v for k, v in extracted_data.items()
        }

        temp_df = pd.concat([temp_df, pd.DataFrame([transformed_dict])], ignore_index=True)

        temp_df.to_csv(f"./output/{name}.csv", index=False, encoding='euc-kr')


schedule.every(30).minutes.do(main_job)

main_job()

while True:
    schedule.run_pending()
    time.sleep(1)
