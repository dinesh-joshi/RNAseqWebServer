from django import forms

# from dataUpload.models import Task
from . models import basicplotsclass


class basic_plots_form(forms.ModelForm):
    class Meta:
        model = basicplotsclass
        # fields = ("cell_filtering_methods","Cell_Filtering_Parameter_value","gene_filtering_methods",
        # "Gene_Filtering_Parameter_value")
        exclude = ('data_upload',)
