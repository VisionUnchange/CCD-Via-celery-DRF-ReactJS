from django.contrib.auth.models import User
from rest_framework import serializers

from capfore.models import Task,PackageThreshold, CityAttribute, SceneAttribute,Cell  #, Snippet



class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())
    class Meta:
        model = User
        fields = ('id','username','tasks' )

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = (
            'cgi',
            'name',
            'task_id',
            'scene1',
            'scene2',
            'scene3',
            'band',
            'city',
            'erab_nbrmeanestab',
            'erab_nbrsuccestab',
            'erab_upoctdl',
            'f',
            'indoor',
            'lat',
            'long',
            'packagetype',
            'pdcp_upoctdl',
            'pdcp_upoctdl_e',
            'pdcp_upoctdl_predict',
            'pdcp_upoctul',
            'pdcp_upoctul_e',
            'pdcp_upoctul_predict',
            'prb_dlutilization',
            'prb_dlutilization_e',
            'prb_dlutilization_predict',
            'prb_ulutilization',
            'prb_ulutilization_e',
            'prb_ulutilization_predict',
            'rrc_connmean',
            'rrc_connmean_e',
            'rrc_connmean_predict',
            'rrc_effectiveconnmean',
            'rrc_effectiveconnmean_e',
            'rrc_effectiveconnmean_predict',
            'isneededexpansion',
        )


class TaskSerializer(serializers.ModelSerializer):
    # packages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # citys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # scenes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # cells = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Task
        fields = ('__all__')

class PackageThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageThreshold
        fields = ('__all__')

class CityAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityAttribute
        fields = ('__all__')

class SceneAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SceneAttribute
        fields = ('__all__')
