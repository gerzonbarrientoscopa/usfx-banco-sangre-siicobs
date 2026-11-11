<template>
  <div class="app-container">
    <el-dialog
      :visible.sync="innerVisible"
      append-to-body
      destroy-on-close
      title="Hemocomponentes"
      width="90%"
      @closed="notifyAddedItem"
    >
      <div class="filter-container">
        <el-row :gutter="10" style="width: 100%">
          <el-col :md="8">
            <el-select
              v-model="listQuery.typehemocomponent_id"
              :loading="typeHemocomponentLoading"
              :remote-method="remoteMethod"
              automatic-dropdown
              class="filter-item"
              clearable
              filterable
              placeholder="Tipo de Hemocomponente"
              remote
              @change="getListItems()"
            >
              <el-option
                v-for="item in listTypeHemocomponents"
                :key="item.id"
                :label="item.name "
                :value="item.id"
              />
            </el-select>
          </el-col>
          <el-col :md="16">
            <el-input
              v-model.lazy="listQuery.search"
              :autofocus="'autofocus'"
              :placeholder="'Buscar'"
              class="filter-item"
              clearable
              prefix-icon="el-icon-search"
              style="width: 100%;"
              @input="handleFilter"
            />
          </el-col>
        </el-row>
      </div>
      <el-table
        :data="itemFragmentations"
        style="width: 100%"
      >
        <el-table-column
          label="Codigo"
          width="80"
        >
          <template slot-scope="scope">
            <span><strong>{{ scope.row.donor_code }}</strong></span>
          </template>
        </el-table-column>
        <el-table-column
          label="Tipo de Hemocomponente"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.typehemocomponent.name }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Fecha de Expiración"
          width="170"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.expiration_date | toHumanDatetime }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Tubuladura"
          width="150"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.fragmentation.extraction.tubing }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="Volumen"
          width="150"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.weight }} ml.</span>
          </template>
        </el-table-column>
        <el-table-column
          :label="$t('actions')"
          align="center"
          class-name="small-padding"
          fixed="right"
          width="150"
        >
          <template slot-scope="scope">
            <el-button size="mini" @click="handleAddItem(scope.row)">Agregar</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-show="total>0"
          :current-page="listQuery.page"
          :page-size="listQuery.limit"
          :page-sizes="[10, 20, 30, 50]"
          :total="total"
          background
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-dialog>
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="left"
      label-width="160px"
      style="width: 100%;"
    >
      <el-row :gutter="20">
        <el-col :md="24" :sm="24">
          <div class="grid-content">
            <el-form-item :label="$t('models.distribution.register_at')" prop="register_at">
              <el-date-picker
                v-model="temp.register_at"
                :picker-options="dateTimePickerOptions"
                format="dd-MM-yyyy HH:mm"
                placeholder="Seleccione fecha y hora"
                type="datetime"
                value-format="yyyy-MM-dd HH:mm:ss"
              />
            </el-form-item>
            <el-form-item :label="$t('models.distribution.medical')" prop="medical_id">
              <el-select
                v-model="temp.medical_id"
                :loading="medicalLoading"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodMedical"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
                @change="setInstitution(temp.medical_id)"
              >
                <el-option
                  v-for="item in medicals"
                  :key="item.id"
                  :label="item | fullName "
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.medical.institution')" prop="institution_id">
              <el-select
                v-model="temp.institution_id"
                :loading="institutionLoading"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodInstitution"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
              >
                <el-option
                  v-for="item in institutions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                <span style="float: left">{{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.type | institutionTypeValue }}</span>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.distribution.patient')" prop="patient_id">
              <el-select
                v-model="temp.patient_id"
                :loading="patientLoading"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodPatient"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
              >
                <el-option
                  v-for="item in patients"
                  :key="item.id"
                  :label="item | fullName "
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.distribution.service_transfunctional')" prop="service_transfunctional">
              <el-input
                v-model="temp.service_transfunctional"
                style="display: block"
                @input.native="setUpperCase(temp, 'service_transfunctional', $event)"
              />
            </el-form-item>
            <el-form-item :label="$t('models.distribution.type_payment')" prop="type_payment">
              <el-select v-model="temp.type_payment" :placeholder="$t('please_select')" class="filter-item">
                <el-option
                  v-for="item in TYPE_PAYMENT_OPTIONS"
                  :key="item.key"
                  :label="item.display_name"
                  :value="item.key"
                />
              </el-select>
            </el-form-item>

            <el-form-item :label="$t('models.distribution.observations')" prop="observations">
              <el-input v-model="temp.observations" :rows="2" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
            </el-form-item>
            <el-table
              :data="temp.itemfragmentations"
              style="width: 100%"
            >
              <el-table-column label="Código" width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.donor_code }}</span>
                </template>
              </el-table-column>
              <el-table-column
                label="Tipo de Hemocomponente"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.typehemocomponent.name }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Fecha de Expiración" width="180">
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.expiration_date | toHumanDatetime }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Tubuladura" width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.fragmentation.extraction.tubing }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Volumen" width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.itemfragmentation.weight }} ml.</span>
                </template>
              </el-table-column>
              <el-table-column
                :label="$t('actions')"
                align="center"
                class-name="small-padding"
                fixed="right"
                width="250"
              >
                <template slot-scope="scope">
                  <el-button size="mini" @click="handleRemoveItem(scope.$index)">Quitar</el-button>
                </template>
              </el-table-column>
            </el-table>
            <br>
            <el-form-item>
              <el-button @click="handleShowItemDialog()">
                Agregar Items
              </el-button>
              <el-button @click="isEdit ? updateData() : createData()">
                {{ $t('confirm') }}
              </el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { debounce } from 'debounce'
