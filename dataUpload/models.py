from sys import flags
from django.db import models
import uuid
import tarfile
import os
import scanpy as sc
from RNAseqWebServer import settings
from RNAseqWebServer.settings import BASE_UPLOAD_PATH

PATH = BASE_UPLOAD_PATH + "media"
CACHE_PATH = BASE_UPLOAD_PATH+"cache"


def task_directory_path(instance, filename):
    return 'task_{0}/{1}'.format(instance.task_id, filename)


class Task(models.Model):
    file_id = models.AutoField(primary_key=True)
    task_id = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(blank=False, null=False,
                            upload_to=task_directory_path)
    path_to_tar = models.CharField(max_length=1000, default="")

    def adata(): return None
    path_to_cache = models.CharField(max_length=1000, default="")

    def extract(self, filename):

        path_to_tar = os.path.join(PATH, filename)
        file = tarfile.open(path_to_tar)
        file.extractall(os.path.dirname(path_to_tar))
        file.close()
        return path_to_tar

    def generate_adata(self):
        data_path = [f.path for f in os.scandir(os.path.dirname(
            self.path_to_tar)+"/filtered_gene_bc_matrices") if f.is_dir()][0]
        self.adata = sc.read_10x_mtx(
            data_path, var_names='gene_symbols', cache=True)
        path = PATH[:0]+PATH[1:]
        self.path_to_cache = CACHE_PATH+"/"+path.replace("/", "-")+"-"+"task_" + str(
            self.task_id) + "-"+"filtered_gene_bc_matrices-hg19-matrix.h5ad"
        print(self.path_to_cache)
        return self.adata
