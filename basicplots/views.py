from django.shortcuts import render, get_object_or_404
from basicplots.form import basic_plots_form
from dataUpload.models import Task
from .models import basicplotsclass
from django.views import View

# Create your views here


def plots(request):

    curr_fileId = request.session['file_id']
    print("----------current file id:-----------", curr_fileId)

    try:
        inst = basicplotsclass.objects.get(data_upload=curr_fileId)

        form = basic_plots_form(request.POST, inst)
    except basicplotsclass.DoesNotExist:
        form = basic_plots_form(request.POST)

    #form.fields['cell_filtering_methods'].initial = 'min_gen'
    # form.fields['Cell_Filtering_Paramter_value'].initial = 200
    # form.fields['gene_filtering_methods'].initial = 'min_cell'
    # form.fields['Gene_Filtering_Paramter_value'].initial = 3

    if request.method == 'POST':

        #print('Printing POST:',request.POST)

        if form.is_valid():
            # print("%%%%%%%%%%",form.cleaned_data)
            try:
                if basicplotsclass.objects.get(data_upload=curr_fileId):
                    print("Printing form data: ",
                          form.cleaned_data['basic_plots'])
                    basicplotsclass.objects.filter(data_upload=curr_fileId).update(
                        basic_plots=form.cleaned_data['basic_plots'])

            except basicplotsclass.DoesNotExist:
                form.save()
            #print("-------accessing through foreign key:--------", form.data_upload_id)

    adata = obj.generate_adata()
    print("adata content for the first time:", adata)
    df = adata.to_df()
    rows = df.shape[0]
    counts_per_cell = np.array(df.sum(axis=1))
    counts_per_gene = np.array(df.sum(axis=0))
    genes_per_cell = np.count_nonzero(df, axis=1)
    cells_per_gene = np.count_nonzero(df, axis=0)

    res = {}
    res['histograms'] = {}
    res['scatterplots'] = {}
    res['histograms']['counts_per_cell'] = {
        "xlabel": "log10(counts_per_cell+1)", "ylabel": "frequency", "title": "Counts Per Cell", "data": np.log10(counts_per_cell + 1).tolist()}
    res['histograms']['genes_per_cell'] = {
        "xlabel": "log10(genes_per_cell+1)", "ylabel": "frequency", "title": "Genes Per Cell", "data": np.log10(genes_per_cell + 1).tolist()}
    res['histograms']['counts_per_gene'] = {
        "xlabel": "log10(counts_per_gene+1)", "ylabel": "frequency", "title": "Counts Per Gene", "data": np.log10(counts_per_gene + 1).tolist()}
    res['histograms']['cells_per_gene'] = {
        "xlabel": "log10(cells_per_gene+1)", "ylabel": "frequency", "title": "Cells Per Gene", "data": np.log10(cells_per_gene + 1).tolist()}

    genes_per_cell.sort()
    res['scatterplots']['ordered_genes_per_cell'] = {"xlabel": "cell", "ylabel": "sort(genes_per_cell)", "yscale": "log", "title": "genes per cell (ordered)", "data": {
        "x": rows, "y": genes_per_cell.tolist()}}

    mito_genes = np.array(df.columns[df.columns.str.startswith("MT-")])
    mito_gene_read_counts = np.array(df[mito_genes].sum(axis=1))
    pct_mito = mito_gene_read_counts / counts_per_cell * 100
    pct_mito.sort()

    res['scatterplots']['mitochondrial_counts'] = {"xlabel": "cells sorted by percentage mitochondrial counts",
                                                   "ylabel": "percentage mitochondrial counts", "title": "Mitochondrial Content", "data": {"x": rows, "y": pct_mito.tolist()}}

    adata.write(obj.path_to_cache)
    print("adata content after plotting histogram and sctterplots:", adata)
    # return res

    return render(request, "basicplots/basicplots.html", {'form': form})
