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
        v-if="checkPermission(['add_reason'])"
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
      <el-table-column
        type="index"
        width="50"
      />

      <el-table-column :label="$t('models.reason.name')">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.reason.type')" width="155px" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.type=== 'TE'">{{ scope.row.type | typeFilter }}</el-tag>
          <el-tag v-if="scope.row.type=== 'PE'">{{ scope.row.type | typeFilter }}</el-tag>
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
          <el-button v-if="checkPermission(['change_reason'])" size="mini" @click="handleUpdate(scope.row)">{{ $t('edit') }}</el-button>
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
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="right"
        label-width="120px"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <div class="grid-content">

              <el-form-item :label="$t('models.reason.name')" prop="name">
                <el-input v-model="temp.name" @input.native="setUpperCase(temp, 'name', $event)" />
              </el-form-item>

              <el-form-item :label="$t('models.reason.type')" prop="type">
                <el-select v-model="temp.type" :placeholder="$t('please_select')" class="filter-item">
                  <el-option
                    v-for="item in typeOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

            </div>
          </el-col>
        </el-row>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancelButtonText') }}</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import reasons from '@/query/reason'
import { debounce } from 'debounce'

const typeOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]

const typeKeyValue = typeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'Reason',
  directives: {},
  filters: {
    typeFilter(type) {
      return typeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: 'type,name' },
      showReviewer: false,
      for_loop: 0,
      typeOptions,
      temp: {
        id: undefined,
        name: '',
        type: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Razones de Rechazo',
        create: 'Creando Razones de Rechazo'
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
    getList() {
      this.listLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: reasons.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.reasons.results
        this.total = data.reasons.totalCount
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
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createReason',
              query: reasons.createReason(),
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
                message: 'Registro creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateReason',
              query: reasons.updateReason(),
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
                message: 'Registro actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    }
  }
}
</script>
