import pysam
import os

from unittest import TestCase
from eds_tools import EdsTool
from pysam import VariantFile, FastaFile, VariantHeader, tabix_index, FastaFile
from tempfile import TemporaryDirectory



class TryTesting(TestCase):
    def test_with_snps_and_indel(self):
        sample_name = "EDS_TOOL"
        
        vcfh = VariantHeader()
        vcfh.add_meta('contig', items=[('ID', "chr1"), ("assembly", "hg38"), ("species", "Homo Sapiens")])
        vcfh.add_meta('ALT', items=[('ID',"NON_REF"), ('Description','blah blah')])
        vcfh.add_meta('FILTER', items=[('ID',"LowQual"), ('Description','Low quality')])
        vcfh.add_meta('FORMAT', items=[('ID',"AD"), ('Number', 'R'), ('Type', 'Integer'), ('Description','Low quality')])
        vcfh.add_sample(sample_name)
        
        contig = "chr1"
        with TemporaryDirectory() as tmpdirname:
            vcf_filename = os.path.join(tmpdirname, "test.vcf.gz")
            with VariantFile(vcf_filename, "w", header=vcfh) as vcf:
                new_record = vcf.new_record(contig=contig, start=0, stop=1, alleles=('A', 'T'))
                new_record.samples[sample_name]['AD'] = (9, 10)
                vcf.write(new_record)
                
                new_record = vcf.new_record(contig=contig, start=1, stop=2, alleles=('T', 'A'))
                new_record.samples[sample_name]['AD'] = (20, 10)
                vcf.write(new_record)
                
                new_record = vcf.new_record(contig=contig, start=3, stop=4, alleles=('A', 'ACCC'))
                new_record.samples[sample_name]['AD'] = (9, 10)
                vcf.write(new_record)
                
                new_record = vcf.new_record(contig=contig, start=6, stop=9, alleles=('ATG', 'A'))
                new_record.samples[sample_name]['AD'] = (9, 10)
                vcf.write(new_record)
            

            tabix_index(vcf_filename, preset="vcf", force=True)
            
            regions_filepath = os.path.join(tmpdirname, "regions.txt")
            with open(regions_filepath, 'w') as fp:
                fp.write("chr1:0-10\n")
            
            genome_filepath = os.path.join(tmpdirname, "genome.fa")
            
            chrom1 = "ATG" * 5
            with open(genome_filepath, 'w') as fp:
                fp.write(">chr1\n")
                fp.write(chrom1 + "\n")
            
            with open(genome_filepath + ".fai", 'w') as fp:
                fp.write("chr1\t{}\t5\t{}\t{}".format(len(chrom1), len(chrom1), len(chrom1) + 1))
            
            genome_file = FastaFile(genome_filepath)
            
            py_eds_tool = EdsTool(regions_filepath)

            py_eds_tool = py_eds_tool.sequence(
                fi= genome_filepath,
                vcf=vcf_filename
            )
            sequences = py_eds_tool.sequences
            self.assertEqual(sequences[0], "TTGACCCTGAA")

