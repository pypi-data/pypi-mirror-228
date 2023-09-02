# EDSTools -- EvolvedDevelopmentSequenceTools

BEDTools style repository for passing VCF/BED files.

Designed to combined variant calls from peaked data with the reference genome. Returns the genomic sequence of the allele most present in the peak.

Example Usage:

```
import eds_tools

py_eds_tool = eds_tools.EdsTool("/<path>/analysis_regions.txt")

py_eds_tool = py_eds_tool.sequence(
    fi= "/<path>/genome.fa",
    vcf="/<path>/gatk-snp-indel.vcf.gz"
)
sequences = py_eds_tool.sequences
```

To run the unittests please run:

```
cd eds_tools
python -m unittest discover
```
