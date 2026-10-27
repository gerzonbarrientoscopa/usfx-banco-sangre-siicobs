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
    <el-table-column :label="$t('models.purchase.register_at')" width="150" align="left" fixed>
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.purchase.employee')" align="left">
      <template slot-scope="scope">
        <span>{{ scope.row.employee | fullName }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.purchase.quantity')" width="150" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.items.length }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: 'TablePurchase',
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
