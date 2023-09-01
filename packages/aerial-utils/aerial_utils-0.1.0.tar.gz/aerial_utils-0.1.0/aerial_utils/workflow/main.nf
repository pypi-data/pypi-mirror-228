nextflow.enable.dsl=2

/*
#==============================================
WAL_YAN/BED_FILTER
#==============================================
*/


include { BEDTOOLS_INTERSECT as BED_FILTER } from './modules/nf-core/bedtools/intersect/main'                                         


workflow bed_filter {

        ch_in_bedtools = Channel.fromPath( params.input )
                            .splitCsv(header: false, skip: 1)
                            .map{ row -> 
                                    {
                                        sampleName          = row[0]
                                        bedGraphFile        = row[1]

                                        return tuple([id:sampleName], bedGraphFile)
                                    }
                                }

        BED_FILTER (ch_in_bedtools, params.bed)

}

/*
#==============================================
WAL_YAN/PICARD_PROFILER
#==============================================
*/


