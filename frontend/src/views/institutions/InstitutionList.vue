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
      <el-button
        v-if="checkPermission(['add_institution'])"
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"

        @click="handleCreate"
      >
        {{ $t('add') }}
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
      @selection-change="handleSelectionChange"
    >
      <el-table-column :label="$t('models.institution.name')">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.type')" align="center" width="160px">
        <template slot-scope="scope">
          <span>{{ scope.row.type | institutionTypeValue }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.department')" align="center" width="120px">
        <template slot-scope="scope">
          <span>{{ scope.row.department | departmentOptionsFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.address')" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.address }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('models.institution.phone')" width="100px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('actions')"
        fixed="right"
        align="center"
        width="230"
        class-name="small-padding"
      >
        <template slot-scope="scope">
          <el-button v-if="checkPermission(['change_institution'])" size="mini" @click="handleUpdate(scope.row)">
            {{ $t('edit') }}
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="60%" destroy-on-close>
      <el-row :gutter="20">
        <el-col :md="24">
          <div class="grid-content">
            <institution-form v-if="dialogStatus !== 'join'" :row="temp" @dialogStatus="handleCloseForm" />
            <institution-join v-if="dialogStatus === 'join'" ref="Receptor" :row="multipleSelection" @dialogStatus="handleCloseForm" />
          </div>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import institutions from '@/query/institution'
import InstitutionForm from './InstitutionForm'
import InstitutionJoin from './InstitutionJoin'
import { debounce } from 'debounce'
import { DEPARTMENT_OPTIONS } from '@/utils/const'

const departmentOptionsKeyValue = DEPARTMENT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'InstitutionList',
  components: { InstitutionForm, InstitutionJoin },
  directives: {},
  filters: {
    departmentOptionsFilter(type) {
      return departmentOptionsKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: 'name' },
      showReviewer: false,
      temp: { id: undefined },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Institucion',
        create: 'Creando Institucion',
        join: 'Unir Institucion'
      },
      downloadLoading: false,
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
          query: institutions.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.institutions.results
        this.total = data.institutions.totalCount
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
    handleJoin() {
      this.dialogStatus = 'join'
      this.widthDialog = '85%'
      this.dialogFormVisible = true
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
