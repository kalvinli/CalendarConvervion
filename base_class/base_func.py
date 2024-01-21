from baseopensdk.api.base.v1 import *
from baseopensdk import BaseClient
import time, json
from lunardate import LunarDate


###########################   批量公历农历互转   ###########################
def batch_convert_date_func(data: str):
  # print(data, flush=True)
  data_json = json.loads(data).get("parameters","")
  if data_json == '':
    return "参数错误"
  # print(data_json)

  APP_TOKEN = data_json.get("app_token")
  PERSONAL_BASE_TOKEN = data_json.get("personal_base_token")
  TABLE_ID = data_json.get("table_id")
  VIEW_ID = data_json.get("view_id")

  # 转换类型
  TYPE = data_json.get("type")

  # 源字段
  FIELD_SOURCE = data_json.get("field_source")

  # 目标字段
  FIELD_TARGET = data_json.get("field_target")
  FIELD_LUNAR_CN = ""

  LeapMonthList = { "1900": "8", "1903": "5", "1906": "4", "1909": "2", "1911": "6", "1914": "5", "1917": "2", "1919": "7", "1922": "5", "1925": "4", "1928": "2", "1930": "6", "1933": "5", "1936": "3", "1938": "7", "1941": "6", "1944": "4", "1947": "2", "1949": "7", "1952": "5", "1955": "3", "1957": "8", "1960": "6", "1963": "4", "1966": "3", "1968": "7", "1971": "5", "1974": "4", "1976": "8", "1979": "6", "1982": "4", "1984": "10", "1987": "6", "1990": "5", "1993": "3", "1995": "8", "1998": "5", "2001": "4", "2004": "2", "2006": "7", "2009": "5", "2012": "4", "2014": "9", "2017": "6", "2020": "4", "2023": "2", "2025": "6", "2028": "5", "2031": "3", "2033": "11", "2036": "6", "2039": "5", "2042": "2", "2044": "7", "2047": "5", "2050": "3", "2052": "8", "2055": "6", "2058": "4", "2061": "3", "2063": "7", "2066": "5", "2069": "4", "2071": "8", "2074": "6", "2077": "4", "2080": "3", "2082": "7", "2085": "5", "2088": "4", "2090": "8", "2093": "6", "2096": "4", "2099": "2" }
  nStr_day = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
  nStr_month = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]


  # print("=" * 30)

  # print(APP_TOKEN)
  # print(PERSONAL_BASE_TOKEN)
  # print(TABLE_ID)
  # print(VIEW_ID)
  # print(TYPE)

  # print(FIELD_SOURCE)
  # print(FIELD_TARGET)

  # print("=" * 30)


  # 1. 构建client
  client: BaseClient = BaseClient.builder() \
      .app_token(APP_TOKEN) \
      .personal_base_token(PERSONAL_BASE_TOKEN) \
      .build()

  # 获取【农历（中文）】字段
  try:
    create_field_request = CreateAppTableFieldRequest().builder() \
      .table_id(TABLE_ID) \
      .request_body(
        AppTableField.builder() \
          .field_name("农历（中文）") \
          .type(1) \
          .build()
      ) \
      .build()

    create_field_response = client.base.v1.app_table_field.create(
          create_field_request)
    FIELD_LUNAR_CN = "农历（中文）"
  except Exception as e:
    FIELD_LUNAR_CN = "农历（中文）"


  # 2. 遍历记录
  has_more = True
  page_token = ""


  while has_more:
    list_record_request = ListAppTableRecordRequest.builder() \
      .page_size(500) \
      .view_id(VIEW_ID) \
      .filter("") \
      .table_id(TABLE_ID) \
      .page_token(page_token) \
      .build()

    list_record_response = client.base.v1.app_table_record.list(
          list_record_request)
    records = getattr(list_record_response.data, 'items', [])

    has_more = list_record_response.data.has_more
    page_token = list_record_response.data.page_token
    total = list_record_response.data.total
    result = '成功转换 ' + str(total) + ' 条数据'

    # print(list_record_response.data.__dict__)

    # 如果字段列表为空时，执行清空整个视图的数据
    record_list = []
    for record_item in records:
      # print(record_item.__dict__, flush=True)
      # print("=" * 30)

      fields = record_item.fields
      # print(fields)
      # print(len(fields.items()), flush=True)

      field_list = {}
      for key, value in fields.items():
        if key == FIELD_SOURCE:   
          # print(str(key) + ':' + str(value))

          try:
            value = int(value)
          except Exception as e:
            value = value[0]

          # print(value)


          time_struct = time.gmtime(value / 1000 + 8 * 3600)
          date_time_Y = int(time.strftime('%Y', time_struct))
          date_time_M = int(time.strftime('%m', time_struct))
          date_time_D = int(time.strftime('%d', time_struct))


          timestamp = 0
          isLeapMonth = 0
          lunar_cn = ""
          if TYPE == "农历转公历":
            lunar_cn = fields.get(FIELD_LUNAR_CN, "")
            if "闰" in lunar_cn:
              isLeapMonth = 1

            lunar_date = str(LunarDate(date_time_Y, date_time_M, date_time_D, isLeapMonth).toSolarDate())
            timestamp = int(time.mktime(time.strptime(lunar_date,"%Y-%m-%d")))*1000

            if isLeapMonth == 1:
              lunar_cn = "闰" + nStr_month[date_time_M-1] + "月" + nStr_day[date_time_D-1]
            else:
              lunar_cn = nStr_month[date_time_M-1] + "月" + nStr_day[date_time_D-1]

          else:
            solar_date = LunarDate.fromSolarDate(date_time_Y, date_time_M, date_time_D)

            if solar_date.isLeapMonth:
                isLeapMonth = 1

            if isLeapMonth == 1:
              lunar_cn = "闰" + nStr_month[solar_date.month-1] + "月" + nStr_day[solar_date.day-1]
            else:
              lunar_cn = nStr_month[solar_date.month-1] + "月" + nStr_day[solar_date.day-1]

            solar_date = str(solar_date.year)+"-"+str(solar_date.month)+"-"+str(solar_date.day)
            timestamp = int(time.mktime(time.strptime(solar_date,"%Y-%m-%d")))*1000

          field_list[FIELD_TARGET] = timestamp
          field_list[FIELD_LUNAR_CN] = lunar_cn

      record_list.append({"fields": field_list, "record_id": record_item.record_id})

    # print(record_list)
    result = batch_update_record_func(APP_TOKEN, PERSONAL_BASE_TOKEN, TABLE_ID, record_list)

  # print(result, flush=True)
  return result


###########################   批量更新记录，按照每500条记录写入一次   ###########################
def batch_update_record_func(APP_TOKEN: str, PERSONAL_BASE_TOKEN : str, TABLE_ID: str, record_list: object):

  try:

    # 1. 构建client
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    step = 500
    for i in range(0, len(record_list), step):
      new_record_list = record_list[i:i + step]
      retry = 0
      while retry < 3:
        try:
          # 2. 批量保存
          batch_update_records_request = BatchUpdateAppTableRecordRequest().builder() \
          .table_id(TABLE_ID) \
          .request_body(
            BatchUpdateAppTableRecordRequestBody.builder() \
              .records(new_record_list) \
              .build()
          ) \
          .build()
          # print(batch_update_records_request.__dict__)

          batch_update_records_response = client.base.v1.app_table_record.batch_update(
              batch_update_records_request)
          # print(batch_update_records_response.__dict__)
          retry = 3
          result = "数据保存成功"
        except Exception as e:
          retry = retry + 1
          if retry == 3:
            result = "重试写入超过2次，数据操作失败，请检查网络！"
            raise "重试写入超过2次，数据操作失败，请检查网络！"

    return result

  except Exception as e:
    return "数据保存失败"
