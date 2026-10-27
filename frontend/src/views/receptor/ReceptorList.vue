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
        v-if="checkPermission(['add_patient'])"
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
      :default-sort="{prop: 'first_name', order: 'ascending'}"
      border
      fit
      highlight-current-row
      stripe
      style="width: 100%;"
      @sort-change="handleOrderChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column :label="$t('models.patient.first_name')" min-width="170px">
        <template slot-scope="scope">
          <span>{{ scope.row.first_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.middle_name')" prop="middle_name">
        <template slot-scope="scope">
          <span>{{ scope.row.middle_name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.patient.last_name')" prop="last_name">
        <template slot-scope="scope">
          <span>{{ scope.row.last_name }}</span>
        </template>
      </el-table-column>

      <el-table-column
        :label="$t('actions')"
        align="center"
        fixed="right"
        width="180px"
      >
        <template slot-scope="scope">
          <el-button-group>
            <el-tooltip :content="$t('edit')" :enterable="false" class="item" effect="dark">
              <el-button v-if="checkPermission(['change_patient'])" size="mini" @click="handleUpdate(scope.row)"><font-awesome-icon icon="edit" /></el-button>
            </el-tooltip>
            <el-button
              v-if="$route.name === 'registry-fast' || $route.name === 'distribution-fast'"
              size="mini"
              type="primary"
              @click="handleSelected(scope.row)"
            >Seleccionar
            </el-button>
          </el-button-group>
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
            <receptor-form v-if="dialogStatus !== 'join'" :row="temp" @dialogStatus="handleCloseForm" />
          </div>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import ReceptorForm from './ReceptorForm'
import Cookies from 'js-cookie'
import { graphqlRequest } from '@/api/graphql'
import patients from '@/query/patient'
import { debounce } from 'debounce'

export default {
  name: 'ReceptorList',
  components: { ReceptorForm },
  directives: {},
  filters: {
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
      textMap: { update: 'Modificando Receptor', create: 'Agregando Receptor' },
      downloadLoading: false,
      dialogShowVisible: false,
      widthDialog: null,
      multipleSelection: [],
      buttonJoin: true
    }
  },
  watch: {
    multipleSelection: function(value) {
      this.buttonJoin = value.length <= 1
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
          service: 'patients',
          query: patients.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.patients.results
        this.total = data.patients.totalCount
        this.listLoading = false
      })
    },
    handleFilter: debounce(function() {
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
    handleOrderChange(val) {
      if (val['prop']) {
        this.listQuery.ordering = (val['order'] === 'descending' ? '-' : '') + val['prop']
        this.getList()
      }
    },
    handleCreate() {
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.widthDialog = '60%'
      this.temp = null
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.widthDialog = '60%'
      this.temp = row
    },
    handleShowDetail(row) {
      this.temp = row
      this.dialogShowVisible = true
    },
    handleCloseDetail() {
      this.dialogShowVisible = false
      this.temp = null
    },
    handleSelected(row) {
      const receptor = {
        id: row.id,
        first_name: row.first_name,
        middle_name: row.middle_name,
        last_name: row.last_name
      }
      Cookies.set('donationReceptor', receptor)
      Cookies.set('distributionReceptor', receptor)
      const h = this.$createElement

      this.$message({
        showClose: true,
        message: h('p', null, [
          h('span', null, 'Paciente Seleccionado: '),
          h('b', null, row.first_name + ' ' + row.middle_name + ' ' + row.last_name)
        ]),
        type: 'success'
      })
      this.$emit('selectedReceptor', false)
    },
    handleCloseForm() {
      if (this.dialogStatus === 'join') {
        this.$refs.Receptor.buttonJoin = true
      }
      this.dialogFormVisible = false
      this.getList()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    }
  }
}
</script>
