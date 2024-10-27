import json
# import pygraphviz as pgv
import os
import re
import ast
import time


from openai import OpenAI


class ERDiagramGenerator:
    """
    自动生成ER图
    params:
        content: 接受实际的需求
    """

    def __init__(self, content, output_dir, output_name):
        self.content = content
        self.output_dir = output_dir
        self.output_name = output_name

    def generate_prompt(self):
        suffix = """
            请将上面这段文字整理成如下er图信息表（注意，下面的代码仅提供格式信息，你不要学习下面代码中的属性、联系等信息python代码）：
            entity_list = [
                "hospital",
                "patient",
                "doctor",
                "outpatientdata",
                "inpatientdata",
                "examinationdata",
                "expensedata"
            ]  # entity_list存放所有的实体名称

            entity_dict = {  # entity_dict存放实体属性
            "hospital": [
                "hospital_name",
            ],
            "patient": [
                "patient_name",
                "patient_id_number",
            ],
            "doctor": [
                "doctor_id",
                "doctor_name",
            ],
            "outpatientdata": [
                "outpatient_id",
                "visit_date",
                "visit_time",
                "department",
                "diagnosis",
                "prescription",
                "treatment_cost",
            ],
            "inpatientdata": [
                "inpatient_id",
                "admission_date",
                "discharge_date",
                "hospitalization_days",
                "diagnosis",
                "department_in_charge",
                "hospitalization_cost",
            ],
            "examinationdata": [
                "examination_id",
                "examination_date",
                "examination_time",
                "examination_type",
                "cost",
            ],
            "expensedata": [
                "expense_id",
                "payment_date",
                "payment_time",
                "expense_type",
                "amount",
            ],
        }

        associations = [  # associations存放实体间联系
            {
                "association": "has",
                "entity1": "hospital", 
                "entity1_nbr": "1",
                "entity2": "outpatientdata",
                "entity2_nbr": "n"
            },
            {
                "association": "has",
                "entity1": "hospital", 
                "entity1_nbr": "1",
                "entity2": "inpatientdata",
                "entity2_nbr": "n"
            },
            {
                "association": "has",
                "entity1": "hospital", 
                "entity1_nbr": "1",
                "entity2": "examinationdata",
                "entity2_nbr": "n"
            },
            {
                "association": "has",
                "entity1": "hospital", 
                "entity1_nbr": "1",
                "entity2": "expensedata",
                "entity2_nbr": "n"
            },
            {
                "association": "belongs_to",
                "entity1": "patient", 
                "entity1_nbr": "1",
                "entity2": "outpatientdata",
                "entity2_nbr": "1"
            },
            {
                "association": "belongs_to",
                "entity1": "patient", 
                "entity1_nbr": "1",
                "entity2": "inpatientdata",
                "entity2_nbr": "1"
            },
            {
                "association": "belongs_to",
                "entity1": "patient", 
                "entity1_nbr": "1",
                "entity2": "examinationdata",
                "entity2_nbr": "n"
            },
            {
                "association": "belongs_to",
                "entity1": "patient", 
                "entity1_nbr": "1",
                "entity2": "expensedata",
                "entity2_nbr": "n"
            },
            {
                "association": "prescribe",
                "entity1": "doctor", 
                "entity1_nbr": "1",
                "entity2": "outpatientdata",
                "entity2_nbr": "n"
            },
            {
                "association": "prescribe",
                "entity1": "doctor", 
                "entity1_nbr": "1",
                "entity2": "inpatientdata",
                "entity2_nbr": "1"
            },
            {
                "association": "prescribe",
                "entity1": "doctor", 
                "entity1_nbr": "1",
                "entity2": "examinationdata",
                "entity2_nbr": "n"
            },
        ]
        """
        ret = self.content + suffix
        return ret

    def get_LLM_response(self, q):
        """
        根据content的内容，获取大模型的返回值
        params:
            q: 输入给大模型的问题
        """
        # API Key
        api_key = "sk-tp0PvDsgccr8HRRHKXOCC9m5yQv9t2ifQJJoTs0PrfiLtpTd"

        # 初始化 OpenAI 客户端
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
        )

        # 计时
        now = time.time()
        # 发送请求到 Kimi API
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",  # 使用的模型
            messages=[{"role": "user", "content": q}],  # 只包含用户的消息
            temperature=0.3,  # 控制输出的随机性
        )

        ret = completion.choices[0].message.content
        print("*"*50)
        print(f"time cost: {time.time()-now}")
        print(ret)
        print("*"*50)
        return ret

    def analysis_model_output(self, ret):
        """
        将大模型的输出结果解析成三个list
        """
        # 移除注释和多余的空格
        ret = re.sub(r'#.*', '', ret)  # 移除注释
        ret = re.sub(r'\s+', ' ', ret)  # 移除多余的空白字符
        entity_list = []
        entity_dict = {}
        associations = []

        # 提取并解析 entity_list
        entity_list_match = re.search(r"entity_list = \[(.*?)\]", ret, re.DOTALL)
        if entity_list_match:
            entity_list_str = entity_list_match.group(1).strip()
        entity_list = ast.literal_eval("[" + entity_list_str + "]")

        # 提取并解析 entity_dict
        entity_dict_match = re.search(r"entity_dict = {(.*?)}", ret, re.DOTALL)
        if entity_dict_match:
            entity_dict_str = entity_dict_match.group(1).strip()
        entity_dict = ast.literal_eval("{" + entity_dict_str + "}")

        # 提取并解析 associations
        associations_match = re.search(r"associations = \[(.*?)\]", ret, re.DOTALL)
        if associations_match:
            associations_str = associations_match.group(1).strip()
        associations = ast.literal_eval("[" + associations_str + "]")
        
        
        return entity_list, entity_dict, associations
    

    def create_er_graph(
        self, entity_list, entity_dict, associations, output_dir, output_name
    ):
        G = pgv.AGraph(directed=False)
        for i in range(len(entity_list)):
            G.add_node(
                f"entity_{i}", shape="rectangle", label=entity_list[i]
            )  # 矩形实体
            tmp = entity_dict[entity_list[i]]
            for j in range(len(tmp)):
                G.add_node(
                    f"attribute_{entity_list[i]}_{j}",
                    shape="rectangle",
                    style="rounded",
                    label=tmp[j],
                )
                G.add_edge(f"entity_{i}", f"attribute_{entity_list[i]}_{j}")

        for i in range(len(associations)):
            tmp = associations[i]
            G.add_node(
                f"relationship_{i}", shape="diamond", label=tmp["association"]
            )  # 菱形关系
            index_entity1 = entity_list.index(tmp["entity1"])
            index_entity2 = entity_list.index(tmp["entity2"])
            G.add_edge(
                f"entity_{index_entity1}", f"relationship_{i}", label=tmp["entity1_nbr"]
            )
            G.add_edge(
                f"entity_{index_entity2}", f"relationship_{i}", label=tmp["entity2_nbr"]
            )

        G.graph_attr.update(
            label="ER Diagram Example",
            fontsize="12",
            fontcolor="black",
            fontname="Arial",
            rankdir="TB",
        )  # TB 表示自顶向下布局
        G.graph_attr.update(
            overlap="false",  # 关闭节点重叠
            splines="true",  # 启用曲线边
            rankdir="TB",  # 指定布局方向
            ranksep=".2",  # 节点间的垂直距离
            nodesep=".1",  # 边上的点之间的水平距离
            fontsize=10,  # 字体大小
            fontname="Arial",  # 字体名称
        )
        output_name = os.path.join(output_dir, output_name)
        G.draw(f"{output_name}.png", prog="sfdp")

    def work(self):
        # 生成大模型输入
        q = self.generate_prompt()
        # 获取大模型返回结果
        ret = self.get_LLM_response(q)
        # 解析结果
        entity_list, entity_dict, associations = self.analysis_model_output(ret)
        
        # 画图
        # self.create_er_graph(
        #     entity_list, entity_dict, associations, self.output_dir, self.output_name
        # )
        # 结果修正
        dic ={
            "entity_list": entity_list,
            "entity_dict": entity_dict,
            "associations": associations
            }
        # 将dic保存在JSON中
        with open(f"{self.output_dir}\{'analysis'}.json", "w",encoding="utf-8") as f:
            json.dump(dic, f,ensure_ascii=False)
 
        input("press enter to continue...")
        # 重新从dic中读取
        with open(f"{self.output_dir}\{'analysis'}.json", "r") as f:
            dic = json.load(f)
        entity_list = dic["entity_list"]
        entity_dict = dic["entity_dict"]
        associations = dic["associations"]
        # 画图
        # self.create_er_graph(
        #     entity_list, entity_dict, associations, self.output_dir, self.output_name
        # )


