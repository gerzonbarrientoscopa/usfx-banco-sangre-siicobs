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
    <el-table-column :label="$t('models.order.id')" align="center" width="70px" fixed>
      <template slot-scope="scope">
        <span>{{ scope.row.code }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.order.register_at')" align="center" width="150px">
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.order.employee')">
      <template slot-scope="scope">
        <span>{{ scope.row.receiver | fullName }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.order.quantity')" width="150" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.items.length }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.order.state')" width="155px" align="center">
      <template slot-scope="scope">
        <el-tag :type="getColorState(scope.row.state)">{{ scope.row.state | stateFilter }}</el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
const stateOptions = [
  { key: 0, display_name: 'NUEVO' },
  { key: 1, display_name: 'EN PROCESO' },
  { key: 2, display_name: 'ENTREGADO' },
  { key: 3, display_name: 'CANCELADO' }
]
const stateKeyValue = stateOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'TableOrder',
  filters: {
    stateFilter(type) {
      return stateKeyValue[type]
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
  },
  methods: {
    getColorState(state) {
      switch (state) {
        case 0:
          return ''
        case 1:
          return 'warning'
        case 2:
          return 'success'
        case 3:
          return 'danger'
      }
    }
  }
}
</script>

<style scoped>

</style>
