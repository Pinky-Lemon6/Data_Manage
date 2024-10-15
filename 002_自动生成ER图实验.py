import pygraphviz as pgv
import os

class ERDiagramGenerator():
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
            请将上面这段文字整理成如下er图信息表（p，注意，下面的代码仅提供格式信息，你不要学习下面代码中的属性、联系等信息ython代码）：
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
        TODO: 调用大模型api得到答案
        """
        ret = ""
        return ret
    
    def analysis_model_output(self, ret):
        """
        将大模型的输出结果解析成三个list
        TODO: 代码未完成，现在是直接打印结果
        """
        entity_list = [
            "student", 
            "staff", 
            "course", 
            "notice", 
            "college", 
            "financial_order", 
            "dormitory"
        ]

        entity_dict = {
            "student": [
                "student_id",
                "student_name",
                "student_gender",
                "student_age",
                "student_major",
                "student_college",
                "student_phone",
                "student_email"
            ],
            "staff": [
                "staff_id",
                "staff_name",
                "staff_gender",
                "staff_age",
                "staff_title",
                "staff_department",
                "staff_college",
                "staff_position",
                "staff_phone",
                "staff_email"
            ],
            "course": [
                "course_id",
                "course_name",
                "course_description",
                "course_credit_hours",
                "course_teacher_id"
            ],
            "notice": [
                "notice_id",
                "notice_title",
                "notice_content",
                "notice_publish_date",
                "notice_publisher_id"
            ],
            "college": [
                "college_id",
                "college_name",
                "college_president",
                "college_location"
            ],
            "financial_order": [
                "order_id",
                "order_payer",
                "order_amount",
                "order_type",
                "order_status",
                "order_date",
                "order_student_id"
            ],
            "dormitory": [
                "dorm_id",
                "dorm_building",
                "dorm_room_number",
                "dorm_capacity",
                "dorm_occupancy"
            ]
        }

        associations = [
            {
                "association": "enroll_in",
                "entity1": "student",
                "entity1_nbr": "n",
                "entity2": "course",
                "entity2_nbr": "m"
            },
            {
                "association": "teach",
                "entity1": "staff",
                "entity1_nbr": "1",
                "entity2": "course",
                "entity2_nbr": "n"
            },
            {
                "association": "affiliated_with",
                "entity1": "staff",
                "entity1_nbr": "n",
                "entity2": "college",
                "entity2_nbr": "m"
            },
            {
                "association": "publish",
                "entity1": "staff",
                "entity1_nbr": "1",
                "entity2": "notice",
                "entity2_nbr": "n"
            },
            {
                "association": "issued_to",
                "entity1": "financial_order",
                "entity1_nbr": "1",
                "entity2": "student",
                "entity2_nbr": "1"
            },
            {
                "association": "reside_in",
                "entity1": "student",
                "entity1_nbr": "1",
                "entity2": "dormitory",
                "entity2_nbr": "n"
            }
        ]
        return entity_list, entity_dict, associations

    def create_er_graph(self, entity_list, entity_dict, associations, output_dir, output_name):
        G = pgv.AGraph(directed = False)
        for i in range(len(entity_list)):
            G.add_node(f"entity_{i}", shape = "rectangle", label = entity_list[i]) # 矩形实体
            tmp = entity_dict[entity_list[i]]
            for j in range(len(tmp)):
                G.add_node(f"attribute_{entity_list[i]}_{j}", shape = "rectangle", style = "rounded", 
                        label = tmp[j])
                G.add_edge(f"entity_{i}", f"attribute_{entity_list[i]}_{j}")
        
        for i in range(len(associations)):
            tmp = associations[i]
            G.add_node(f"relationship_{i}", shape = "diamond", label = tmp["association"]) # 菱形关系
            index_entity1 = entity_list.index(tmp["entity1"])
            index_entity2 = entity_list.index(tmp["entity2"])
            G.add_edge(f"entity_{index_entity1}", f"relationship_{i}", label = tmp["entity1_nbr"])
            G.add_edge(f"entity_{index_entity2}", f"relationship_{i}", label = tmp["entity2_nbr"])
            
        G.graph_attr.update(label="ER Diagram Example", fontsize="12", fontcolor="black",
                        fontname="Arial", rankdir="TB")  # TB 表示自顶向下布局
        G.graph_attr.update(
            overlap='false',  # 关闭节点重叠
            splines='true',   # 启用曲线边
            rankdir='TB',     # 指定布局方向
            ranksep='.2',     # 节点间的垂直距离
            nodesep='.1',     # 边上的点之间的水平距离
            fontsize=10,      # 字体大小
            fontname="Arial", # 字体名称
        )
        print(output_dir)
        print(output_name)
        output_name = os.path.join(output_dir, output_name)
        print(output_dir)
        print(output_name)
        G.draw(f'{output_name}.png', prog='sfdp')

    def work(self):
        # 生成大模型输入
        q = self.generate_prompt()
        # 获取大模型返回结果
        ret = self.get_LLM_response(q)
        # 解析结果
        entity_list, entity_dict, associations = self.analysis_model_output(ret)
        # 画图
        self.create_er_graph(entity_list, entity_dict, associations, self.output_dir, self.output_name)



if __name__ == "__main__":
    # 测试
    content = ""
    output_dir = "D:\\py_code\\study"
    output_name = "test"
    worker = ERDiagramGenerator(content=content, output_dir=output_dir, output_name=output_name)
    worker.work()