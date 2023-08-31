from django.db import models, connection

SHARD_TABLE_NUM = 3


class Region(models.Model):
    id = models.AutoField("ID", primary_key=True)
    code = models.IntegerField('行政编码', null=False, default=0)
    p_code = models.IntegerField('上级行政编码', null=False, default=0)
    name = models.CharField('地区名称', null=False, default="", max_length=50)
    level = models.IntegerField('行政划分等级', null=False, default="0")
    is_delete = models.IntegerField('是否删除', null=False, default=0)
    spell = models.CharField('拼音', max_length=50, null=False, default="")

    class Meta:
        managed = False
        db_table = "append_public_region"
        verbose_name = "行政区编码表"
        verbose_name_plural = verbose_name


class NoticeType(models.Model):
    class Meta:
        managed = False
        db_table = "append_public_notice_type"
        verbose_name = "提醒类型表"
        verbose_name_plural = verbose_name

    id = models.AutoField("ID", primary_key=True)
    value = models.CharField(max_length=25, null=True, blank=True, default="", verbose_name='提醒类型', )
    name = models.CharField(max_length=255, null=True, blank=True, default="", verbose_name='提醒类型名称', )
    description = models.CharField(max_length=255, null=True, blank=True, default="", verbose_name='类型描述', )

    def __str__(self):
        return self.name


class Notice(models.Model):
    class Meta:
        managed = False
        db_table = "append_public_notice"
        verbose_name = "提醒表"
        verbose_name_plural = verbose_name

    status_choice = [(0, '未读'), (1, '已读'), (3, '已删除')]

    id = models.AutoField("ID", primary_key=True)
    notice_type = models.ForeignKey(to=NoticeType, on_delete=models.DO_NOTHING, verbose_name='提醒类型', null=False, blank=False, )
    notice_title = models.CharField(max_length=255, null=False, blank=False, verbose_name='标题')
    notice_content = models.CharField(max_length=1250, null=False, blank=False, verbose_name='内容', default="")
    link = models.CharField(max_length=1500, null=False, blank=False, verbose_name='跳转链接', default="", help_text="跳转链接参数使用")
    files = models.JSONField(null=False, blank=False, verbose_name='文件json', default={}, help_text="消息提醒所带素材")
    status = models.IntegerField(null=False, blank=False, verbose_name='状态', default=0, choices=status_choice, help_text="0：未读；1：已读；2:已删除")
    created_time = models.DateTimeField(verbose_name='发出时间', auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True, verbose_name='已读时间')
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name='到期时间')
    thread_id = models.IntegerField(null=True, blank=True, verbose_name='信息（模板）ID', default=0)
    from_user_id = models.IntegerField(null=True, blank=True, verbose_name='发出提醒用户ID', default=0)
    to_user_id = models.IntegerField(null=True, blank=True, verbose_name='提醒用户ID', default=0)
    to_role_id = models.IntegerField(null=True, blank=True, verbose_name='提醒角色ID', default=0)


class AccessLevel(models.Model):
    id = models.AutoField("ID", primary_key=True)
    access_code = models.IntegerField(null=True, blank=True, verbose_name='访问级别的数字编码', default=0, help_text="注意：数值越大，权限越大。高访问级别可看到小于该访问级别的内容")
    access_level = models.CharField(max_length=25, null=True, blank=True, verbose_name='访问级别KEY', )
    name = models.CharField(max_length=255, null=False, blank=True, verbose_name='访问级别名称', default="", )
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='相关描述', default="", )

    class Meta:
        managed = False
        unique_together = ["access_level", "access_code"]
        db_table = "append_access_level"
        verbose_name = "访问级别表"
        verbose_name_plural = verbose_name


class Encyclopedia(models.Model):
    class Meta:
        managed = False
        db_table = "append_public_ecyclopedia"
        verbose_name = "百科问答表"
        verbose_name_plural = verbose_name

    id = models.AutoField("ID", primary_key=True)
    user_id = models.IntegerField(null=True, blank=True, verbose_name='用户ID')
    question = models.TextField(null=True, blank=True, verbose_name='问题描述')
    snapshot = models.JSONField(null=True, blank=True, verbose_name='快照')
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_time = models.DateTimeField(auto_now=True, null=True, blank=True)


