<template>
  <div class="app-container">
    <el-dialog :visible.sync="innerVisible" append-to-body destroy-on-close title="Agregando Institución" width="70%">
      <institution-form v-if="dialogStatus === 'create-institution'" :is-secondary-form="institutionFormSecondary" @createInstitutionId="handleCreatedInstitution" @dialogStatus="handleCloseForm" />
    </el-dialog>
    <el-form ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="120px" style="width: 100%;">
      <el-row :gutter="20">
        <el-col :md="24" :sm="24">
          <div class="grid-content">
            <el-form-item :label="$t('models.medical.first_name')" prop="first_name">
              <el-input v-model="temp.first_name" @input.native="setUpperCase(temp, 'first_name', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.medical.middle_name')" prop="middle_name">
              <el-input v-model="temp.middle_name" @input.native="setUpperCase(temp, 'middle_name', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.medical.last_name')" prop="last_name">
              <el-input v-model="temp.last_name" @input.native="setUpperCase(temp, 'last_name', $event)" />
            </el-form-item>
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
                <el-tooltip class="item" content="Agregar nueva Institucion" effect="dark" placement="top-end">
                  <el-button size="small" @click="handleCreateInstitution">
                    <font-awesome-icon icon="plus-circle" style="font-size: 14px" />
                  </el-button>
                </el-tooltip>
              </el-row>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogFormVisible = false">{{ $t('cancelButtonText') }}</el-button>
      <el-button @click="isEdit?updateData():createData()">{{ $t('confirmButtonText') }}
      </el-button>
    </div>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import institutions from '@/query/institution'
import medicals from '@/query/medical'
import InstitutionForm from '@/views/institutions/InstitutionForm'

export default {
  name: 'MedicalForm',
  components: { InstitutionForm },
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
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
        institution_id: undefined
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: { update: 'Modificando Médico', create: 'Creando Médico' },
      rules: {
        first_name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        middle_name: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        last_name: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }],
        institution_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      listInstitutionLoading: false,
      institutions: null,
      innerVisible: false,
      institutionFormSecondary: true
    }
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
    checkPermission,
    getListInstitution() {
      this.listInstitutionLoading = true
      graphqlRequest(
        {
          from: this.$route.name,
          query: institutions.medical_select(this.listInstitutionQuery)
        }
      ).then(response => {
        const data = response.data
        this.institutions = data.institutions.results
        this.listInstitutionLoading = false
      })
    },
    remoteMethodInstitution(query) {
      this.listInstitutionQuery.search = query !== '' ? query : ''
      this.getListInstitution()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        first_name: '',
        middle_name: '',
        last_name: '',
        institution_id: undefined
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

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createMedical',
              query: medicals.createMedical(),
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
      this.listInstitutionQuery['id'] = row.institution.id
      this.getListInstitution()
      const tempData = Object.assign({}, row) // copy obj
      tempData.institution_id = tempData.institution.id
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

          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateMedical',
              query: medicals.updateMedical(),
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
