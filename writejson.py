# -*- coding:utf-8 -*-
import json
import os

jsondata_list = []  #用来写入json文件的总列表
bcedata_list = [
                ["建材阶段","建材阶段是指从建材原材料的开采、运输、加工和建材生产一直到建材运输到施工现场的过程。该阶段的碳排放主要来源于上述过程中的能源消耗以及生产工艺环节中的物化反应。国内现有研究普遍认为，该阶段是除运营阶段之外碳排放量最大的阶段，占整个生命周期的10%～30%左右。",["建材生成阶段", "建材运输阶段"], [["一次能源换算法", "高回收率建材", "水泥","混凝土砌块", "砖", "陶瓷"],["排放系数法","建材种类","建材使用量","建材碳排放因子","建材回收处理"]],["巨石集团", "北新建材", "洛阳玻璃", "三狮集团", "南方水泥", "中联水泥", "北方水泥", "西南水泥"],"使用新型干法水泥较传统水泥工业的能源效率有很大的减排空间。通过更新研发设备、优化生产工艺，水泥工业能效有的减排潜力通过减少能源的消耗。实验研究表明，通过减少石灰石原料燃料的使用，更换使用可替代的工业废弃物的方法可以显著降低二氧化碳的排放量。",
                "建筑施工阶段"],
                ["建材生成阶段",'是生成建筑过程中所用材料的过程',['建材开采','建材生产'],[['估算法','工程定额']],['北新建材','南方水泥','巨石集团'],'提高材料回收率，优化材料加工处理方式（如钢材使用转炉法）','建材运输阶段'],
                ['建材开采','是获取建筑材料的开采生产过程',[],[['估算法','化石能源碳足迹因子','电力碳足迹因子','建筑材料碳足迹因子']],[],'降低火力发电的比例，减少燃料油等燃料的比例','建材生产'],
                ['建材生产','是生产制作建筑材料的过程',[],[['估算法','化石能源碳足迹因子','电力碳足迹因子','建筑材料碳足迹因子']],[],'降低火力发电的比例，减少燃料油等燃料的比例','建材运输阶段'],
                ["建材运输阶段",'是建筑材料从工厂运输至施工现场的运输过程',['运输至施工现场'],[['估算法','运输工具','运输方式','运输重量','运输距离'],['排放系数法','材料质量','运输方式','运输距离']],['中远海运','中铁快运','中国储运'],'根据运输距离、质量选择合适的运输方式','建筑施工阶段'],
                ["建筑施工阶段","建筑施工阶段是指建材运送到施工场地以后，在现场的施工和建造过程。建造施工阶段的能耗主要是各种机械设备用电以及各施工工艺的燃料消耗等。",[],[["投入产出法","施工费用"],["施工程序能耗估算法"],["现场能耗实测法","施工供应量","碳排放因子"],["预决算书估算法"],["施工工艺法","原地平整场地","起重机搬运","水平运输","施工工艺工程量"],["将故居施工现场的能源消耗量及能源的碳排放因子来计算建造施工的二氧化碳排放量"]],["中国建筑股份有限公司","中国中铁股份有限公司","中国铁建股份有限公司",
                "中国交通建设股份有限公司","中国冶金科工股份有限公司","中国电力建设股份有限公司","上海建工集团股份有限公司","中国葛洲坝集团股份有限公司","中国化学工程股份有限公司"],"因此，发展推广木结构（特别是复合木材,料）,装配式钢结构，加大建筑工业化和装配率是降低建筑物化阶段碳排的有效手段。","建筑运营阶段"],
                ["建筑运营阶段",'是建筑落地后进行日常使用及盈利和后续维护的过程',['产品使用','建筑维护','更新改造'],[['估算法','设备功率','年能耗','设计年限','建筑材料的更换年限'],["排放系数法","空调等设备生产耗能","设备运行耗能","建筑维护更新耗能"]],['中国建筑股份有限公司','中国中铁股份有限公司','中国铁建股份有限公司'],'建设绿地进行碳抵消，采用监测仪表实时统计及时更新老旧设备','建筑拆除阶段'],
                ['产品使用','是维持建筑能够实现其建筑功能的阶段',[],[['功率估算法','设备功率','运行时间','设备使用碳足迹因子'],['软件辅助估算法','计算机数据整理'],['统计数据辅助法','《民用建筑能耗统计报表制度》、《中国统计年鉴》'],['实际信息估算法','用户缴费信息','监测仪表']],[],'种植绿色植物进行碳抵消','建筑维护'],
                ['建筑维护','是指在建筑落地后的长周期内维持其原有功能的过程',[],[['估算法','材料更换的碳足迹','人工或机械作业的碳足迹'],["排放系数法","维护更新年二氧化碳排放量","建筑使用年限"]],['万科物业','碧桂园服务'],"",'更新改造'],
                ['更新改造','是指对现有建筑物的功能及外观进行翻新重制的过程',[],[['估算法','材料更换的碳足迹','人工或机械作业的碳足迹'],["排放系数法","维护更新年二氧化碳排放量","建筑使用年限"]],['北京今朝装饰','广州星艺装饰'],'可采用环保材料或局部装修，实现小能耗高功效',''],
                ["建筑拆除阶段",'是建筑物的功能损失后的拆除及后续废弃物处理的阶段',['拆除施工','建筑垃圾运输','建筑垃圾处置'],[['估算法','拆除机械施工','运输机械耗能','实际消耗量'],["排放系数法","建筑拆除施工过程中的二氧化碳排放量","建筑垃圾运输过程中的二氧化碳排放量","建筑垃圾处理过程中的二氧化碳排放量"]],['北京中海建筑物拆除有限公司','鑫源拆迁公司'],'不仅仅要着眼于降低使用阶段的碳排放，还应该合理减少建筑的“大拆大建”，增加定期维护保养，延长居住建筑的可使用时间，减少二氧化碳的重复排放。提高废弃物回收利用率',''],
                ["拆除施工","对已经建成或部分建成的建筑物或构筑物等进行拆除",[],[["施工工艺法","破碎、构建拆除工艺","开挖、移除土方","平整土方","起重机搬运","建筑施工能耗*10%"]],[],"优化拆除方式，用拆解代替拆除，使各种建材得到充分的回收和再利用。","建筑垃圾运输"],
                ["建筑垃圾运输","对建筑物实施新建、改建、扩建或者是拆除过程中产生的固体废弃物从施工现场到建筑垃圾处理厂的过程",[],[['估算法','运输工具','运输方式','运输重量','运输距离']],[],"","建筑垃圾处置"],
                ["建筑垃圾处置","对建筑物实施新建、改建、扩建或者是拆除过程中产生的固体废弃物进行焚烧、填埋或回收等处理",[],[["排放系数法","垃圾处理方式","建筑垃圾种类","建筑垃圾数量"]],[],"提高建筑垃圾回收利用率",""],
                ["全生命周期","是指从材料与构建生产、规划与设计、建造与运输、运行与维护直到拆除与处理（废弃、再循环和再利用等）的全循环过程。",["建材阶段","建筑施工阶段","建筑运营阶段","建筑拆除阶段"],[["生命周期法","建筑面积"]],["海螺水泥","华建集团","碧桂园","招商蛇口","华新水泥"],"多采用集成建筑,装配式建筑,模块化建筑,超低能耗建筑",""]
                ]
#所有的基础信息列表
##########编写每条的数据########
for bce in bcedata_list:
    bce_dict = {}
    bce_dict["name"] = bce[0]  #阶段
    bce_dict["desc"] = bce[1]   #描述
    bce_dict["sonstage"] = bce[2]   #子阶段
    bce_dict["method"] = bce[3]    #计量方法
    bce_dict["company"] = bce[4]    #相关公司
    bce_dict["way_decline"] = bce[5]  #减排措施
    bce_dict["next_stage"] = bce[6]  # 下一阶段
    jsondata_list.append(bce_dict)
with open('submit.json', 'w+', encoding='utf8') as f:
    json.dump(jsondata_list,f)

with open('submit.json', 'r') as f:
    for i in json.load(f):
        print(len(i))
        print(i['method'])
