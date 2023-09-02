# Bed tools style wrapper to create training regions
import pysam
import logging
import re


class FakeVariantHeader(object):
    def __init__(self):
        self.samples = ["fake_sample"]


class FakeVariantFile(object):
    def __init__(self):
        self.header = FakeVariantHeader()
        
    def fetch(self, chrom, start, end):
        return []


class EdsTool(object):
    def __init__(self, regions):
        with open(regions) as regions_fp:
            self.regions = [re.split(':|-|\t', x.strip("\n")) for x in regions_fp.readlines()]
        self.regions = [(x[0], int(x[1]), int(x[2])) for x in self.regions]
        self.sequences = None  # list of sequences
        
    def sequence(self, fi, vcf=None, sample=None):
        genome_file = pysam.FastaFile(fi)
        variant_file = pysam.VariantFile(vcf) if vcf else FakeVariantFile()
        self.sequences = []

        if sample is None:
            # Using first sample from VCF
            sample = variant_file.header.samples[0]

        for region in self.regions:
            seq = genome_file.fetch(*region).upper()
            indent = -region[1]
            
            for v in variant_file.fetch(*region):
                filter_keys = v.filter.keys()
                if len(filter_keys) and 'PASS' not in v.filter.keys():
                    continue
                if not v.alts:
                    continue
                if v.alts == tuple(["<NON_REF>"]):
                    continue
                if "AD" not in v.samples[sample]:
                    continue
                
                # Get allele index of max value. Default to reference on matches
                allelic_depths = list(v.samples[sample]["AD"])
                haplotype_index = allelic_depths.index(max(allelic_depths))
                
                alt = v.alleles[haplotype_index]
                if  v.ref != seq[v.start + indent:v.stop + indent]:
                    logging.warning(
                        "inconsistency: {}:{} {} != {}".format(v.chrom, v.pos, v.ref, seq[v.start + indent:v.stop + indent])
                    )
                
                seq = seq[:v.start + indent] + alt + seq[v.stop + indent:]
                indent = indent + len(alt) - len(v.ref)
            
            self.sequences.append(seq)
            
        return self

