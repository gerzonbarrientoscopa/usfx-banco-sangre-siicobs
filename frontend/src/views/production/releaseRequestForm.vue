<template>
  <div class="createPost-container">
    <el-dialog :visible.sync="innerVisible" append-to-body destroy-on-close title="Paquetes o Servicios" width="90%">
      <el-table :data="typeHemocomponents" style="width: 100%">
        <el-table-column label="Sigla" width="150px">
          <template slot-scope="scope">
            <span>{{ scope.row.acronym }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Paquete">
          <template slot-scope="scope">
            <span>{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="150">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleAddTH(scope.$index, scope.row)">Agregar</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-form ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="250px" style="width: 100%;">
      <el-form-item :label="$t('models.releaseRequest.attendant')" prop="attendant_id">
        <el-select v-model="temp.attendant_id" :placeholder="$t('please_select')" automatic-dropdown class="filter-item" filterable>
          <el-option
            v-for="item in employees"
            :key="item.id"
            :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('models.releaseRequest.medical')" prop="medical_id">
        <el-select
          v-model="temp.medical_id"
          :loading="medicalLoading"
          :placeholder="$t('please_select')"
          :remote-method="remoteMethodMedical"
          automatic-dropdown
          class="filter-item"
          filterable
          remote
        >
          <el-option
            v-for="item in medicals"
            :key="item.id"
            :label="item | fullNameWithInstitution"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('models.releaseRequest.description')" prop="description">
        <el-input v-model="temp.description" :rows="4" type="textarea" @input.native="setUpperCase(temp, 'description', $event)" />
      </el-form-item>
      <el-table :data="temp.typeHemocomponents" style="width: 100%">
        <el-table-column label="Sigla" width="100px">
          <template slot-scope="scope">
            <span>{{ scope.row.typehemocomponent.acronym }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Paquete">
          <template slot-scope="scope">
            <span>{{ scope.row.typehemocomponent.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Cantidad Solicitada">
          <template slot-scope="scope">
            <el-form-item label-width="0px" prop="quantity_request" style="margin-bottom: 0">
              <el-input-number v-model.number="scope.row.quantity_request" :min="1" size="small" />
            </el-form-item>
          </template>
        </el-table-column>
        <el-table-column label="Cantidad Liberada">
          <template slot-scope="scope">
            <el-form-item label-width="0px" prop="quantity_release" style="margin-bottom: 0">
              <el-input-number v-model.number="scope.row.quantity_release" :min="0" size="small" />
            </el-form-item>
          </template>
        </el-table-column>
        <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="250">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleRemoveTH(scope.$index, scope.row)">Quitar {{ scope.rowIndex }}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-form-item>
        <el-button @click="handleShowTypeHemocomponentsDialog()">
          Agregar Paquetes
        </el-button>
        <el-button @click="isEdit ? updateData() : createData()"> {{ $t('confirm') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import checkPermission from '@/utils/permission'
import releaseRequests from '@/query/releaseRequest'
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import medicals from '@/query/medical'
import typehemocomponents from '@/query/type-hemocomponent'

const statusOptions = [
  { key: 1, display_name: 'NUEVO' },
  { key: 2, display_name: 'EN PROCESO' },
  { key: 3, display_name: 'LIBERADO' }
]

export default {
  name: 'ReleaseRequestForm',
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      statusOptions,
      listMedicalQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      listTypeHemocomponentQuery: { page: 1, limit: 20, title: undefined, offset: 0, search: '', ordering: '-name' },
      temp: {
        id: undefined,
        employee_id: undefined,
        medical_id: undefined,
        attendant_id: undefined,
        description: '',
        status: 1,
        register_at: moment(),
        typeHemocomponents: []
      },
      rules: {
        medical_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        attendant_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        status: [],
        description: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        quantity_request: [],
        quantity_release: []
      },
      medicals: null,
      medicalLoading: false,
      innerVisible: false,
      typeHemocomponents: [],
      typeHemocomponentLoading: false
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
    checkPermission,
    determineAction() {
      if (this.row != null) {
        this.handleUpdate(this.row)
        this.isEdit = true
      } else {
        this.handleCreate()
        this.isEdit = false
      }
    },
    getListMedicals() {
      this.medicalLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'medicals',
          query: medicals.list(this.listMedicalQuery)
        }
      ).then(response => {
        const data = response.data
        this.medicals = data.medicals.results
        this.medicalLoading = false
      })
    },
    remoteMethodMedical(query) {
      if (query !== '') {
        this.listMedicalQuery.search = query
      } else {
        this.listMedicalQuery.search = ''
      }
      this.getListMedicals()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        employee_id: undefined,
        medical_id: undefined,
        attendant_id: undefined,
        description: '',
        status: 1,
        register_at: moment(),
        typeHemocomponents: []
      }
    },
    handleCreate() {
      this.resetTemp()
      this.getListMedicals()
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.employee_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createReleaseRequest',
              query: releaseRequests.createReleaseRequest(),
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
        }
      })
    },
    handleUpdate(row) {
      const tempData = Object.assign({}, row)
      tempData.attendant_id = tempData.attendant.id
      tempData.medical_id = tempData.medical.id
      this.listMedicalQuery['id'] = tempData.medical.id
      this.getListMedicals()
      this.temp = tempData
      this.listMedicalQuery['id'] = undefined
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.employee_id = this.employee_id
          tempData.register_at = moment(tempData.register_at)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateReleaseRequest',
              query: releaseRequests.updateReleaseRequest(),
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
        }
      })
    },
    handleAddTH(index, row) {
      const tempData = Object.assign({}, this.temp)
      tempData.typeHemocomponents.push({ typehemocomponent: row, quantity_request: 1, quantity_release: 0 })
      this.temp = tempData
      delete this.typeHemocomponents.splice(index, 1)
    },
    handleRemoveTH(index, row) {
      var tempData = Object.assign({}, this.temp)
      var newItems = []
      var oldItems = tempData.typeHemocomponents
      oldItems.forEach(function(obj, idx) {
        if (index !== idx) {
          newItems.push(obj)
        }
      })
      tempData.typeHemocomponents = newItems
      this.temp = tempData
    },
    getListTypeHemocomponents() {
      this.typeHemocomponentLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.requestRelease(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.typeHemocomponents = data.typehemocomponents.results
        this.typeHemocomponentLoading = false
      })
    },
    handleShowTypeHemocomponentsDialog() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.requestRelease(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.typeHemocomponents = data.typehemocomponents.results
        this.total = data.typehemocomponents.count
        this.innerVisible = true
        const tempData = Object.assign({}, this.temp)
        const newListItems = []
        if (tempData.typeHemocomponents) {
          this.typeHemocomponents.forEach(function(obj, idx) {
            const findItemAdded = tempData.typeHemocomponents.filter(element => element.typehemocomponent.id === obj.id)
            if (findItemAdded.length === 0) {
              newListItems.push(obj)
            }
          })
          this.typeHemocomponents = newListItems
        }
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.handleShowItemDialog()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.handleShowItemDialog()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.handleShowItemDialog()
    }
  }
}
</script>
<style>
  .item {
    margin-bottom: 0;
  }
</style>
