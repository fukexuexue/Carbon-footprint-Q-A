class QuestionParser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)#实体
        question_types = res_classify['question_types']#关系
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            # 关系类问题
            if question_type == 'related_company':
                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            elif question_type == 'next_stage':
                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            elif question_type == 'son_stage':
                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            elif question_type == 'consider':
                sql = self.sql_transfer(question_type, entity_dict.get('method'))

            elif question_type == 'computing_method':
                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            # 属性类问题
            elif question_type == 'stage_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            elif question_type == 'stage_way_decline':

                sql = self.sql_transfer(question_type, entity_dict.get('stage'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 关系类问题
        if question_type == 'related_company':
            sql = ["MATCH (m:Stage)-[r:related_company]->(n:Company) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'computing_method':
            sql = ["MATCH (m:Stage)-[r:computing_method]->(n:Method) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'consider':
            sql = ["MATCH (m:Method)-[r:consider]->(n:Factor) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'son_stage':
            sql = ["MATCH (m:Stage)-[r:son_stage]->(n:Stage) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'next_stage':
            sql = ["MATCH (m:Stage)-[r:next_stage]->(n:Stage) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 属性类问题
        elif question_type == 'stage_desc':
            sql = ["MATCH (m:Stage) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        elif question_type == 'stage_way_decline':
            sql = ["MATCH (m:Stage) where m.name = '{0}' return m.name, m.way_decline".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionParser()
