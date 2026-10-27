<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model.lazy="listQuery.search"
        :autofocus="'autofocus'"
        :placeholder="$t('models.medical.search')"
        class="filter-item"
        clearable
        prefix-icon="el-icon-search"
        style="width: 50%;"
        @input="handleFilter"
      />
      <el-button
        v-if="checkPermission(['add_medical'])"
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
      style="width: 100%;"
    >
      <el-table-column :label="$t('models.medical.register_at')" align="center" fixed width="150px">
        <template slot-scope="scope">
          <span>{{ scope.row.register_at | toHumanDatetime }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.medical.full_name')">
        <template slot-scope="scope">
          <span>{{ scope.row | fullName }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.medical.institution')">
        <template slot-scope="scope">
          <span v-if="scope.row.institution">{{ scope.row.institution.name }}  ({{ scope.row.institution.address }})</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        align="center"
        class-name="small-padding"
        fixed="right"
        width="250px"
      >
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_medical']) && $route.name !== 'phlebotomy-fast'"
            size="mini"
            type="primary"
            @click="handleUpdate(scope.row)"
          >{{ $t('edit') }}</el-button>
          <el-button
            v-if="$route.name === 'phlebotomy-fast' || $route.name === 'distribution-fast'"
            size="mini"
            type="primary"
            @click="handleSelected(scope.row)"
          >Seleccionar
          </el-button>
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

    <el-dialog
      :before-close="handleCloseForm"
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      destroy-on-close
      width="90%"
    >
      <medical-form :row="temp" @dialogStatus="handleCloseForm" />
    </el-dialog>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import permission from '@/directive/permission/index.js'
import MedicalForm from './MedicalForm'
import Cookies from 'js-cookie'
import { graphqlRequest } from '@/api/graphql'
import medicals from '@/query/medical'
import { debounce } from 'debounce'

export default {
  name: 'MedicalList',
  components: { MedicalForm },
  directives: { permission },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', sort: '+id', ordering: '-register_at' },
      temp: {
        id: undefined,
        first_name: '',
        middle_name: '',
        last_name: '',
        institution_id: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Modificando Médico',
        create: 'Creando Médico'
      },
      downloadLoading: false
    }
  },
  watch: {},
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
          query: medicals.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.medicals.results
        this.total = data.medicals.totalCount
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
      this.temp = null
    },
    handleUpdate(row) {
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.temp = row
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    },
    handleSelected(row) {
      Cookies.set('phlebotomyMedical', row)
      Cookies.set('distributionMedical', row)
      this.$message({
        showClose: true,
        message: 'Médico Seleccionado: ' + row.first_name + ' ' + row.middle_name + ' ' + row.last_name + ', Ahora presione siguiente ',
        type: 'success'
      })
      this.$emit('selectedMedical', false)
    }
  }
}
</script>
