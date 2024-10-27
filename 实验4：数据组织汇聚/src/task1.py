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


def format_OutpatientData(ret):
    columns = ["医院名","门诊ID","病患姓名","病患身份证号","就诊日期","就诊时间",
               "就诊科室","诊断结果","医生ID","医生姓名","处方信息","诊疗费用",]
    ret = pd.DataFrame(ret)
    ret = ret[columns]
    ret = ret.fillna("")
    return ret

def OutpatientData_A():
    OutpatientData_A = {
        "医院名": "医院名", # 计算
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

    data_dir = os.path.join(current_directory, "../data/医院A/OutpatientData.csv")
    data = pd.read_csv(data_dir)
    data["医院名"] = "医院A"
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in OutpatientData_A.keys():
        reflact_col = OutpatientData_A[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    
    ret = format_OutpatientData(ret)
    return ret

def OutpatientData_B():
    """B需要将OutpatientData与DoctorInfoData做join"""
    OutpatientData_B = {
        "医院名": "医院名", # 计算
        "门诊ID": None,
        "病患姓名": "病人姓名",
        "病患身份证号": "病人身份证号",
        "就诊日期": "就诊日期", # 计算
        "就诊时间": "就诊时间", # 计算
        "就诊科室": "所属科室", # join
        "诊断结果": "病因",
        "医生ID": "医生ID", 
        "医生姓名": "医生姓名",  # join
        "处方信息": "处方信息", 
        "诊疗费用": "医疗费用", 
    }

    data_dir = os.path.join(current_directory, "../data/医院B/OutpatientData.csv")
    datasub_dir = os.path.join(current_directory, "../data/医院B/DoctorInfoData.csv")
    data = pd.read_csv(data_dir)
    datasub = pd.read_csv(datasub_dir)
    data = pd.merge(data, datasub, on="医生ID", how="left")
    data["医院名"] = "医院B"
    data["就诊日期"] = data["就诊时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%Y-%m-%d")
        )
    data["就诊时间"] = data["就诊时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%H:%M")
        )

    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in OutpatientData_B.keys():
        reflact_col = OutpatientData_B[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_OutpatientData(ret)
    return ret
    

def format_InpatientData(ret):
    columns = ["医院名","住院ID","病患姓名","病患身份证号","入院日期","出院日期",
               "住院时间","诊断结果","负责科室","医生ID","医生姓名","住院费用",]
    ret = pd.DataFrame(ret)
    ret = ret[columns]
    ret = ret.fillna("")
    return ret

def InpatientData_A():
    InpatientData_A = {
        "医院名": "医院名", # 计算
        "住院ID": "住院ID",
        "病患姓名": "姓名",
        "病患身份证号": "身份证号",
        "入院日期": "入院日期",
        "出院日期": "出院日期",
        "住院时间": "住院时间", # 计算
        "诊断结果": "诊断结果",
        "负责科室": "科室",
        "医生ID": "主治医生ID",
        "医生姓名": "主治医生姓名",
        "住院费用": "医疗费用",
    }

    data_dir = os.path.join(current_directory, "../data/医院A/InpatientData.csv")
    data = pd.read_csv(data_dir)
    data["医院名"] = "医院A"
    data["住院时间"] = data[["入院日期", "出院日期"]].apply(
        lambda x: ((datetime.strptime(x["出院日期"], "%Y-%m-%d"))
                   -(datetime.strptime(x["入院日期"], "%Y-%m-%d"))).days,
        axis=1
        )
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in InpatientData_A.keys():
        reflact_col = InpatientData_A[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_InpatientData(ret)
    return ret
    
def InpatientData_B():
    InpatientData_B = {
        "医院名": "医院名", # 计算
        "住院ID": "",
        "病患姓名": "病人姓名",
        "病患身份证号": "病人身份证号",
        "入院日期": "入院日期",
        "出院日期": "出院日期",
        "住院时间": "住院时间",
        "诊断结果": "病因",
        "负责科室": "所属科室", # join
        "医生ID": "医生ID",
        "医生姓名": "医生姓名", # join
        "住院费用": "住院费用",
    }

    data_dir = os.path.join(current_directory, "../data/医院B/InpatientData.csv")
    datasub_dir = os.path.join(current_directory, "../data/医院B/DoctorInfoData.csv")
    data = pd.read_csv(data_dir)
    datasub = pd.read_csv(datasub_dir)
    data = pd.merge(data, datasub, on="医生ID", how="left")
    data["医院名"] = "医院B"
    
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in InpatientData_B.keys():
        reflact_col = InpatientData_B[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_InpatientData(ret)
    return ret

def format_ExaminationData(ret):
    columns = ["医院名","检查ID","病患姓名","病患身份证号","日期","时间","类型",
               "费用","医生ID","医生姓名",]
    ret = pd.DataFrame(ret)
    ret = ret[columns]
    ret = ret.fillna("")
    return ret

def ExaminationData_A():
    ExaminationData_A = {
        "医院名": "医院名", # 计算
        "检查ID": "检查ID",
        "病患姓名": "检查人姓名",
        "病患身份证号": "检查人身份证号",
        "日期": "检查日期",
        "时间": "检查时间",
        "类型": "检查类型",
        "费用": "检查费用",
        "医生ID": "负责医生ID",
        "医生姓名": "负责医生姓名",
    }

    data_dir = os.path.join(current_directory, "../data/医院A/ExaminationData.csv")
    data = pd.read_csv(data_dir)
    data["医院名"] = "医院A"
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in ExaminationData_A.keys():
        reflact_col = ExaminationData_A[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_ExaminationData(ret)
    return ret

def ExaminationData_B():
    ExaminationData_B = {
        "医院名": "医院名", # 计算
        "检查ID": "",
        "病患姓名": "患者姓名",
        "病患身份证号": "身份证号",
        "日期": "日期", # 计算
        "时间": "时间", # 计算
        "类型": "检查类型",
        "费用": "检查费用",
        "医生ID": "医生ID",
        "医生姓名": "医生姓名", # join
    }

    data_dir = os.path.join(current_directory, "../data/医院B/ExaminationData.csv")
    datasub_dir = os.path.join(current_directory, "../data/医院B/DoctorInfoData.csv")
    data = pd.read_csv(data_dir)
    datasub = pd.read_csv(datasub_dir)
    data = pd.merge(data, datasub, on="医生ID", how="left")
    data["医院名"] = "医院B"
    data["日期"] = data["检查时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%Y-%m-%d")
        )
    data["时间"] = data["检查时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%H:%M")
        )
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in ExaminationData_B.keys():
        reflact_col = ExaminationData_B[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_ExaminationData(ret)
    return ret

def format_ExpenseData(ret):
    columns = ["医院名","费用ID","患者姓名","患者身份证号",
               "缴费日期","缴费时间","费用类型","金额",]
    ret = pd.DataFrame(ret)
    ret = ret[columns]
    ret = ret.fillna("")
    return ret

def ExpenseData_A():
    ExpenseData_A = {
        "医院名": "医院名", # 计算
        "费用ID": "费用ID",
        "患者姓名": "患者姓名",
        "患者身份证号": "患者身份证号",
        "缴费日期": "缴费日期",
        "缴费时间": "缴费时间",
        "费用类型": "费用类型",
        "金额": "金额",
    }

    data_dir = os.path.join(current_directory, "../data/医院A/ExpenseData.csv")
    data = pd.read_csv(data_dir)
    data["医院名"] = "医院A"
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in ExpenseData_A.keys():
        reflact_col = ExpenseData_A[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_ExpenseData(ret)
    return ret

def ExpenseData_B():
    ExpenseData_B = {
        "医院名": "医院名", # 计算
        "费用ID": "",
        "患者姓名": "病人姓名",
        "患者身份证号": "病人身份证号",
        "缴费日期": "缴费日期", # 计算
        "缴费时间": "缴费时间", # 计算
        "费用类型": "费用类型",
        "金额": "金额",
    }

    data_dir = os.path.join(current_directory, "../data/医院B/ExpenseData.csv")
    data = pd.read_csv(data_dir)
    data["医院名"] = "医院B"
    data["缴费日期"] = data["缴费时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%Y-%m-%d")
        )
    data["缴费时间"] = data["缴费时间"].apply(
        lambda x: datetime.strftime(datetime.strptime(x, "%Y-%m-%d %H:%M"), "%H:%M")
        )
    
    len = data.shape[0]
    columns = data.columns.to_list()

    ret = {}
    for column in ExpenseData_B.keys():
        reflact_col = ExpenseData_B[column]
        if reflact_col in columns:
            ret[column] = data[reflact_col]
        else:
            ret[column] = [""]*len
    ret = format_ExpenseData(ret)
    return ret

def main():
    OutpatientDataA = OutpatientData_A()
    OutpatientDataB = OutpatientData_B()
    OutpatientData = pd.concat([OutpatientDataA, OutpatientDataB], axis=0)
    print("*"*100)
    print(OutpatientData)
    InpatientDataA = InpatientData_A()
    InpatientDataB = InpatientData_B()
    InpatientData = pd.concat([InpatientDataA, InpatientDataB], axis=0)
    print("*"*100)
    print(InpatientData)
    print("*"*100)
    ExaminationDataA = ExaminationData_A()
    ExaminationDataB = ExaminationData_B()
    ExaminationData = pd.concat([ExaminationDataA, ExaminationDataB], axis=0)
    print(ExaminationData)
    print("*"*100)
    ExpenseDataA = ExpenseData_A()
    ExpenseDataB = ExpenseData_B()
    ExpenseData = pd.concat([ExpenseDataA, ExpenseDataB], axis=0)
    print(ExpenseData)
    output_dir = os.path.join(current_directory, "../output")
    OutpatientData.to_csv(os.path.join(output_dir, "OutpatientData.csv"), index=False)
    InpatientData.to_csv(os.path.join(output_dir, "InpatientData.csv"), index=False)
    ExaminationData.to_csv(os.path.join(output_dir, "ExaminationData.csv"), index=False)
    ExpenseData.to_csv(os.path.join(output_dir, "ExpenseData.csv"), index=False)

if __name__ == "__main__":
    main()