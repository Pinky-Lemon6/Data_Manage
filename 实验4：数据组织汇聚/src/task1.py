# **************************************************
# output:
#  门诊数据表 (`OutpatientData`)
# | 属性名          | 数据类型   | 示例数据             |
# |-----------------|------------|----------------------|
# | 医院名          | TEXT    | 医院A              |
# | 门诊ID          | VARCHAR    | OP12345              |
# | 病患姓名          | VARCHAR    | 张晓明               |
# | 病患身份证号    | VARCHAR    | 430221 19930809 8118 |
# | 就诊日期        | DATE       | 2023-06-15           |
# | 就诊时间        | TIME       | 20:33           |
# | 就诊科室            | VARCHAR    | 内科                 |
# | 诊断结果            | VARCHAR    | 上呼吸道感染         |
# | 医生ID          | VARCHAR    | D001                 |
# | 医生姓名      | VARCHAR    | 王萧                 |
# | 处方信息        | TEXT       | 阿莫西林 500mg*3天   |
# | 诊疗费用        | DECIMAL    | 150.00               |

#  住院数据表 (`InpatientData`)
# | 属性名          | 数据类型   | 示例数据             |
# |-----------------|------------|----------------------|
# | 医院名          | TEXT    | 医院A              |
# | 住院ID          | VARCHAR    | IP12345              |
# | 病患姓名          | VARCHAR    | 张晓明               |
# | 病患身份证号          | VARCHAR    | 430221 19930809 8118 |
# | 入院日期        | DATE       | 2023-06-10           |
# | 出院日期        | DATE       | 2023-06-20           |
# | 住院时间        | INT       | 10           |
# | 诊断结果            | VARCHAR    | 肺炎                 |
# | 负责科室            | VARCHAR    | 内科                 |
# | 医生ID      | VARCHAR    | D002                 |
# | 医生姓名      | VARCHAR    | 王萧                 |
# | 住院费用        | DECIMAL    | 5000.00              |

#  检查数据表 (`ExaminationData`)
# | 属性名          | 数据类型   | 示例数据             |
# |-----------------|------------|----------------------|
# | 医院名          | TEXT    | 医院A              |
# | 检查ID          | VARCHAR    | EX12345              |
# | 病患姓名          | VARCHAR    | 张晓明               |
# | 病患身份证号    | VARCHAR    | 430221 19930809 8118 |
# | 日期        | DATE       | 2023-06-12           |
# | 时间        | TIME       | 20:33           |
# | 类型        | VARCHAR    | 血液检查             |
# | 费用        | DECIMAL    | 50.00              |
# | 医生ID      | VARCHAR    | D002                 |
# | 医生姓名      | VARCHAR    | 王萧                 |

#  费用数据表 (`ExpenseData`)
# | 属性名          | 数据类型   | 示例数据             |
# |-----------------|------------|----------------------|
# | 医院名          | TEXT    | 医院A              |
# | 费用ID          | VARCHAR    | EXP12345             |
# | 患者姓名          | VARCHAR    | 张晓明               |
# | 患者身份证号          | VARCHAR    | 430221 19930809 8118 |
# | 缴费日期        | DATE       | 2023-06-15           |
# | 缴费时间        | TIME       | 20:33           |
# | 费用类型        | VARCHAR    | 药品费               |
# | 金额            | DECIMAL    | 100.00               |
# **************************************************


import pandas as pd
import os
from datetime import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
OutpatientData_A = {
    "医院名": None,
    "门诊ID": "就诊ID",
    "病患姓名": "患者姓名",
    "病患身份证号": "患者身份证号",
    "就诊日期": "就诊日期",
    "就诊时间": "就诊时间",
    "就诊科室": "科室",
    "诊断结果": "诊断结果",
    "医生ID": "医生ID", 
    "医生姓名": "医生姓名", 
    "处方信息": "处方信息", 
    "诊疗费用": "医疗费用", 
}
OutpatientData_B = {
    "医院名": None,
    "门诊ID": None,
    "病患姓名": "病人姓名",
    "病患身份证号": "病人身份证号",
    "就诊日期": "就诊日期",
    "就诊时间": "就诊时间",
    "就诊科室": None,
    "诊断结果": "病因",
    "医生ID": "医生ID", 
    "医生姓名": None, 
    "处方信息": "处方信息", 
    "诊疗费用": "医疗费用", 
}



def OutpatientData(hospital_code, reflact_OutpatientData):
    ret = {}
    data_dir = os.path.join(current_directory, f"../data/医院{hospital_code}/OutpatientData.csv")
    data = pd.read_csv(data_dir)
    if hospital_code == "B":
        data["就诊日期"] = data["就诊时间"].apply(lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%Y-%m-%d"))
        data["就诊时间"] = data["就诊时间"].apply(lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%H:%M"))

    len = data.shape[0]
    data_columns = data.columns.to_list()
    for column in reflact_OutpatientData.keys():
        if reflact_OutpatientData[column] in data_columns:
            ret[column] = data[reflact_OutpatientData[column]]
        else:
            ret[column] = [""]*len
    ret["医院名"] = [f"医院{hospital_code}"]*len
    return ret
    

def InpatientData(hospital_code):
    pass

def ExaminationData(hospital_code):
    pass

def ExpenseData(hospital_code):
    pass

def main():
    print("*"*100)
    test = pd.DataFrame(OutpatientData("A", reflact_OutpatientData=OutpatientData_A))
    print(test.head(1).T)
    print("")
    print(test.dtypes)
    print("*"*100)
    test = pd.DataFrame(OutpatientData("B", reflact_OutpatientData=OutpatientData_B))
    print(test.head(1).T)
    print("")
    print(test.dtypes)



if __name__ == "__main__":
    main()