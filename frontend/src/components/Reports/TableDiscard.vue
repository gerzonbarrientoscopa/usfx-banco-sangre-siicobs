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
    <el-table-column :label="$t('models.release.register_at')" align="center" fixed prop="register_at" width="100px">
      <template slot-scope="scope">
        <span>{{ scope.row.register_at | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.code')" align="center" width="100px">
      <template slot-scope="scope">
        <span>
          <strong>{{ scope.row.itemfragmentation.fragmentation.extraction ? '': 'F-' }}{{ scope.row.itemfragmentation.donor_code }}</strong>
        </span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.hemocomponent')" align="center" width="260px">
      <template slot-scope="scope">
        <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.extraction_date')" align="center" width="160px">
      <template slot-scope="scope">
        <span v-if="scope.row.itemfragmentation.fragmentation.extraction">
          {{ scope.row.itemfragmentation.fragmentation.extraction.register_at | toHumanDate }}
        </span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.expiration_date')" align="center" width="160px">
      <template slot-scope="scope">
        <span>{{ scope.row.itemfragmentation.expiration_date | toHumanDate }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.observations')" align="center" width="155px">
      <template slot-scope="scope">
        <span>{{ scope.row.observations }}</span>
      </template>
    </el-table-column>
    <el-table-column :label="$t('models.release.employee')" align="center">
      <template slot-scope="scope">
        <span>{{ scope.row.employee | fullName }}</span>
      </template>
    </el-table-column>
  </el-table>

</template>

<script>

export default {
  name: 'TableDiscard',
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
