<template>
  <div class="app-container">
    <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="200px" style="width: 100%;">
      <el-row :gutter="20">
        <el-col :sm="24" :md="24">
          <div class="grid-content">
            <el-form-item :label="$t('models.institution.type')" prop="type">
              <el-radio-group v-model="temp.type">
                <el-radio-button v-for="type in INSTITUTION_TYPE_OPTIONS" :key="type.key" :label="type.key">
                  {{ type.display_name }}
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item :label="$t('models.institution.name')" prop="name">
              <el-input v-model="temp.name" @input.native="setUpperCase(temp, 'name', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.institution.department')" prop="department">
              <el-select v-model="temp.department" :placeholder="$t('please_select')" class="filter-item" filterable automatic-dropdown>
                <el-option v-for="item in departmentOptions" :key="item.key" :label="item.display_name" :value="item.key" />
              </el-select>
            </el-form-item>
            <el-form-item :label="$t('models.institution.address')" prop="address">
              <el-input v-model="temp.address" @input.native="setUpperCase(temp, 'address', $event)" />
            </el-form-item>
            <el-form-item :label="$t('models.institution.phone')" prop="phone">
              <el-input v-model.number="temp.phone" type="number" maxlength="9" />
            </el-form-item>
            <el-form-item>
              <el-button @click="isEdit ? updateData() : createData()"> {{ $t('confirm') }}</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { graphqlRequest } from '@/api/graphql'
import institutions from '@/query/institution'
import { DEPARTMENT_OPTIONS, INSTITUTION_TYPE_OPTIONS } from '@/utils/const'

export default {
  name: 'InstitutionForm',
  props: {
    row: {
      type: Object,
      default: null
    },
    isSecondaryForm: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isEdit: false,
      departmentOptions: DEPARTMENT_OPTIONS,
      temp: {
        id: undefined,
        name: '',
        address: '',
        department: '',
        phone: undefined,
        nit: '',
        type: 'PU',
      },
      rules: {
        name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        department: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        address: [],
        phone: [],
        nit: []
      },
      INSTITUTION_TYPE_OPTIONS
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
    resetTemp() {
      this.temp = {
        id: undefined,
        department: 'CH',
        type: 'PU',
        name: '',
        address: '',
        phone: undefined,
        nit: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
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
              service: 'createInstitution',
              query: institutions.createInstitution(),
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
              if (this.isSecondaryForm) {
                const new_institution = response.data['create_institution']['institution']
                this.$emit('createInstitutionId', new_institution.id)
              }

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
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
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
              service: 'updateInstitution',
              query: institutions.updateInstitution(),
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
    }
  }
}
</script>
