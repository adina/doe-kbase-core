library(phyloseq)
metadata = read.delim(file="./meta.txt", row.names = 1, sep="\t", header=TRUE)
abund <- read.delim(sep='\t', file="./merged.out",header=TRUE, strip.white=TRUE, row.names=1)
abund_core <- abund[apply(abund, MARGIN=1, function(x) all(x > 0)),]
abund_matrix <- as.matrix(abund_core)
abundance <- otu_table(abund_matrix, taxa_are_rows=TRUE)
metadata <- sample_data(metadata)
metag <- phyloseq(metadata, abundance)
save(metag, file = "metag.RData")