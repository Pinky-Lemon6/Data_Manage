import pygraphviz as pgv
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
            entity_list = ["student", "staff", "course", "notice", "college", "finicialOrder", "dormitory"] # entity_list存放所有的实体名称

            entity_dict = { # entity_dict存放实体属性
                "student": [
                    "student_id",
                    "student_name",
                    "student_gender",
                    "student_age",
                    "student_major",
                    "student_college",
                ], 
                "staff": [
                    "staff_id",
                    "staff_name",
                    "staff_title",
                    "staff_department",
                    "staff_college",
                    "staff_position",
                ], 
                "course": [
                    "course_id",
                    "course_name",
                    "course_credit_hours",
                    "course_staff_id",
                ], 
                "notice": [
                    "notice_id",
                    "notice_title",
                    "notice_content",
                    "notice_publish_date",
                    "notice_staff_id",
                ], 
                "college": [
                    "college_id",
                    "college_name",
                    "college_president",
                ], 
                "finicialOrder": [
                    "forder_id",
                    "forder_payer",
                    "forder_amount",
                    "forder_status",
                ], 
                "dormitory": [
                    "dorm_id",
                    "dorm_building",
                    "dorm_room_number",
                    "dorm_capacity",
                    "dorm_student_id"
                ],
            }

            associations = [ # associations存放实体间联系
                {
                    "association": "attend",
                    "entity1": "student", 
                    "entity1_nbr": "m",
                    "entity2": "course",
                    "entity2_nbr": "n"
                },
                {
                    "association": "tuition",
                    "entity1": "staff", 
                    "entity1_nbr": "n",
                    "entity2": "course",
                    "entity2_nbr": "1"
                },
                {
                    "association": "work for",
                    "entity1": "staff", 
                    "entity1_nbr": "m",
                    "entity2": "college",
                    "entity2_nbr": "n"
                },
                {
                    "association": "live",
                    "entity1": "student", 
                    "entity1_nbr": "1",
                    "entity2": "dormitory",
                    "entity2_nbr": "n"
                }
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
        self.create_er_graph(
            entity_list, entity_dict, associations, self.output_dir, self.output_name
        )


if __name__ == "__main__":
    # 测试
    while(1):
        time.sleep(60)
        print("*"*100)
        print("*"*100)
        print("*"*100)
        content = """现在有这样一个微人大学校事务管理系统的数据库：
        我们希望构建的实体主要有学生、教职工、课程、通知、学院、财务订单、宿舍、职务，请你自己补充以上实体所需要的属性数据以及实体间的联系，要求尽可能详细。"""
        output_dir = "D:\\py_code\\study"
        output_name = "test"
        worker = ERDiagramGenerator(
            content=content, output_dir=output_dir, output_name=output_name
        )
        worker.work()
