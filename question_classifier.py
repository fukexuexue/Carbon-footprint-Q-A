import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.company_path = os.path.join(cur_dir, 'dict/company.txt')
        self.stage_path = os.path.join(cur_dir, 'dict/stage.txt')
        self.factor_path = os.path.join(cur_dir, 'dict/factor.txt')
        self.method_path = os.path.join(cur_dir, 'dict/method.txt')
        # 加载特征词
        self.company_wds= [i.strip() for i in open(self.company_path,encoding="utf-8") if i.strip()]#encoding="utf-8"
        self.stage_wds= [i.strip() for i in open(self.stage_path,encoding="utf-8") if i.strip()]
        self.factor_wds= [i.strip() for i in open(self.factor_path,encoding="utf-8") if i.strip()]
        self.method_wds= [i.strip() for i in open(self.method_path,encoding="utf-8") if i.strip()]
        self.region_words = set(self.company_wds + self.stage_wds +self.method_wds+self.factor_wds)

        # 构造领域actree，匹配特征词，不同于看这个词是否存在，匹配要更精准
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        # 关系类问题
        self.wdtype_dict = self.build_wdtype_dict()
        self.computing_method_qwds = ["计算方法", "度量", "衡量", "计算", "度量方法", "计算方式", "途径", "公式", "用什么","仪器", "测量", "使用什么", "怎么计算", "怎样计算", "如何度量"]
        self.related_company_qwds = ['相关公司','企业','责任方','股份有限公司','哪家','哪个公司','哪一方','单位','部门','工厂','制造厂商','生产企业','制造厂','机构','责任','机关']
        self.consider_qwds = ['哪些影响因素', '造成', '影响比较大', "因子","影响因子","要素"]
        self.son_stage_qwds = ['子阶段有哪些', '子步骤', "分为几步", "子流程"]
        self.next_stage_qwds = ['下一步','接下来','下一阶段','下一个','下一个流程','随后','于是','此后','以后','之后','随后']
        # 属性类问题
        self.stage_way_decline_qwds = [ '减碳方式', "减排", "减碳", "减排方式"]
        self.stage_desc_qwds = ['什么意思', '描述', "怎样描述", "定义", "怎样描述", "概念", '描述','怎样描述','是什么','定义','概念','什么含义','涵义','含意','如何界定','释义','通俗表达','是啥','如何解释','该怎么解释','该怎么描述']
        print('model init finished ......')
        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        stage_dict = self.check_stage(question)
        if not stage_dict:
            return {}
        data['args'] = stage_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in stage_dict.values():
            types += type_
        question_type = 'others'
        question_types = []
        print(types)

        # 关系类问题
        # 阶段-企业
        if self.check_words(self.related_company_qwds, question) and ('stage' in types):
            question_type = 'related_company'
            question_types.append(question_type)

        #阶段-下一阶段
        if self.check_words(self.next_stage_qwds, question) and ('stage' in types):
            question_type = 'next_stage'
            question_types.append(question_type)

        #阶段-子阶段
        if self.check_words(self.son_stage_qwds, question) and ('stage' in types):
            question_type = 'son_stage'
            question_types.append(question_type)

        # 计算方法-影响因子
        if self.check_words(self.consider_qwds, question) and ('method' in types):
            question_type = 'consider'
            question_types.append(question_type)

        # 阶段-计算方法
        if self.check_words(self.computing_method_qwds, question) and ('stage' in types):
            question_type = 'computing_method'
            question_types.append(question_type)

        # 属性类问题
        # 阶段-描述
        if self.check_words(self.stage_desc_qwds, question) and ('stage' in types):
            question_type = 'stage_desc'
            question_types.append(question_type)

        # 阶段-减排方式
        if self.check_words(self.stage_way_decline_qwds, question) and ('stage' in types):
            question_type = 'stage_way_decline'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == []:
            print("数据库信息不足够")
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.company_wds:
                wd_dict[wd].append('company')
            if wd in self.factor_wds:
                wd_dict[wd].append('factor')
            if wd in self.stage_wds:
                wd_dict[wd].append('stage')
            if wd in self.method_wds:
                wd_dict[wd].append('method')
        return wd_dict
    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_stage(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        print(region_wds)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        # print(data)