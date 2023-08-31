# encoding: utf-8
"""
@project: djangoModel->user_apply_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户审批服务
@created_time: 2023/8/30 17:09
"""

"""
设计思路：
所有的审核都有四个状态
[{"label": "未申请", "value": "0"}, {"label": "通过", "value": "1"}, {"label": "待审核", "value": "2"}, {"label": "审核驳回", "value": "3"}]

执行步骤：
1. 仅仅在 未申请/审核驳回 状态可以添加申请。
2. 通过联动用户状态，用户字段改成通过。
3. 审核不通过，联动用户字段改成不通过。
4. 审核不通过，用户可以继续提交申请，并生成一条新的记录。
5. 审批记录仅仅有三个状态：待审核、通过、审核驳回, 没有提交记录就是未审批。

核心：
整个审批过程中需要保证 用户详情状态与审批记录结果一致。
审核通过的审批，联动了用户详情里面状态，由于 ‘仅仅在 未申请/审核驳回 状态可以添加申请。’ 所以不可以重复申请审批了。达到了状态一致。
用户审批记录与用户主表和用户详细表的审核状态结合。

各端判断：
1. 移动端使用用户详情里面的字段
2. 后台管理端仅仅看审批记录，看已通过的需要在在审批管理里面，选择已通过卡片就可以看到通过审批记录，这些记录代表审核通过的用户。

查询：
审批主表，联表：用户主表、用户详情表。

审批类型：
代表不通的审批类型，且配置了，用户详情表与审批结果的映射。

表结构：
-- 用户状态审批表
CREATE TABLE `user_apply_record` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '申请的用户ID',
  `apply_type_id` int NOT NULL COMMENT '审批类型',
  `verify_user_id` int NOT NULL COMMENT '审核人',
  `result` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'VERIFYING' COMMENT '审核结果: 通过：PASS；拒绝：REJECT；忽略：IGNORE; 审核中：VERIFYING',
  `remark` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '' COMMENT '备注',
  `reject_reason` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '' COMMENT '拒绝理由',
  `snapshot` json DEFAULT NULL COMMENT '用户状态快照',
  `verifyed_time` timestamp NULL DEFAULT NULL COMMENT '审核时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci COMMENT='用户状态审批表';
-- 用户申请类型
CREATE TABLE `user_apply_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '类型搜索key',
  `type_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型名称',
  `description` varchar(500) NOT NULL COMMENT '描述',
  `config` json DEFAULT NULL COMMENT '配置，联动字段配置',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户申请类型';
"""


class UserApplyServices:
    @staticmethod
    def add_apply_record(params: dict = None):
        """
        添加审批记录, 联动用户状态修改成审核中
        :return:
        """
        pass

    def edit_apply_record(self):
        pass

    def apply_record_list(self):
        pass

    def get_record_detail(self):
        pass
