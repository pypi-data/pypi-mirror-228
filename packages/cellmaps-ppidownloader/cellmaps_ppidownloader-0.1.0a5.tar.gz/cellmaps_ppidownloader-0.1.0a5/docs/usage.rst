=====
Usage
=====

This page should provide information on how to use cellmaps_ppidownloader

In a project
--------------

To use cellmaps_ppidownloader in a project::

    import cellmaps_ppidownloader

On the command line
---------------------

For information invoke :code:`cellmaps_ppidownloadercmd.py -h`

**Example usage**

The PPI downloader requires the following input files: 

1) bait list file: TSV file of baits used for AP-MS experiments
2) edge list file: TSV file of edges for protein interaction network
3) provenance: file containing provenance information about input files in JSON format (see sample provenance file in examples folder)

.. code-block::

   cellmaps_ppidownloadercmd.py ./cellmaps_ppidownloader_outdir --edgelist examples/edgelist.tsv --baitlist examples/baitlist.tsv --provenance examples/provenance.json

Via Docker
---------------

**Example usage**

.. code-block::

   docker run -v `pwd`:`pwd` -w `pwd` idekerlab/cellmaps_ppidownloadercmd:0.1.0 cellmaps_ppidownloadercmd.py ./cellmaps_ppidownloader_outdir --edgelist examples/edgelist.tsv --baitlist examples/baitlist.tsv --provenance examples/provenance.json