import Cookies from 'js-cookie'
import { graphqlRequest } from '@/api/graphql'
import medicals from '@/query/medical'
import institutions from '@/query/institution'
import patients from '@/query/patient'
import itemFragmentations from '@/query/itemFragmentation'
import typehemocomponents from '@/query/type-hemocomponent'
import distributions from '@/query/distribution'
import moment from 'moment'
import { TYPE_PAYMENT_OPTIONS } from '@/utils/const'
import {institutionTypeValue} from "../../filters";

export default {
  name: 'DistributionForm',
  data() {
    return {
      dateTimePickerOptions: {
        shortcuts: [{
          text: 'Hoy',
          onClick(picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: 'Ayer',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: 'Hace una semana',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      },
      isEdit: false,
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      tableKey: 0,
      patients: null,
      medicals: null,
      institutions: null,
      list: null,
      total: null,
      loading: false,
      listLoading: true,
      institutionLoading: false,
      patientLoading: false,
      medicalLoading: false,
      TYPE_PAYMENT_OPTIONS,
      listPatientQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      listMedicalQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      listInstitutionQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-id', id: undefined },
      listQuery: { page: 1, limit: 10, offset: 0, search: '', ordering: '-id', typediscard: true, typehemocomponent_id: '' },
      temp: {
        id: undefined,
        employee_id: undefined,
        extraction_id: undefined,
        patient_id: undefined,
        medical_id: undefined,
        institution_id: undefined,
        itemfragmentations: [],
        service_transfunctional: '',
        observations: '',
        type_payment: '',
        register_at: new Date()
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Editando Distribucion',
        create: 'Creando Distribucion'
      },
      rules: {
        patient_id: [],
        medical_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        institution_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type_payment: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        service_transfunctional: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        medical: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        observations: [{ trigger: 'blur' }],
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
      },
      downloadLoading: false,
      totalHC: 0,
      innerVisible: false,
      pendingItemNotification: null,
      itemFragmentations: [],
      listTypeHemocomponents: [],
      typeHemocomponentLoading: false,
      listTypeHemocomponentQuery: { page: 1, limit: 20, title: undefined, offset: 0, search: '', ordering: '-name' }
    }
  },
  computed: {
    ...mapGetters([
      'employees',
      'employee_id'
    ])
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    institutionTypeValue,
    determineAction() {
      if (this.$route.params && this.$route.params.id) {
        this.getDistribution(this.$route.params.id)
        this.isEdit = true
      } else {
        this.handleCreate()
        this.isEdit = false
      }
      this.getListTypeHemocomponents()
    },
    getDistribution(id) {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'distributions',
          query: distributions.getDistribution(id)
        }
      ).then(response => {
        const data = response.data
        this.setTagsViewTitle(data.distribution)
        this.handleUpdate(data.distribution)
      })
    },
    setTagsViewTitle(distribution) {
      const title = 'Distribución'
      const route = Object.assign({}, this.$route, { title: `${title}-${distribution.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    getListTypeHemocomponents() {
      this.typeHemocomponentLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'typehemocomponents',
          query: typehemocomponents.package_select(this.listTypeHemocomponentQuery)
        }
      ).then(response => {
        const data = response.data
        this.listTypeHemocomponents = data.typehemocomponents.results
        this.typeHemocomponentLoading = false
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        this.listTypeHemocomponentQuery.search = query
      } else {
        this.listTypeHemocomponentQuery.search = ''
      }
      this.getListTypeHemocomponents()
    },
    setInstitution(id) {
      graphqlRequest(
        {
          from: this.$route.name,
          query: medicals.get(id)
        }
      ).then(response => {
        const medical = response.data.medical

        if (medical.institution) {
          this.temp.institution_id = medical.institution.id
          this.listInstitutionQuery['id'] = medical.institution.id
          this.getListInstitutions()
          this.listInstitutionQuery['id'] = undefined
        }
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        employee_id: undefined,
        extraction_id: undefined,
        patient_id: undefined,
        medical_id: undefined,
        institution_id: undefined,
        itemfragmentations: [],
        register_at: new Date()
      }
    },
    handleCreate() {
      this.resetTemp()
      if (Cookies.get('distributionMedical') !== 'undefined' && Cookies.get('distributionMedical') !== undefined) {
        const medical = JSON.parse(Cookies.get('distributionMedical'))
        this.listMedicalQuery['id'] = medical.id
        if (medical.institution) {
          this.listInstitutionQuery['id'] = medical.institution.id
        }
      }
      if (Cookies.get('distributionReceptor') !== 'undefined' && Cookies.get('distributionReceptor') !== undefined) {
        const patient = JSON.parse(Cookies.get('distributionReceptor'))
        this.listPatientQuery['id'] = patient.id
      }
      this.dialogStatus = 'create'
      this.getListPatients()
      this.getListMedicals()
      this.getListInstitutions()

      this.listPatientQuery['id'] = undefined
      this.listMedicalQuery['id'] = undefined
      this.listInstitutionQuery['id'] = undefined
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          if (this.temp.itemfragmentations.length === 0) {
            this.$notify({
              title: 'Estado',
              message: 'Necesitas agregar al menos un Item de Fragmentacion',
              type: 'warning',
              duration: 2000
            })
            return
          }
          const tempData = Object.assign({}, this.temp)
          tempData.employee_id = this.employee_id
          tempData.is_donation = false
          tempData.register_at = new Date(tempData.register_at).toISOString()
          tempData.register_at = moment(tempData.register_at)
          tempData.itemfragmentations = this.formattedItemDistribution(tempData)

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createDistribution',
              query: distributions.createDistribution(),
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
              this.$router.push({ name: 'distributions', params: {}})

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
      const tempData = Object.assign({}, row)
      if (tempData.patient) {
        this.listPatientQuery['id'] = row.patient.id
      }
      this.listMedicalQuery['id'] = row.medical.id
      this.listInstitutionQuery['id'] = row.institution.id
      tempData.register_at = new Date(tempData.register_at)
      tempData.medical_id = tempData.medical.id
      tempData.institution_id = tempData.institution.id
      tempData.patient ? tempData.patient_id = tempData.patient.id : tempData.patient_id = undefined
      this.temp = tempData
      this.dialogStatus = 'update'
      this.getListPatients()
      this.getListMedicals()
      this.getListInstitutions()

      this.listPatientQuery['id'] = undefined
      this.listMedicalQuery['id'] = undefined
      this.listInstitutionQuery['id'] = undefined
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    formattedItemDistribution(tempData) {
      const newListMenus = []
      tempData.itemfragmentations.forEach(function(obj, idx) {
        newListMenus.push({ id: obj.itemfragmentation.id })
      })
      return newListMenus
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.itemfragmentations = this.formattedItemDistribution(tempData)
          tempData.employee_id = this.employee_id
          tempData.status = 'IN_PROGRESS'
          tempData.register_at = moment(tempData.register_at)
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateDistribution',
              query: distributions.updateDistribution(),
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
              this.$notify({
                title: 'Estado',
                message: 'Se ha actualizado distribución',
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
    getListMedicals() {
      this.medicalLoading = true
      if (Cookies.get('distributionMedical') !== 'undefined' && Cookies.get('distributionMedical') !== undefined) {
        const medical = JSON.parse(Cookies.get('distributionMedical'))
        const tempData = Object.assign({}, this.temp)
        tempData.medical_id = medical.id

        if (medical.institution) {
          tempData.institution_id = medical.institution.id
        }

        this.temp = tempData
      }
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'medicals',
          query: medicals.distribution_select(this.listMedicalQuery)
        }
      ).then(response => {
        const data = response.data
        this.medicals = data.medicals.results
        this.medicalLoading = false
      })
    },
    getListPatients() {
      this.patientLoading = true
      if (Cookies.get('distributionReceptor') !== 'undefined' && Cookies.get('distributionReceptor') !== undefined) {
        const patient = JSON.parse(Cookies.get('distributionReceptor'))
        const tempData = Object.assign({}, this.temp)
        tempData.patient_id = patient.id

        this.temp = tempData
      }
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'patients',
          query: patients.distribution_select(this.listPatientQuery)
        }
      ).then(response => {
        const data = response.data
        this.patients = data.patients.results
        this.patientLoading = false
      })
    },
    getListInstitutions() {
      this.institutionLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'institutions',
          query: institutions.distribution_select(this.listInstitutionQuery)
        }
      ).then(response => {
        const data = response.data
        this.institutions = data.institutions.results
        this.institutionLoading = false
      })
    },
    remoteMethodInstitution(query) {
      if (query !== '') {
        this.listInstitutionQuery.search = query
      } else {
        this.listInstitutionQuery.search = ''
      }
      this.getListInstitutions()
    },
    remoteMethodMedical(query) {
      if (query !== '') {
        this.listMedicalQuery.search = query
      } else {
        this.listMedicalQuery.search = ''
      }
      this.getListMedicals()
    },
    remoteMethodPatient(query) {
      if (query !== '') {
        this.listPatientQuery.search = query
      } else {
        this.listPatientQuery.search = ''
      }
      this.getListPatients()
    },
    handleAddItem2(index, row) {
      const tempData = Object.assign({}, this.temp)
      tempData.itemfragmentations.push({ itemfragmentation: row })
      this.temp = tempData
      delete this.itemfragmentations.splice(index, 1)
    },
    handleAddItem(hemocomponent) {
      const tempData = Object.assign({}, this.temp)
      let is_expired = true
      const distributionDateMidnight = moment(new Date(this.temp.register_at).toISOString())
      const hemocomponentExpiration = moment(hemocomponent.expiration_date).endOf('day')
      if (hemocomponentExpiration >= distributionDateMidnight) {
        tempData.itemfragmentations.push({ itemfragmentation: hemocomponent })
        this.temp = tempData
        is_expired = false
      }

      const notification = {
        title: 'Estado',
        message: is_expired ? 'Hemocomponente vencido, no se puede agregar' : 'Hemocomponente Agregado',
        type: is_expired ? 'error' : 'success',
        duration: 2000
      }

      if (is_expired) {
        this.$notify(notification)
        return
      }

      this.pendingItemNotification = notification
      this.innerVisible = false
    },
    notifyAddedItem() {
      if (!this.pendingItemNotification) return

      const notification = this.pendingItemNotification
      this.pendingItemNotification = null
      this.$notify(notification)
    },
    handleRemoveItem(index) {
      const itemfragmentations = this.temp.itemfragmentations.slice()
      if (index < 0 || index >= itemfragmentations.length) return

      itemfragmentations.splice(index, 1)
      this.temp = Object.assign({}, this.temp, { itemfragmentations })
    },
    isItemAdded(itemId) {
      const arrKeys = this.temp.itemfragmentations.map(el => (el.itemfragmentation.id).toString())
      const findItemAdded = arrKeys.lastIndexOf(itemId.toString())
      return findItemAdded > -1
    },
    handleShowItemDialog() {
      this.getListItems();
    },
    getListItems(){
      const tempListQuery = Object.assign({}, this.listQuery)
      const tempData = this.temp

      if (tempListQuery.typehemocomponent_id === '') {
        tempListQuery.typehemocomponent_id = null
      }

      let isAutomaticallyAdd = false

      if (tempListQuery.search !== '' && tempListQuery.search[0] === '0') {
        const searchElement = tempListQuery.search.substring(1, tempListQuery.search.length)
        tempListQuery.id = parseInt(searchElement, 10)
        tempListQuery.search = ''
        isAutomaticallyAdd = true
      }

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'itemfragmentations',
          query: itemFragmentations.listAddingDistributions(tempListQuery),
          variables: tempListQuery
        }
      ).then(response => {
        const data = response.data
        this.itemFragmentations = data.itemfragmentations.results
        this.total = data.itemfragmentations.totalCount
        this.innerVisible = true

        const newListItems = []

        this.itemFragmentations.forEach(function (obj) {
          const findItemAdded = tempData.itemfragmentations.filter(element => {
            return element.itemfragmentation.id === obj.id
          })

          if (findItemAdded.length === 0) {
            newListItems.push(obj)
          }
        })
        this.itemFragmentations = newListItems

        //verify if we are searching for add
        if (isAutomaticallyAdd) {
          if (this.isItemAdded(tempListQuery.id)) {
            this.$message({
              showClose: true,
              message: 'El Hemocomponente ya esta agregado',
              type: 'error'
            })
            return 0
          }

          if (this.itemFragmentations.length === 1 ) {
            this.handleAddItem(this.itemFragmentations[0])
          } else {
            this.$message({
              showClose: true,
              message: 'El Hemocomponente no existe en liberación',
              type: 'error'
            })
          }
          this.listQuery.search = ''
          this.getListItems();
        }
      })
    },

    handleFilter: debounce(function() {
      this.listQuery.page = 1
      this.listQuery.offset = 0
      this.getListItems()
    }, 500),
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getListItems()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.listQuery.offset = this.listQuery.limit * (val - 1)
      this.getListItems()
    }
  }
}
</script>
