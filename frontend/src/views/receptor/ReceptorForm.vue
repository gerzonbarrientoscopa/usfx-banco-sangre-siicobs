<template>
  <div class="createPost-container">
    <el-dialog :visible.sync="innerVisible" append-to-body destroy-on-close title="Agregando Institución" width="70%">
      <institution-form
        v-if="dialogStatus === 'create-institution'"
        :is-secondary-form="institutionFormSecondary"
        @createInstitutionId="handleCreatedInstitution"
        @dialogStatus="handleCloseForm"
      />
    </el-dialog>
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="right"
      label-width="160px"
      style="width: 100%;"
    >
      <el-form-item :label="$t('models.medical.institution')" prop="institution_id">
        <el-row class="el-row--flex">
          <el-select
            v-model="temp.institution_id"
            :loading="listInstitutionLoading"
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
            />
          </el-select>
          <el-tooltip class="item" content="Agregar nueva Institución" effect="dark" placement="top-end">
            <el-button
              v-if="checkPermission(['add_institution'])"
              size="small"
              type="primary"
              @click="handleCreateInstitution"
            >
              <font-awesome-icon icon="plus-circle" style="font-size: 14px" />
            </el-button>
          </el-tooltip>
        </el-row>
      </el-form-item>
      <el-form-item :label="$t('models.patient.first_name')" prop="first_name">
        <el-input v-model="temp.first_name" @input.native="setUpperCase(temp, 'first_name', $event)" />
      </el-form-item>

      <el-form-item :label="$t('models.patient.middle_name')" prop="middle_name">
        <el-input v-model="temp.middle_name" @input.native="setUpperCase(temp, 'middle_name', $event)" />
      </el-form-item>

      <el-form-item :label="$t('models.patient.last_name')" prop="last_name">
        <el-input v-model="temp.last_name" @input.native="setUpperCase(temp, 'last_name', $event)" />
      </el-form-item>

      <el-form-item :label="$t('models.patient.ci')" prop="ci">
        <el-input v-model="temp.ci" />
      </el-form-item>

      <el-form-item :label="$t('models.patient.gender')" prop="gender">
        <el-select v-model="temp.gender" :placeholder="$t('please_select')" class="filter-item" automatic-dropdown>
          <el-option
            v-for="item in genderOptions"
            :key="item.key"
            :label="item.display_name"
            :value="item.key"
          />
        </el-select>
      </el-form-item>

      <el-form-item :label="$t('models.patient.birth_date')" prop="birth_date">
        <el-row class="el-row--flex">
          <el-date-picker
            v-model="temp.birth_date"
            :placeholder="$t('models.patient.birth_date')"
            type="date"
            format="dd-MM-yyyy"
            value-format="yyyy-MM-dd"
          />
          <div style="width: 250px; margin: 0 50px" class="el-row--flex">
            <label style="width: 50px;">Edad</label>
            <el-input v-model="temp.age_receptor" :disabled="temp.is_real_birthdate" class="input-with-select">
              <el-select slot="append" v-model="temp.type_age_receptor" class="el-select-age">
                <el-option label="Años" value="1" />
                <el-option label="Meses" value="2" />
                <el-option label="Días" value="3" />
              </el-select>
            </el-input>
          </div>

          <el-switch
            v-model="temp.is_real_birthdate"
            active-color="#13ce66"
            inactive-color="#ff4949"
            active-text="F. Nac. real"
            inactive-text="F. Nac. no es real"
            style="display: block"
          />
        </el-row>
      </el-form-item>

      <el-form-item :label="$t('models.patient.address')" prop="address">
        <el-input v-model="temp.address" @input.native="setUpperCase(temp, 'address', $event)" />
      </el-form-item>

      <el-form-item :label="$t('models.patient.phone')" prop="phone">
        <el-input v-model.number="temp.phone" type="number" />
      </el-form-item>

      <el-form-item>
        <el-button @click="isEdit ? updateData() : createData()"> {{ $t('confirm') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import institutions from '@/query/institution'
import patients from '@/query/patient'
import InstitutionForm from '@/views/institutions/InstitutionForm'
import moment from 'moment'

const genderOptions = [
  { key: 'F', display_name: 'Femenino' },
  { key: 'M', display_name: 'Masculino' }
]

export default {
  name: 'ReceptorForm',
  components: { InstitutionForm },
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      genderOptions,
      isEdit: false,
      listInstitutionQuery: {
        page: 1,
        limit: 20,
        offset: 0,
        search: '',
        ordering: 'name',
        id: undefined
      },
      temp: {
        id: undefined,
        first_name: '',
        middle_name: '',
        last_name: '',
        ci: undefined,
        birth_date: null,
        gender: '',
        phone: undefined,
        address: '',
        institution_id: undefined,
        is_real_birthdate: true,
        age_receptor: undefined,
        type_age_receptor: '1'
      },
      rules: {
        first_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        middle_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        last_name: [{ trigger: 'blur' }],
        ci: [],
        birth_date: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        gender: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        address: [],
        phone: [{ required: false, type: 'number', message: 'Debe ser número', trigger: 'blur' }]
      },
      listInstitutionLoading: false,
      institutions: null,
      dialogStatus: '',
      innerVisible: false,
      institutionFormSecondary: true
    }
  },
  watch: {
    row: function() {
      this.determineAction()
    },
    'temp.age_receptor': function(value) {
      if (value != null && !this.temp.is_real_birthdate) {
        const date = moment()
        const tempData = Object.assign({}, this.temp)

        if (this.temp.type_age_receptor === '1') {
          date.subtract(value, 'Y')
        } else if (this.temp.type_age_receptor === '2') {
          date.subtract(value, 'M')
        } else {
          date.subtract(value, 'd')
        }
        tempData.birth_date = date.format('YYYY-MM-DD')
        this.temp = tempData
      }
    },
    'temp.type_age_receptor': function(value) {
      if (value != null && !this.temp.is_real_birthdate) {
        const age = this.temp.age_receptor
        const date = moment()

        const tempData = Object.assign({}, this.temp)

        if (value === '1') {
          date.subtract(age, 'Y')
        } else if (value === '2') {
          date.subtract(age, 'M')
        } else {
          date.subtract(age, 'd')
        }

        tempData.birth_date = date.format('YYYY-MM-DD')
        this.temp = tempData
      }
    },
    'temp.birth_date': function(value) {
      if (this.temp.is_real_birthdate) {
        const tempData = Object.assign({}, this.temp)
        const totalMonths = moment().diff(value, 'months')
        const totalDays = moment().diff(value, 'days')
        const years = parseInt(totalMonths / 12)
        const months = totalMonths % 12

        if (years === 0) {
          if (months === 0) {
            tempData.age_receptor = totalDays
            tempData.type_age_receptor = '3'
          } else {
            tempData.age_receptor = months
            tempData.type_age_receptor = '2'
          }
        } else {
          tempData.age_receptor = years
          tempData.type_age_receptor = '1'
        }
        this.temp = tempData
      }
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
    getListInstitution() {
      this.listInstitutionLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'institutions',
          query: institutions.donor_select(this.listInstitutionQuery)
        }
      ).then(response => {
        const data = response.data
        this.institutions = data.institutions.results
        this.listInstitutionLoading = false
      })
    },
    remoteMethodInstitution(query) {
      if (query !== '') {
        this.listInstitutionQuery.search = query
      } else {
        this.listInstitutionQuery.search = ''
      }
      this.getListInstitution()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        first_name: '',
        middle_name: '',
        last_name: '',
        ci: undefined,
        birth_date: null,
        gender: '',
        phone: undefined,
        address: '',
        institution_id: undefined,
        is_real_birthdate: false,
        age_receptor: undefined,
        type_age_receptor: '1'
      }
    },
    handleCreate() {
      this.resetTemp()
      this.getListInstitution()
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.institution = tempData.institution_id
          if (tempData.birth_date) {
            tempData.birth_date = moment(tempData.birth_date).format('YYYY-MM-DD')
          }
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createPatient',
              query: patients.createPatient(),
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
      tempData.type_age_receptor = '1'
      if (tempData.institution) {
        tempData.institution_id = tempData.institution.id
        this.listInstitutionQuery['id'] = tempData.institution.id
      }
      this.getListInstitution()
      this.temp = tempData
      this.listInstitutionQuery['id'] = undefined
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.institution = tempData.institution_id
          tempData.birth_date = moment(tempData.birth_date).format('YYYY-MM-DD')

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updatePatient',
              query: patients.updatePatient(),
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
    handleCreateInstitution() {
      this.innerVisible = true
      this.dialogStatus = 'create-institution'
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.innerVisible = false
    },
    handleCreatedInstitution(id) {
      this.temp.institution_id = id
      this.listInstitutionQuery['id'] = id
      this.getListInstitution()
    }
  }
}
</script>
<style>
  .item {
    margin-bottom: 0;
  }
  .el-select-age {
    width: 110px;
  }
  .input-with-select {
    background-color: #fff;
  }
</style>
