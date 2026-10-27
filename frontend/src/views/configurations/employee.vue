<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" :placeholder="$t('models.employee.full_name')" :autofocus="'autofocus'" prefix-icon="el-icon-search" clearable class="filter-item" @input="handleFilter" />
      <el-button
        v-if="checkPermission(['add_employee'])"
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"

        @click="handleCreate"
      >{{ $t('add') }}
      </el-button>
    </div>

    <el-table :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%;">
      <el-table-column :label="$t('models.employee.full_name')" min-width="250px">
        <template slot-scope="scope">
          <span>{{ scope.row | fullName }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.employee.ci')" align="center" width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.ci }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.employee.role')" align="center" width="180px">
        <template slot-scope="scope">
          <span v-if="scope.row.user">
            <span v-for="(group) in scope.row.user.groups" :key="group.id">
              <el-tag size="mini">{{ group.name }}</el-tag>
            </span>
          </span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.employee.username')" width="150px" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.user">{{ scope.row.user.username }}</span>
        </template>
      </el-table-column>

      <el-table-column :label="$t('models.employee.status')" class-name="status-col" width="150px">
        <template slot-scope="scope">
          <el-tag :type="scope.row | statusFilter">
            {{ scope.row.user && scope.row.user.is_active ? 'ACTIVADO' : 'DESACTIVADO' }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column :label="$t('actions')" align="center" width="250px" fixed="right" class-name="small-padding">
        <template slot-scope="scope">
          <el-button
            v-if="checkPermission(['change_employee'])"
            type="primary"
            size="mini"
            @click="handleUpdate(scope.row)"
          >{{ $t('edit') }}
          </el-button>
          <el-button
            v-if="checkPermission(['change_user']) && scope.row.user"
            :type="scope.row.user && scope.row.user.is_active ? 'danger' : 'success'"
            size="mini"
            @click="handleModifyStatus(scope.row)"
          >
            {{ scope.row.user && scope.row.user.is_active ? 'DESACTIVAR' : 'ACTIVAR' }}
          </el-button>
          <el-button
            v-if="checkPermission(['add_user']) && !scope.row.user"
            size="mini"
            @click="handleAddUser(scope.row)"
          >
            Agregar Usuario
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="80%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="120px" style="width: 100%;">
        <el-row :gutter="20">
          <el-col :sm="24" :md="8">
            <div class="grid-content">
              <el-form-item :label="$t('models.employee.first_name')" prop="first_name">
                <el-input v-model="temp.first_name" @input.native="setUpperCase(temp, 'first_name', $event)" />
              </el-form-item>

              <el-form-item :label="$t('models.employee.middle_name')" prop="middle_name">
                <el-input v-model="temp.middle_name" @input.native="setUpperCase(temp, 'middle_name', $event)" />
              </el-form-item>

              <el-form-item :label="$t('models.employee.last_name')" prop="last_name">
                <el-input v-model="temp.last_name" @input.native="setUpperCase(temp, 'last_name', $event)" />
              </el-form-item>
            </div>
          </el-col>
          <el-col :sm="24" :md="8">
            <div class="grid-content">
              <el-form-item :label="$t('models.employee.ci')" prop="ci">
                <el-input v-model.number="temp.ci" type="number" />
              </el-form-item>

              <el-form-item :label="$t('models.employee.gender')" prop="gender">
                <el-select
                  v-model="temp.gender"
                  :placeholder="$t('please_select')"
                  class="filter-item"
                  automatic-dropdown
                >
                  <el-option
                    v-for="item in genderOptions"
                    :key="item.key"
                    :label="item.display_name"
                    :value="item.key"
                  />
                </el-select>
              </el-form-item>

              <el-form-item :label="$t('models.employee.home_address')" prop="home_address">
                <el-input v-model="temp.home_address" @input.native="setUpperCase(temp, 'home_address', $event)" />
              </el-form-item>
            </div>
          </el-col>
          <el-col :sm="24" :md="8">
            <div class="grid-content">
              <el-form-item :label="$t('models.employee.mobile_phone')" prop="mobile_phone">
                <el-input v-model.number="temp.mobile_phone" type="number" />
              </el-form-item>
              <el-form-item :label="$t('models.employee.code_licence')" prop="code_licence">
                <el-input v-model="temp.code_licence" @input.native="setUpperCase(temp, 'code_licence', $event)" />
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ $t('cancelButtonText') }}</el-button>
        <el-button @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="'Agregando Usuario'" :visible.sync="dialogFormUserVisible" width="50%">
      <el-form
        ref="dataFormUser"
        :rules="rules_user"
        :model="temp_user"
        label-position="right"
        label-width="200px"
        style="width: 100%;"
      >
        <el-row :gutter="20">
          <el-col :sm="24" :md="24">
            <div class="grid-content">
              <el-form-item :label="$t('models.user.username')" prop="username">
                <el-input v-model="temp_user.username" />
              </el-form-item>

              <el-form-item :label="$t('models.user.password')" prop="password">
                <el-input v-model="temp_user.password" type="password" />
              </el-form-item>

              <el-form-item :label="$t('models.user.password_confirmation')" prop="password_confirmation">
                <el-input v-model="temp_user.password_confirmation" type="password" />
              </el-form-item>
              <el-form-item :label="$t('models.user.group_id')" prop="group_ids">
                <el-select
                  v-model="temp_user.group_ids"
                  :placeholder="$t('please_select')"
                  class="filter-item"
                  automatic-dropdown
                  multiple
                >
                  <el-option
                    v-for="item in groups"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id"
                  />
                </el-select>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormUserVisible = false">{{ $t('cancelButtonText') }}</el-button>
        <el-button @click="createUserData()">{{ $t('confirmButtonText') }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import employees from '@/query/employee'
import { debounce } from 'debounce'
import users from '@/query/user'
import groups from '@/query/group'

const genderOptions = [
  { key: 'F', display_name: 'Femenino' },
  { key: 'M', display_name: 'Masculino' }
]

export default {
  name: 'Employee',
  directives: {},
  filters: {
    statusFilter(row) {
      let status = 'danger'

      if (row.user && row.user.is_active) {
        status = 'success'
      }
      return status
    }
  },
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
        ordering: 'first_name,middle_name,last_name'
      },
      listQueryGroups: {
        page: 1,
        limit: 100,
        offset: 0,
        search: '',
        ordering: 'name'
      },
      genderOptions,
      groups: [],
      temp: {
        id: undefined,
        first_name: '',
        middle_name: '',
        last_name: '',
        ci: '',
        gender: '',
        status: '',
        mobile_phone: '',
        rol: '',
        home_address: '',
        code_licence: ''
      },
      temp_user: {
        username: '',
        password: '',
        password_confirmation: '',
        employee_id: undefined,
        groups: undefined
      },
      dialogFormVisible: false,
      dialogFormUserVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Modificando Personal Responsable',
        create: 'Creando Personal Responsable'
      },
      rules: {
        first_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        middle_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        last_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        ci: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }, {
          type: 'number',
          message: 'Debe ser número'
        }],
        gender: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        status: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        rol: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
      },
      rules_user: {
        username: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        password: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        password_confirmation: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        group_ids: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
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
          query: employees.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.list = data.employees.results
        this.total = data.employees.totalCount
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
    handleModifyStatus(row) {
      if (row.user) {
        const message = row.user.is_active ? 'Usuario deactivado' : 'Usuario activado'
        graphqlRequest(
          {
            from: this.$route.name,
            service: 'updateUser',
            query: users.updateUser(),
            variables: { id: row.user.id, is_active: !row.user.is_active }
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
            this.$message({
              message: message,
              type: 'success'
            })
          }
        })
      }
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        code_licence: '',
        institution_id: 1 // Generic institution
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
              service: 'createEmployee',
              query: employees.createEmployee(),
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
              service: 'updateEmployee',
              query: employees.updateEmployee(),
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
    },
    getListGroup() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'grups',
          query: groups.userSelect(this.listQueryGroups)
        }
      ).then(response => {
        const data = response.data
        this.groups = data.groups.results
        this.total = data.groups.totalCount
      })
    },
    resetTempUser() {
      this.temp_user = {
        username: '',
        password: '',
        password_confirmation: '',
        employee_id: undefined,
        group_ids: []
      }
    },
    handleAddUser(row) {
      this.resetTempUser()
      this.getListGroup()
      this.temp_user.profile_id = row.id
      this.dialogFormUserVisible = true
      this.$nextTick(() => {
        this.$refs['dataFormUser'].clearValidate()
      })
    },
    createUserData() {
      this.$refs['dataFormUser'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp_user)

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createUser',
              query: users.createUser(),
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
              this.dialogFormUserVisible = false
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
    }
  }
}
</script>
