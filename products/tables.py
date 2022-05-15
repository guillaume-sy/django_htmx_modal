import django_tables2 as tables
from .models import Factory


class FactoryTable(tables.Table):

    class Meta:
        model = Factory
        fields = ['factory_name', 'factory_reg_date', 'id']
        template_name = "table/factory_table.html"
