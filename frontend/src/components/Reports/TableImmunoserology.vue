<template>
  <el-table
    :key="tableKey"
    v-loading="loading"
    :data="list"
    fit
    border
    highlight-current-row
    style="width: 100%;"
  >
    <el-table-column :label="$t('models.immunoserology.register_at')" align="center" fixed width="120px">
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.code')" align="center" width="100px">
      <template slot-scope="scope">
        <span>{{ scope.row.donation.donor.code }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.chagas_hai')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.chagas_hai === 'R' }">{{ scope.row.chagas_hai | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.cheia')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.cheia === 'R' }">{{ scope.row.cheia | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.rpr')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.rpr === 'R' }">{{ scope.row.rpr | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.hvc')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.hvc === 'R' }">{{ scope.row.hvc | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.hbsag')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.hbsag === 'R' }">{{ scope.row.hbsag | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.hiv')" align="center" width="120px">
      <template slot-scope="scope">
        <p :class="{ 'text_red': scope.row.hiv === 'R' }">{{ scope.row.hiv | typeReactFilter }}</p>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.immunoserology.employee')" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.employee | fullName }}</span>
      </template>
    </el-table-column>
  </el-table>

</template>

<script>
import { TYPE_REACT_OPTIONS } from '@/utils/const'

const typeReactKeyValue = TYPE_REACT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TableImmunoserology',
  filters: {
    typeReactFilter(type) {
      return typeReactKeyValue[type]
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
