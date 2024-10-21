from openai import OpenAI
import re
import ast

def get_LLM_response(content):
    api_key = "sk-tp0PvDsgccr8HRRHKXOCC9m5yQv9t2ifQJJoTs0PrfiLtpTd"
    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    completion = client.chat.completions.create(model="moonshot-v1-8k", messages=[{"role": "user", "content": content}], temperature=0.3)
    ret = completion.choices[0].message.content
    return ret

# def clean_string(s):
#     """移除字符串中的注释和多余的空白字符"""
#     s = re.sub(r'#.*', '', s)  # 移除注释
#     s = re.sub(r'\s+', ' ', s)  # 移除多余的空白字符
#     return s.strip()

# def analysis_model_output(ret):
#     entity_list = []
#     entity_dict = {}
#     associations = []
    
#     # 使用正则表达式匹配实体列表
#     entity_list_match = re.search(r'entity_list = \[(.*?)\]', ret, re.DOTALL)
#     if entity_list_match:
#         entity_list_str = clean_string(entity_list_match.group(1) + ']')
#         print("Raw entity_list string:", entity_list_str)
#         try:
#             entity_list = ast.literal_eval(entity_list_str)
#         except Exception as e:
#             print("Error parsing entity_list:", e)
    
#     # 使用正则表达式匹配实体属性字典
#     entity_dict_match = re.search(r'entity_dict = {(.*?)}', ret, re.DOTALL)
#     if entity_dict_match:
#         entity_dict_str = clean_string(entity_dict_match.group(1) + '}')
#         print("Raw entity_dict string:", entity_dict_str)
#         try:
#             entity_dict = ast.literal_eval(entity_dict_str)
#         except Exception as e:
#             print("Error parsing entity_dict:", e)
    
#     # 使用正则表达式匹配实体间的关联关系
#     associations_match = re.search(r'associations = \[(.*?)\]', ret, re.DOTALL)
#     if associations_match:
#         associations_str = clean_string(associations_match.group(1) + ']')
#         print("Raw associations string:", associations_str)
#         try:
#             associations = ast.literal_eval(associations_str)
#         except Exception as e:
#             print("Error parsing associations:", e)
    
#     return entity_list, entity_dict, associations


def analysis_model_output(ret):
    # 移除注释和多余的空格
    ret = re.sub(r'#.*', '', ret)  # 移除注释
    ret = re.sub(r'\s+', ' ', ret)  # 移除多余的空白字符
    entity_list = []
    entity_dict = {}
    associations = []

    # 提取并解析 entity_list
    entity_list_match = re.search(r'entity_list = \[(.*?)\]', ret, re.DOTALL)
    if entity_list_match:
        entity_list_str = entity_list_match.group(1).strip()
        entity_list = ast.literal_eval('[' + entity_list_str + ']')
    
    # 提取并解析 entity_dict
    entity_dict_match = re.search(r'entity_dict = {(.*?)}', ret, re.DOTALL)
    if entity_dict_match:
        entity_dict_str = entity_dict_match.group(1).strip()
        entity_dict = ast.literal_eval('{' + entity_dict_str + '}')
    
    # 提取并解析 associations
    associations_match = re.search(r'associations = \[(.*?)\]', ret, re.DOTALL)
    if associations_match:
        associations_str = associations_match.group(1).strip()
        associations = ast.literal_eval('[' + associations_str + ']')
    
    return entity_list, entity_dict, associations

content = """
现在有这样一个微人大学校事务管理系统的数据库：我们希望构建的实体主要有学生、教职工、课程、通知、学院、财务订单、宿舍、职务、课程名，请你自己补充以上实体所需要的属性数据以及实体间的联系，要求尽可能详细。
"""

suffix = """
            要求：根据上述语义画出ER 图，要求在图中画出并注明联系的类型；实体的属性。
            请将上面这段文字整理成如下er图信息表（注意，下面的代码仅提供格式信息，你不要学习下面python代码中的属性、联系等信息）：
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
content = content + suffix
# response = get_LLM_response(content)
response = """以下是根据您提供的信息整理的ER图信息表：

```python
entity_list = [
    "student",
    "staff",
    "course",
    "notice",
    "college",
    "financialOrder",
    "dormitory",
    "position"  # 新增实体职务
]

entity_dict = {
    "student": [
        "student_id",
        "student_name",
        "student_gender",
        "student_age",
        "student_major",
        "student_college",
        "student_dorm_id"  # 学生宿舍ID
    ],
    "staff": [
        "staff_id",
        "staff_name",
        "staff_title",
        "staff_department",
        "staff_college",
        "staff_position_id"  # 教职工职务ID
    ],
    "course": [
        "course_id",
        "course_name",
        "course_credit_hours",
        "course_staff_id"  # 课程对应的教职工ID
    ],
    "notice": [
        "notice_id",
        "notice_title",
        "notice_content",
        "notice_publish_date",
        "notice_staff_id"  # 发布通知的教职工ID
    ],
    "college": [
        "college_id",
        "college_name",
        "college_president"  # 学院院长
    ],
    "financialOrder": [
        "forder_id",
        "forder_payer",
        "forder_amount",
        "forder_status",
        "forder_student_id"  # 财务订单对应的学生ID
    ],
    "dormitory": [
        "dorm_id",
        "dorm_building",
        "dorm_room_number",
        "dorm_capacity",
        "dorm_college_id"  # 宿舍所属学院ID
    ],
    "position": [  # 新增实体职务
        "position_id",
        "position_name",
        "position_description"
    ]
}

associations = [
    {
        "association": "attend",
        "entity1": "student",
        "entity1_nbr": "m",
        "entity2": "course",
        "entity2_nbr": "n"
    },
    {
        "association": "teach",
        "entity1": "staff",
        "entity1_nbr": "n",
        "entity2": "course",
        "entity2_nbr": "1"
    },
    {
        "association": "work_for",
        "entity1": "staff",
        "entity1_nbr": "m",
        "entity2": "college",
        "entity2_nbr": "1"
    },
    {
        "association": "live_in",
        "entity1": "student",
        "entity1_nbr": "1",
        "entity2": "dormitory",
        "entity2_nbr": "n"
    },
    {
        "association": "issue",
        "entity1": "staff",
        "entity1_nbr": "1",
        "entity2": "notice",
        "entity2_nbr": "n"
    },
    {
        "association": "pay",
        "entity1": "student",
        "entity1_nbr": "1",
        "entity2": "financialOrder",
        "entity2_nbr": "n"
    },
    {
        "association": "hold",
        "entity1": "staff",
        "entity1_nbr": "1",
        "entity2": "position",
        "entity2_nbr": "n"
    }
]
```

在这个ER图信息表中，我添加了一个新的实体“position”来表示职务，并为每个实体添加了相应的属性。同时，我也补充了一些实体间的联系，例如教职工和职务之间的关系，以及学生和财务订单之间的关系。这些联系有助于更全面地描述人大学校事务管理系统的数据库结构。
"""
entity_list, entity_dict, associations = analysis_model_output(response)

print("Entity List:", entity_list)
print("Entity Dictionary:", entity_dict)
print("Associations:", associations)