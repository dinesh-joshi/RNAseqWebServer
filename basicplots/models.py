from django.db import models
from dataUpload.models import Task


class basicplotsclass(models.Model):

    data_upload = models.OneToOneField(
        Task, on_delete=models.CASCADE, primary_key=True)

    Basic_Plots_Choices = [('cts_per_cell', 'counts per cell'), ('gen_per_cell', 'genes per cell'), ('cts_per_gen', 'counts per gene'),
                           ('cells_per_gen', 'cells per gene'), ('gen_per_cell_ord', 'gene per cell (Ordered)'), ('mito_cont', 'mitochondrial content')]

    basic_plots = models.CharField(
        max_length=30,
        choices=Basic_Plots_Choices,
        default='cts_per_cell',

    )