class ModuleServices(models.Model):
    class Meta:
        managed = False
        db_table = "append_module_services"
        verbose_name = "模型服务映射表"
        verbose_name_plural = verbose_name

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE `{}`'.format(cls._meta.db_table))

    io_mode_choices = (
        ("SELECT", 'SELECT'),
        ("INSERT", 'INSERT'),
        ("DELETE", 'DELETE'),
        ("UPDATE", 'UPDATE'),
        ("NO_IO", "NO_IO")
    )
    data_type_choices = (
        ("MAIN", 'MAIN'),
        ("RECORD", 'RECORD'),
        ("DETAIL", 'DETAIL'),
        ("NO_INPUT", "NO_INPUT")
    )
    id = models.AutoField("ID", primary_key=True)
    module_name = models.CharField(null=True, max_length=120, blank=True, verbose_name='模型名称')
    service_name = models.CharField(null=True, max_length=120, blank=True, verbose_name='服务名称')
    description = models.CharField(null=True, max_length=5000, blank=True, verbose_name='描述')
    io_mode = models.CharField(choices=io_mode_choices, max_length=50, null=True, blank=True, verbose_name="IO模型")
    data_type = models.CharField(choices=data_type_choices, max_length=50, null=True, blank=True, verbose_name="数据类型")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Modules(models.Model):
    class Meta:
        managed = False
        db_table = "append_modules"
        verbose_name = "模型模块注册表"
        verbose_name_plural = verbose_name

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE `{}`'.format(cls._meta.db_table))

    module_type_choices = (
        ("SYSTEM", 'SYSTEM'),
        ("MAIN_MODULE", 'MAIN_MODULE'),
        ("SUB_MODULE", 'SUB_MODULE')
    )
    id = models.AutoField("ID", primary_key=True)
    module_name = models.CharField(null=True, max_length=120, blank=True, verbose_name='模型名称')
    module_type = models.CharField(choices=module_type_choices, max_length=50, null=True, blank=True, verbose_name="数据类型")
    description = models.CharField(null=True, max_length=5000, blank=True, verbose_name='描述')
    created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)


class AppVersion(models.Model):
    class Meta:
        managed = False
        db_table = "append_app_version"
        verbose_name = "APP版本表"
        verbose_name_plural = verbose_name

    app_system_choices = (
        ("ios", 'IOS'),
        ("android", 'Android'),
        ("h5", 'H5'),
        ("mp", 'MP')
    )
    version_type_choices = (
        ("alpha", 'Alpha'),
        ("beta", 'Beta'),
        ("rc", 'RC'),
        ("release", 'Release')
    )
    bool_choices = (
        (1, '是'),
        (0, '否')
    )

    id = models.AutoField("ID", primary_key=True)
    app_system = models.CharField(null=True, max_length=50, choices=app_system_choices, blank=True, verbose_name='app系统')
    version = models.CharField(max_length=255, null=True, blank=True, verbose_name="版本")
    version_type = models.CharField(null=True, max_length=255, choices=version_type_choices, blank=True, verbose_name='版本环境')
    store_name = models.CharField(null=True, max_length=255, blank=True, verbose_name="APP商城名称")
    store_url = models.CharField(null=True, max_length=5000, blank=True, verbose_name='APP商城跳转路由')
    version_detail = models.TextField(null=True, blank=True, verbose_name='更新内容')
    download_url = models.CharField(null=True, max_length=5000, blank=True, verbose_name='app软件下载地址')
    is_force_update = models.IntegerField(null=True, choices=bool_choices, default=0, blank=True, verbose_name='是否强制更新')
    push_time = models.DateTimeField(null=True, blank=True, verbose_name='推送时间')
    created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='创建时间')
