
from django.db import models
from capfore.dbgets import getNow

# Create your models here.

TASK_STATUS = (
    ('Created','Created'),
    ('DOING', 'DOING'),
    ('DONE', 'DONE'),
)



class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='Quick Task')
    curdate = models.DateField(verbose_name='当前数据时间点',default = getNow())
    period = models.IntegerField(verbose_name='预测周期',default =1)
    status = models.CharField(choices=TASK_STATUS, default='Created', max_length=100)
    progress = models.FloatField(default = 0 )
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id) + ':' + self.name


class Cell(models.Model):
    task = models.ForeignKey('Task',related_name='cells', on_delete=models.CASCADE)
    cgi = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20, null=True)
    indoor = models.CharField(max_length=20, null=True)
    scene1 = models.CharField(max_length=200, null=True)
    scene2 = models.CharField(max_length=200, null=True)
    scene3 = models.CharField(max_length=200, null=True)
    band = models.CharField(max_length=20, null=True)
    long = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    erab_nbrmeanestab = models.FloatField(null=True)
    erab_nbrsuccestab = models.FloatField(null=True)
    erab_upoctdl = models.FloatField(null=True)
    packagetype = models.CharField(max_length=20, null=True)
    isneededexpansion = models.CharField(max_length=20, null=True)
    f = models.FloatField(null=True)
    rrc_connmean = models.FloatField(null=True)
    rrc_connmean_nowlist = models.CharField(max_length=200 , null=True)
    rrc_connmean_oldlist = models.CharField(max_length=200, null=True)
    rrc_connmean_old = models.FloatField(null=True)
    rrc_connmean_e = models.FloatField(null=True)
    rrc_connmean_forelist =  models.CharField(max_length=200, null=True)
    rrc_connmean_factorlist = models.CharField(max_length=200, null=True)
    rrc_connmean_predict = models.FloatField(null=True)
    prb_dlutilization = models.FloatField(null=True)
    prb_dlutilization_nowlist = models.CharField(max_length=200 , null=True)
    prb_dlutilization_oldlist = models.CharField(max_length=200, null=True)
    prb_dlutilization_old = models.FloatField(null=True)
    prb_dlutilization_e = models.FloatField(null=True)
    prb_dlutilization_forelist =  models.CharField(max_length=200, null=True)
    prb_dlutilization_factorlist = models.CharField(max_length=200, null=True)
    prb_dlutilization_predict = models.FloatField(null=True)
    prb_ulutilization = models.FloatField(null=True)
    prb_ulutilization_nowlist = models.CharField(max_length=200 , null=True)
    prb_ulutilization_oldlist = models.CharField(max_length=200, null=True)
    prb_ulutilization_old = models.FloatField(null=True)
    prb_ulutilization_e = models.FloatField(null=True)
    prb_ulutilization_forelist =  models.CharField(max_length=200, null=True)
    prb_ulutilization_factorlist = models.CharField(max_length=200, null=True)
    prb_ulutilization_predict = models.FloatField(null=True)
    pdcp_upoctdl = models.FloatField(null=True)
    pdcp_upoctdl_nowlist = models.CharField(max_length=200 , null=True)
    pdcp_upoctdl_oldlist = models.CharField(max_length=200, null=True)
    pdcp_upoctdl_old = models.FloatField(null=True)
    pdcp_upoctdl_e = models.FloatField(null=True)
    pdcp_upoctdl_forelist =  models.CharField(max_length=200, null=True)
    pdcp_upoctdl_factorlist = models.CharField(max_length=200, null=True)
    pdcp_upoctdl_predict = models.FloatField(null=True)
    pdcp_upoctul = models.FloatField(null=True)
    pdcp_upoctul_nowlist = models.CharField(max_length=200 , null=True)
    pdcp_upoctul_oldlist = models.CharField(max_length=200, null=True)
    pdcp_upoctul_old = models.FloatField(null=True)
    pdcp_upoctul_e = models.FloatField(null=True)
    pdcp_upoctul_forelist =  models.CharField(max_length=200, null=True)
    pdcp_upoctul_factorlist = models.CharField(max_length=200, null=True)
    pdcp_upoctul_predict = models.FloatField(null=True)
    rrc_effectiveconnmean = models.FloatField(null=True)
    rrc_effectiveconnmean_nowlist = models.CharField(max_length=200 , null=True)
    rrc_effectiveconnmean_oldlist = models.CharField(max_length=200, null=True)
    rrc_effectiveconnmean_old = models.FloatField(null=True)
    rrc_effectiveconnmean_e = models.FloatField(null=True)
    rrc_effectiveconnmean_forelist =  models.CharField(max_length=200, null=True)
    rrc_effectiveconnmean_factorlist = models.CharField(max_length=200, null=True)
    rrc_effectiveconnmean_predict = models.FloatField(null=True)




class PackageThreshold(models.Model):
    task = models.ForeignKey('Task', related_name='packages', on_delete=models.CASCADE)
    packagethreshold_text = models.CharField(max_length=100)
    threshold_rrc = models.FloatField()
    threshold_prb_utilization = models.FloatField()
    threshold_upoct = models.FloatField()

class CityAttribute(models.Model):
    task = models.ForeignKey('Task', related_name='citys', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    user_activty = models.FloatField()

class SceneAttribute(models.Model):
    task = models.ForeignKey('Task', related_name='scenes', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    scene = models.CharField(max_length=100)
    guaranteed_bandwidth = models.FloatField()
    rrc_growth_rate = models.FloatField()

# class Snippet(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default='')
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#     owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ('created',)