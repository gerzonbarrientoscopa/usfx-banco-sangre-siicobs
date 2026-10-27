<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        :placeholder="$t('search')"
        :autofocus="'autofocus'"
        prefix-icon="el-icon-search"
        clearable
        class="filter-item"
        @input="handleFilter"
      />
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.settingPhysical.place')" width="200px" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.place">{{ scope.row.place.name }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.systolic')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.systolic_min }} - {{ scope.row.systolic_max }} mmHg.</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.diastolic')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.diastolic_min }} - {{ scope.row.diastolic_max }} mmHg.</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.pulse')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.pulse_min }} - {{ scope.row.pulse_max }} /min</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.weight_min')" width="150px" align="center">
        <template slot-scope="scope">
          <span> >= {{ scope.row.weight_min }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.hematocrit')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.hematocrit_min }} - {{ scope.row.hematocrit_max }} %</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.settingPhysical.hemoglobin_factor')" width="160px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.hemoglobin_factor }}</span>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-sizes="[10,20,30, 50]"
        :page-size="listQuery.limit"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import settingPhysicals from '@/query/settingPhysical'
import { debounce } from 'debounce'

export default {
  place: 'SettingPhysical',
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: 'place__name'
      },
      temp: {
        id: undefined,
        place_id: undefined,
        hematocrit_min: undefined,
        hematocrit_max: undefined,
        systolic_min: undefined,
        systolic_max: undefined,
        diastolic_min: undefined,
        diastolic_max: undefined,
        pulse_min: undefined,
        pulse_max: undefined,
        weight_min: undefined,
        hemoglobin_factor: undefined
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'setting_physicals',
          query: settingPhysicals.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.settingphysicals.results
        this.total = data.settingphysicals.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function(e) {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getList()
    }, 500),
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Se modifico el estado de una fila',
        type: 'success'
      })
      row.status = status
    }
  }
}
</script>
