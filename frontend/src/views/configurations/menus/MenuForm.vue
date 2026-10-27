<template>
  <div>
    <el-dialog :visible.sync="innerVisible" width="70%" title="Items" append-to-body destroy-on-close>
      <el-table :data="refreshments" style="width: 100%">
        <el-table-column :label="$t('models.refreshment.type')" align="left">
          <template slot-scope="scope">
            <span>{{ scope.row.type | typeFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Item">
          <template slot-scope="scope">
            <span>{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('actions')" fixed="right" align="center" width="150" class-name="small-padding">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleAddRefreshment(scope.$index, scope.row)">Agregar</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-row :gutter="20">
      <el-col :md="24">
        <div class="grid-content">
          <div class="createPost-container">
            <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="200px" style="width: 100%;">
              <el-form-item :label="$t('models.menu.name')" prop="name">
                <el-input v-model="temp.name" @input.native="setUpperCase(temp, 'name', $event)" />
              </el-form-item>
              <el-form-item :label="$t('models.menu.only_volunteer')" prop="only_volunteer">
                <el-switch
                  v-model="temp.only_volunteer"
                  active-text="SI"
                  inactive-text="NO"
                  style="display: block"
                />
              </el-form-item>
              <br>
              <el-form-item>
                <el-button @click="isEdit ? updateData() : createData()">
                  {{ $t('confirm') }}
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import refreshments from '@/query/refreshment'
import menus from '@/query/menu'

const typeOptions = [
  { key: '0', display_name: 'COMESTIBLE' },
  { key: '1', display_name: 'INCENTIVO' }
]

const typeKeyValue = typeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'MenuForm',
  directives: {},
  filters: {
    typeFilter(type) {
      return typeKeyValue[type]
    }
  },
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isEdit: false,
      temp: { id: undefined, name: '', only_volunteer: false},
      rules: {
        quantity: [],
        name: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        only_volunteer: []
      },
      refreshmentLoading: false,
      listRefreshmentQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: 'name' },
      refreshments: [],
      innerVisible: false,
      typeOptions
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  watch: {
    row: function() {
      this.determineAction()
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row != null) {
        this.handleUpdate(this.row)
        this.isEdit = true
      } else {
        this.handleCreate()
        this.isEdit = false
      }
    },
    resetTemp() {
      this.temp = { id: undefined, name: '', only_volunteer: false }
    },
    handleCreate() {
      this.resetTemp()
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
              service: 'createMenu',
              query: menus.createMenu(),
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
              this.$emit('dialogStatus', false)
              this.resetTemp()
              this.$notify({
                title: 'Estado',
                message: 'Registro creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        } else {
          this.$message({
            showClose: true,
            message: 'Hay errores, por favor verifica e intenta nuevamente',
            type: 'error'
          })
        }
      })
    },
    handleUpdate(row) {
      this.resetTemp()
      this.temp = Object.assign({}, row)
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
              service: 'updateMenu',
              query: menus.updateMenu(),
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
              this.$emit('dialogStatus', false)
              this.$notify({
                title: 'Estado',
                message: 'Registro actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        } else {
          this.$message({
            showClose: true,
            message: 'Hay errores, por favor verifica e intenta nuevamente',
            type: 'error'
          })
        }
      })
    }
  }
}
</script>

