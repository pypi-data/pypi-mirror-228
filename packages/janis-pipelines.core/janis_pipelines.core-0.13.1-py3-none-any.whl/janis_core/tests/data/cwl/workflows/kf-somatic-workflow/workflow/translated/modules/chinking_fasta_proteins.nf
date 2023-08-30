nextflow.enable.dsl=2

process CHINKING_FASTA_PROTEINS {
    debug true
    container "ubuntu:latest"
    publishDir "${params.outdir}/after_qc/chunking_final/chinking_fasta_proteins"

    input:
    path infile

    output:
    path "{inputs.outdirname}/*", emit: chunks

    script:
    def infile = infile.join(' ')
    def type_fasta = params.after_qc.chunking_final.chinking_fasta_proteins_type_fasta ? "-t ${params.after_qc.chunking_final.chinking_fasta_proteins_type_fasta}" : ""
    """
    run_result_file_chunker.py \
    -i ${infile} \
    -f ${params.after_qc.chunking_final.chinking_fasta_proteins_format_file} \
    -o ${params.after_qc.chunking_final.chinking_fasta_proteins_outdirname} \
    ${type_fasta} \
    """

}


process CHINKING_FASTA_PROTEINS {
    debug true
    container "ubuntu:latest"
    publishDir "${params.outdir}/after_qc/chunking_final/chinking_fasta_proteins"

    input:
    path infile

    output:
    path "{inputs.outdirname}/*", emit: chunks

    script:
    def infile = infile.join(' ')
    def type_fasta = params.after_qc.chunking_final.chinking_fasta_proteins_type_fasta ? "-t ${params.after_qc.chunking_final.chinking_fasta_proteins_type_fasta}" : ""
    """
    run_result_file_chunker.py \
    -i ${infile} \
    -f ${params.after_qc.chunking_final.chinking_fasta_proteins_format_file} \
    -o ${params.after_qc.chunking_final.chinking_fasta_proteins_outdirname} \
    ${type_fasta} \
    """

}
