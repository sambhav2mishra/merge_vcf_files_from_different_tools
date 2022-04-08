# merge_vcf_files_from_different_tools

An application in Python to merge these vcf files into a single VCF file, so that overlapping variants are present only once in the output file. 

While merging:
A new tag in the INFO field of each variant , named ‘calledBy’ was added, that has name of the tool which called the variant. If a variant is called by both tools, set value as ‘calledBy=Freebayes+VarScan’.
For the common variants, any common INFO and FORMAT tags annotated by both tools by prefixing the tool name in the name of the tag was renamed. Ex: if ‘DP’ tag is annotated by both callers, rename the tags as ‘Freebayes_DP’ and ‘VarScan_DP’ while merging.
