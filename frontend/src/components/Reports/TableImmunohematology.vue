<template>
  <el-table
    :key="tableKey"
    v-loading="loading"
    :data="list"
    border
    fit
    highlight-current-row
    style="width: 100%;"
  >
    <el-table-column :label="$t('models.immunohematology.register_at')" align="center" fixed width="120px">
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.code')" align="center" width="100px">
      <template slot-scope="scope">
        <span>{{ scope.row.donation.donor.code }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.direct_abo')" align="center" width="100px">
      <template slot-scope="scope">
        <span :inner-html.prop="scope.row.direct_abo | bloodGroupToHtml" />
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.factor_rh')" align="center" width="100px">
      <template slot-scope="scope">
        {{ scope.row.factor_rh | rhOptionsFilter }}
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.antikell')" align="center" width="95px">
      <template slot-scope="scope">
        <span>{{ scope.row.antikell | optionsGeneral }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.fsi')" align="center" width="85px">
      <template slot-scope="scope">
        <span>{{ scope.row.fsi | optionsGeneral }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.liss')" align="center" width="85px">
      <template slot-scope="scope">
        <span>{{ scope.row.liss | optionsGeneral }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.alb')" align="center" width="85px">
      <template slot-scope="scope">
        <span>{{ scope.row.alb | optionsGeneral }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.coombs')" align="center" width="85px">
      <template slot-scope="scope">
        <span>{{ scope.row.coombs | optionsGeneral }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.exist_irregular_antibody')" align="center" width="85px">
      <template slot-scope="scope">
        <span>{{ scope.row.exist_irregular_antibody ? 'POSITIVO': 'NEGATIVO' }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunohematology.employee')" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.employee | fullName }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { RH_OPTIONS } from '@/utils/const'

const rhOptionKeyValue = RH_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TableImmunohematology',
  filters: {
    rhOptionsFilter(type) {
      return rhOptionKeyValue[type]
    },
    optionsGeneral(type) {
      if (type === '-') {
        return 'NEG'
      }
      return type
    }
  },
  props: {
    list: {
      type: Array,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableKey: 0
    }
  }
}
</script>

<style scoped>

</style>
