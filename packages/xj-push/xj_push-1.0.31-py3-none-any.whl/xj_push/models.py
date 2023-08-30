from django.db import models


class PushPlan(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    role_id = models.IntegerField(verbose_name='权限id', help_text='')
    group_id = models.IntegerField(verbose_name='分组id', help_text='')
    user_id_list = models.JSONField(verbose_name='用户id列表', blank=True, null=True, help_text='')
    template_id = models.IntegerField(verbose_name='权限ID', help_text='')
    node_to_action_id = models.IntegerField(verbose_name='节点对动作ID', help_text='')
    plan_push_circle = models.CharField(verbose_name='计划周期，参考contab', max_length=50, help_text='')
    plan_push_time = models.DateTimeField(verbose_name='推送时间', help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'push_plan'
        verbose_name_plural = "推送-推送流程"

    def __str__(self):
        return f"{self.id}"


class PushPush(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    templet_id = models.IntegerField(verbose_name='模板id', primary_key=False, help_text='')
    plan_id = models.IntegerField(verbose_name='计划id', primary_key=False, help_text='')
    title = models.CharField(verbose_name='标题', max_length=128)
    content = models.CharField(verbose_name='内容', max_length=128)
    files = models.JSONField(verbose_name='文件', blank=True, null=True, help_text='')
    push_total = models.IntegerField(verbose_name='本次推送用户数量', primary_key=False, help_text='')
    send_success = models.IntegerField(verbose_name='发送成功的用户', primary_key=False, help_text='')
    send_time = models.DateTimeField(verbose_name='开始发送时间')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'push_push'
        verbose_name_plural = "推送-推送主表"

    def __str__(self):
        return f"{self.id}"


class PushRecord(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    push_id = models.IntegerField(verbose_name='推送ID', primary_key=False, help_text='')
    to_user_id = models.IntegerField(verbose_name='发送的用户ID', primary_key=False, help_text='')
    is_receive = models.CharField(verbose_name='是否送达', max_length=128)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'push_record'
        verbose_name_plural = "推送-推送记录"

    def __str__(self):
        return f"{self.id}"


class PushTemplate(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    value = models.CharField(verbose_name='模板搜索关键词', max_length=128, blank=True, null=True, help_text='')
    template = models.CharField(verbose_name='内容推送模板，变量使用{}包裹', max_length=128, blank=True, null=True, help_text='')
    default_params = models.JSONField(verbose_name='模板变量', blank=True, null=True, help_text='')
    alias_params = models.JSONField(verbose_name='模板别名', blank=True, null=True, help_text='')
    title = models.CharField(verbose_name='发送标题', max_length=128, blank=True, null=True, help_text='')
    send_type = models.CharField(verbose_name='模板类型', max_length=128, blank=True, null=True, help_text='')
    files = models.JSONField(verbose_name='模板变量', blank=True, null=True, help_text='')
    push_times = models.IntegerField(verbose_name='推送次数', primary_key=False, help_text='')
    push_success = models.IntegerField(verbose_name='推送成功人数', primary_key=False, help_text='')
    push_total = models.IntegerField(verbose_name='推送模板人数', primary_key=False, help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    enabled = models.IntegerField(verbose_name='是否启用', default=0)

    class Meta:
        db_table = 'push_template'
        verbose_name_plural = "推送-推送模板"

    def __str__(self):
        return f"{self.id}"


class PushSingle(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    to_user_id = models.IntegerField(verbose_name='发送用户ID', help_text='')
    source_code = models.CharField(verbose_name='发送用户ID', max_length=50, help_text='')
    title = models.CharField(verbose_name='发送用户ID', max_length=255, help_text='')
    content = models.TextField(verbose_name='发送用户ID', help_text='')
    template = models.ForeignKey("PushTemplate", verbose_name="模板变量", help_text="", null=True, blank=True, on_delete=models.DO_NOTHING)
    thread_id = models.IntegerField("PushTemplate", help_text="", null=True, blank=True)
    template_params = models.JSONField(verbose_name="模板变量", help_text="")
    link = models.CharField(verbose_name='发送类型', max_length=500, null=True, blank=True, help_text='')
    is_jump_link = models.BooleanField(verbose_name='发送类型', default=0, null=True, blank=True, help_text='')
    send_type = models.TextField(verbose_name='发送类型', help_text='')
    files = models.JSONField(verbose_name='文件集合', help_text='')
    is_read = models.IntegerField(verbose_name='是否阅读', default=0, help_text='')
    is_delete = models.IntegerField(verbose_name='是否删除', default=0, help_text='')
    snapshot = models.JSONField(verbose_name='快照', null=True, blank=True, default={})
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=False, blank=True, help_text='')
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=False, blank=True, help_text='')

    class Meta:
        db_table = 'push_single'
        verbose_name_plural = "推送-站内推送"

    def __str__(self):
        return f"{self.id}"
