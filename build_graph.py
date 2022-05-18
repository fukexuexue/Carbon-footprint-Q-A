import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'submit.json')
        self.g = Graph('http://localhost:7474', auth=('neo4j', 'Luffypg3777'))  # 第一步先启动graph

    '''读取文件'''
    def read_nodes(self):  #列表表示节点和关系，字典表示病的属性
        # 共4类节点
        stages = [] # 阶段
        methods = [] #　计量方法
        factors = [] # 因子
        companies = [] #企业

        stage_infos = []#疾病信息  由疾病的属性字典构成

        # 构建节点实体关系
        rels_stages_s = []  # 阶段－阶段子关系
        rels_stages_n = []  # 阶段－阶段下关系
        rels_methods = [] # 阶段－计量方法关系
        rels_companies = [] # 阶段－相关企业关系
        rels_factors = []  # 计量方法－计算因子关系


        count = 0
        with open('submit.json', 'r') as f:
            for data_json in json.load(f):#data存为json格式,将字符串转换为代码
                stage_dict = {}   #一条数据一个字典，即一个阶段一个字典，字典表示的是属性
                count += 1
                print(count)
                stage = data_json['name'] #取出字段‘name’
                stage_dict['name'] = stage #这是什么阶段构建字典
                stages.append(stage)
                stage_dict['desc'] = '' #字段存入字典中,阶段的描述作为属性
                stage_dict['way_decline'] = ''   #每个阶段的减排方式作为属性
               #每个类的信息过一遍，要么建立属性、要么创建关系（当这一类信息有多个元素时，就要遍历一遍）、要么生成节点，
                if 'sonstage' in data_json:#子阶段
                    stages += data_json['sonstage']
                    for sonstage in data_json['sonstage']:#不止有一个子阶段，遍历，创建关系
                        rels_stages_s.append([stage, sonstage])

                if 'next_stage' in data_json:#下一阶段
                    next_stage = data_json['next_stage']
                    stages.append(next_stage)
                    rels_stages_n.append([stage, next_stage])

                if 'company' in data_json:#相关企业
                    companies += data_json['company']
                    for company in data_json['company']:
                        rels_companies.append([stage, company])

                if 'desc' in data_json:  # 创建这个阶段的属性
                    stage_dict['desc'] = data_json['desc']

                if 'way_decline' in data_json:
                    stage_dict['way_decline'] = data_json['way_decline']

                if 'method' in data_json:
                    for method in data_json["method"]:
                        for i in range(len(method)):
                            if i == 0:
                                methods.append(method[i])
                                rels_methods.append([stage,method[i]])
                            else:
                                factors.append(method[i])
                                rels_factors.append([method[0],method[i]])
                stage_infos.append(stage_dict)
        return set(stages), set(methods), set(factors), set(companies), stage_infos,\
                   rels_factors,rels_methods,rels_companies,rels_stages_n,rels_stages_s

    '''建立节点'''
    def create_node(self, label, nodes):   #创建没有属性的点，自己定标签
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心阶段的节点'''
    def create_diseases_nodes(self, stage_infos):   #创建有属性的点   每个节点对应着有标签和属性
        count = 0
        for stage_dict in stage_infos:
            #创建节点，指定label，name，name是属性
            node = Node("Stage", name = stage_dict['name'], desc = stage_dict['desc'],
                        way_decline = stage_dict['way_decline'] )
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):   #参数都是列表：节点和关系
        Stages, Methods, Factors, Companies, stage_infos, rels_factors, rels_methods, rels_companies, rels_stages_n, rels_stages_s = self.read_nodes()
        self.create_diseases_nodes(stage_infos)    #有属性的节点，要先单独写一个函数来给建立节点，同时附上属性
        self.create_node('Method', Methods)
        print(len(Methods))
        self.create_node('Factor', Factors)
        print(len(Factors))
        self.create_node('Company', Companies)
        print(len(Companies))
        return

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):   #（标签1，标签2.关系集合，关系类别，关系名称（中文--用于问答）
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))

        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        Stages, Methods, Factors, Companies, stage_infos, rels_factors, rels_methods, rels_companies, rels_stages_n, rels_stages_s = self.read_nodes()
        self.create_relationship('Stage', 'Method', rels_methods, 'computing_method', '计算方法')
        self.create_relationship('Stage', 'Company', rels_companies, 'related_company', '相关公司')
        self.create_relationship('Method', 'Factor', rels_factors, 'consider', '计算因子')
        self.create_relationship('Stage', 'Stage', rels_stages_s, 'son_stage', '子阶段')
        self.create_relationship('Stage', 'Stage', rels_stages_n, 'next_stage', '下一阶段')


    '''导出数据'''
    def export_data(self):
        Stages, Methods, Factors, Companies, stage_infos, rels_factors, rels_methods, rels_companies, rels_stages_n, rels_stages_s = self.read_nodes()
        f_stage = open('./dict/stage.txt', 'w+',encoding='utf-8')
        f_company = open('./dict/company.txt', 'w+',encoding='utf-8')
        f_factor = open('./dict/factor.txt', 'w+',encoding='utf-8')
        f_method = open('./dict/method.txt', 'w+',encoding='utf-8')

        f_stage.write('\n'.join(list(Stages)))
        f_company.write('\n'.join(list(Companies)))
        f_factor.write('\n'.join(list(Factors)))
        f_method.write('\n'.join(list(Methods)))

        f_stage.close()
        f_company.close()
        f_factor.close()
        f_method.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()#初始化graph，连接neo4j
    # handler.export_data()
    handler.create_graphnodes()#创建节点
    handler.create_graphrels()#创建关系
