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
      :row-class-name="tableRowClassName"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.rejected.register_at')" fixed width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDate }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.donor.code')" width="155px" align="center">
        <template slot-scope="scope">
          <strong>
            {{ scope.row.donation.donor.code }}
          </strong>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.exam.donation')" width="300px" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.donation.donor | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.reason.type')" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.reason.type | typeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.rejected.reason')" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.reason.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.rejected.resource')" width="200px">
        <template slot-scope="scope">
          <span>{{ scope.row.resource | resourceFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="120"
        class-name="small-padding"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['delete_rejected']) && scope.row.status!=='deleted'"
            size="mini"
            @click="handleDelete(scope.row)"
          >{{ $t('delete') }}
          </el-button>
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
import rejecteds from '@/query/rejected'
import { debounce } from 'debounce'

const typeOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]

const typeKeyValue = typeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const resourceOptions = [
  { key: 'Exam', display_name: 'PRE-TAMIZAJE' },
  { key: 'PhysicalAnalysis', display_name: 'ANALISIS FISICO' },
  { key: 'ClinicalHistory', display_name: 'HISTORIA CLINICA' }
]

const resourceKeyValue = resourceOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Rejected',
  components: {},
  directives: {},
  filters: {
    typeFilter(type) {
      return typeKeyValue[type]
    },
    resourceFilter(type) {
      return resourceKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id' },
      showReviewer: false,
      for_loop: 0,
      temp: { id: undefined, name: '' },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Modificando Tipo de Solucion',
        create: 'Creando Tipo de Solucion'
      },
      rules: {
        name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    tableRowClassName({ row, rowIndex }) {
      if (row.reason.type === 'PE') {
        return 'warning-row'
      }

      return ''
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: rejecteds.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.rejecteds.results
        this.total = data.rejecteds.totalCount
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
    handleDelete(row) {
      this.$confirm(this.$t('messageConfirmDelete'), 'Confirmación', {
        confirmButtonText: this.$t('confirmButtonText'),
        cancelButtonText: this.$t('cancelButtonText'),
        type: 'warning'
      }).then(() => {
        const tempData = Object.assign({}, row)
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'deleteRejected',
            query: rejecteds.deleteRejected(),
            variables: tempData
          }
        ).then(response => {
          if (response.errors) {
            this.$notify({
              title: 'Estado',
              message: response.errors[0].message,
              type: 'error',
              duration: 2000
            })
          } else {
            this.getList()
            this.dialogFormVisible = false
            this.$notify({
              title: 'Estado',
              message: 'Registro eliminado',
              type: 'success',
              duration: 2000
            })
          }
        })
      }).catch(() => {
        // cancel
      })
    }
  }
}
</script>
<style>
  .el-table .warning-row {
    background: #fdc1a9;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>
