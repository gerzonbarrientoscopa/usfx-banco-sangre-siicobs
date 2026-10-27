def get_results_serology(immunoserology):
    partial_result = immunoserology.chagas_hai == 'NR' and immunoserology.cheia == 'NR' and immunoserology.rpr == 'NR' and immunoserology.hvc == 'NR' \
                     and immunoserology.hbsag == 'NR' and immunoserology.hiv == 'NR'

    return partial_result
