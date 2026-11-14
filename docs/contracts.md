# 来源接口与业务口径

design.py的validate校验企业唯一分组、完整二元outcomes、合法实际邀请数和饱和档概率。每group独立选(m,p)档后，在N个企业中等概率无放回选择m个。draw按seed抽一次真实分配，local_space枚举单组分配及其概率，不计算暴露效应。

network.py的exposure只接受登记企业的组内无向边，拒绝自环与跨组边，返回own_invited与any_neighbor_invited。孤立企业的邻居暴露恒为0。prepared同时绑定设计和网络摘要。outcomes是冻结资料，重复分配不生成新的企业观测。

输入为UTF-8 JSON，金额为十进制字符串。样例是合成资料，不限定分析数据规模。