if __name__ == "__main__":
    # 测试
    content = """现在有这样的一系列数据集，格式如下：
        门诊数据表 (`OutpatientData`)
        | 属性名          | 数据类型   | 示例数据             |
        |-----------------|------------|----------------------|
        | 医院名          | TEXT    | 医院A              |
        | 门诊ID          | VARCHAR    | OP12345              |
        | 病患姓名          | VARCHAR    | 张晓明               |
        | 病患身份证号    | VARCHAR    | 430221 19930809 8118 |
        | 就诊日期        | DATE       | 2023-06-15           |
        | 就诊时间        | TIME       | 20:33           |
        | 就诊科室            | VARCHAR    | 内科                 |
        | 诊断结果            | VARCHAR    | 上呼吸道感染         |
        | 医生ID          | VARCHAR    | D001                 |
        | 医生姓名      | VARCHAR    | 王萧                 |
        | 处方信息        | TEXT       | 阿莫西林 500mg*3天   |
        | 诊疗费用        | DECIMAL    | 150.00               |

        住院数据表 (`InpatientData`)
        | 属性名          | 数据类型   | 示例数据             |
        |-----------------|------------|----------------------|
        | 医院名          | TEXT    | 医院A              |
        | 住院ID          | VARCHAR    | IP12345              |
        | 病患姓名          | VARCHAR    | 张晓明               |
        | 病患身份证号          | VARCHAR    | 430221 19930809 8118 |
        | 入院日期        | DATE       | 2023-06-10           |
        | 出院日期        | DATE       | 2023-06-20           |
        | 住院时间        | INT       | 10           |
        | 诊断结果            | VARCHAR    | 肺炎                 |
        | 负责科室            | VARCHAR    | 内科                 |
        | 医生ID      | VARCHAR    | D002                 |
        | 医生姓名      | VARCHAR    | 王萧                 |
        | 住院费用        | DECIMAL    | 5000.00              |

        检查数据表 (`ExaminationData`)
        | 属性名          | 数据类型   | 示例数据             |
        |-----------------|------------|----------------------|
        | 医院名          | TEXT    | 医院A              |
        | 检查ID          | VARCHAR    | EX12345              |
        | 病患姓名          | VARCHAR    | 张晓明               |
        | 病患身份证号    | VARCHAR    | 430221 19930809 8118 |
        | 日期        | DATE       | 2023-06-12           |
        | 时间        | TIME       | 20:33           |
        | 类型        | VARCHAR    | 血液检查             |
        | 费用        | DECIMAL    | 50.00              |
        | 医生ID      | VARCHAR    | D002                 |
        | 医生姓名      | VARCHAR    | 王萧                 |

        费用数据表 (`ExpenseData`)
        | 属性名          | 数据类型   | 示例数据             |
        |-----------------|------------|----------------------|
        | 医院名          | TEXT    | 医院A              |
        | 费用ID          | VARCHAR    | EXP12345             |
        | 患者姓名          | VARCHAR    | 张晓明               |
        | 患者身份证号          | VARCHAR    | 430221 19930809 8118 |
        | 缴费日期        | DATE       | 2023-06-15           |
        | 缴费时间        | TIME       | 20:33           |
        | 费用类型        | VARCHAR    | 药品费               |
        | 金额            | DECIMAL    | 100.00               |
        | 医生ID      | VARCHAR    | D002                 |
        
        请你自己根据以上数据表的信息，帮我生成实体的属性数据以及实体间的联系，要求尽可能详细。"""
    output_dir = "..\output"
    output_name = "test"
    worker = ERDiagramGenerator(
        content=content, output_dir=output_dir, output_name=output_name
    )
    worker.work()
