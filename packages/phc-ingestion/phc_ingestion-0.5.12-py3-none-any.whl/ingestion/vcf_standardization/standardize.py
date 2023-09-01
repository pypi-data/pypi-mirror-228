from typing import Iterator

from ingestion.vcf_standardization.util.read_write import read_vcf, add_to_headers, write_vcf
from ingestion.vcf_standardization.Variant import check_formatting
from logging import Logger

# TO DO: Add optional VENDSIG processing for supported vendors


def standardize_vcf(infile: str, outfile: str, out_path: str, case_id: str, log: Logger):
    approved_chr_list = [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]
    approved_chr_list = approved_chr_list + ["chr" + i for i in approved_chr_list]
    compression = False
    if infile.endswith(".gz"):
        compression = True

    line_count, headers, variants = read_vcf(infile, log)

    def variant_gen() -> Iterator[str]:
        for variant in variants:
            # Ignore structural variants
            if "SVTYPE" in variant:
                continue
            # Working variant
            wv = check_formatting(variant)
            if wv.chr not in approved_chr_list:
                continue

            if "AD" in wv.frmt:
                wv.ad_af_dp.update({"AD": wv.smpl[wv.frmt.index("AD")]})

            wv.standardize_allele_frequency(log)

            wv.standardize_depth(log)

            wv.standardize_allelic_depth(log)

            updated_variant = wv.reassemble_variant()

            yield updated_variant

    standardized_headers = add_to_headers(headers, case_id)

    write_vcf(standardized_headers, variant_gen(), f"{out_path}/{outfile}", compression, log)

    return line_count
