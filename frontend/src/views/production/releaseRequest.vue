<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('models.patient.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_releaserequest'])"
        class="filter-item"

        style="margin-left: 10px;"
        type="primary"
        @click="handleCreate"
      >{{ $t('add') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      stripe
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.releaseRequest.register_at')" align="center" width="170px">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.releaseRequest.attendant')" width="270px">
        <template slot-scope="scope">
          <span>{{ scope.row.attendant | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.releaseRequest.medical')" width="270px">
        <template slot-scope="scope">
          <span>{{ scope.row.medical | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.releaseRequest.description')" width="250px">
        <template slot-scope="scope">
          <span>{{ scope.row.description }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.releaseRequest.status')" align="center" width="150px">
        <template slot-scope="scope">
          <span>
            <el-tag :type="getStatus(scope.row.status)">{{ scope.row.status | statusFilter }}</el-tag>
          </span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.releaseRequest.employee')" width="270px">
        <template slot-scope="scope">
          <span>{{ scope.row.employee | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="150px">
        <template slot-scope="scope">
          <el-tooltip :content="$t('edit')" :enterable="false" class="item" effect="dark">
            <el-button v-if="checkPermission(['change_releaserequest'])" size="mini" @click="handleUpdate(scope.row)"><font-awesome-icon icon="edit" /></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-show="total>0"
        :current-page="listQuery.page"
        :page-size="listQuery.limit"
        :page-sizes="[10,20,30, 50]"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" :width="widthDialog" destroy-on-close>
      <el-row :gutter="20">
        <el-col :md="24">
          <div class="grid-content">
            <release-request-form :row="temp" @dialogStatus="handleCloseForm" />
          </div>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import ReleaseRequestForm from './releaseRequestForm'
import { graphqlRequest } from '@/api/graphql'
import releaseRequests from '@/query/releaseRequest'
import { debounce } from 'debounce'

const statusOptions = [
  { key: 1, display_name: 'NUEVO' },
  { key: 2, display_name: 'EN PROCESO' },
  { key: 3, display_name: 'LIBERADO' }
]

const statusTypeKeyValue = statusOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ReleaseRequest',
  components: { ReleaseRequestForm },
  filters: {
    statusFilter(type) {
      return statusTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-register_at' },
      temp: { id: undefined },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: { update: 'Modificando Solicitud de Liberacion', create: 'Agregando Solicitud de Liberacion' },
      downloadLoading: false,
      dialogShowVisible: false,
      widthDialog: null
    }
  },
  watch: {},
  created() {
    this.getList()
  },
  methods: {
    checkPermission,
    getStatus(x) {
      if (x === 2) return 'warning'
      else if (x === 3) return 'success'
      return ''
    },
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'release-requests',
          query: releaseRequests.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.releaserequests.results
        this.total = data.releaserequests.totalCount
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
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.widthDialog = '80%'
      this.temp = null
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.widthDialog = '80%'
      this.temp = row
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    }
  }
}
</script>
