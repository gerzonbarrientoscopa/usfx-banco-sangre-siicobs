<template>
  <div>
    <el-row :gutter="20">
      <el-col :md="24">
        <div class="grid-content">
          <div class="createPost-container">
            <el-row :gutter="20">
              <el-col :md="16">
                <el-form v-if="aux" ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="200px" style="width: 100%;">
                  <el-form-item label="Registros">
                    <font-awesome-icon icon="syringe" />
                    <el-tooltip>
                      <div slot="content">Fecha de Extracción</div>
                      <span>{{ aux.fragmentation.extraction.register_at|toHumanDate }}</span>
                    </el-tooltip>
                    &nbsp;-&nbsp;
                    <font-awesome-icon icon="tachometer-alt" />
                    <el-tooltip>
                      <div slot="content">Fecha de Expiración</div>
                      <span>{{ aux.expiration_date|toHumanDate }}</span>
                    </el-tooltip>
                  </el-form-item>
                  <el-form-item v-if="aux.type_irregular_antibody" label="Tipo de Anticuerpo Irregular">
                    <b>{{ aux.type_irregular_antibody.name }}</b>
                  </el-form-item>
                  <el-form-item :label="$t('models.release.register_at')" prop="register_at">
                    <el-date-picker
                      v-model="temp.register_at"
                      :placeholder="$t('models.release.register_at')"
                      format="dd-MM-yyyy"
                      type="date"
                      value-format="yyyy-MM-dd"
                    />
                  </el-form-item>
                  <el-form-item :label="$t('models.release.employee')" prop="employee_id">
                    <el-select
                      v-model="temp.employee_id"
                      :placeholder="$t('please_select')"
                      automatic-dropdown
                      class="filter-item"
                      filterable
                    >
                      <el-option
                        v-for="item in employees"
                        :key="item.id"
                        :label="item.first_name +' '+ item.middle_name +' '+ item.last_name "
                        :value="item.id"
                      />
                    </el-select>
                  </el-form-item>
                  <el-form-item :label="$t('models.release.observations')" prop="observations">
                    <el-input v-model="temp.observations" :rows="3" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
                  </el-form-item>
                  <el-form-item>
                    <el-button v-if="isEdit" @click="updateData()">
                      {{ 'Modificar' }}
                    </el-button>
                    <el-button
                      v-if="!isEdit && aux.fragmentation.extraction.donation.immunoserology && aux.fragmentation.extraction.donation.immunoserology"
                      type="primary"
                      @click="createData()"
                    >
                      {{ 'Guardar' }}
                    </el-button>
                  </el-form-item>
                </el-form>
              </el-col>
              <el-col :md="8">
                <laboratory-show v-if="!isEdit" :aux="aux" />
              </el-col>
            </el-row>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import releases from '@/query/release'
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import LaboratoryShow from '../LaboratoryShow.vue'

export default {
  name: 'ReleaseForm',
  components: { LaboratoryShow },
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isEdit: false,
      aux: undefined,
      temp: { id: undefined, reason: '', observations: '', register_at: undefined, employee_id: undefined },
      rules: {
        register_at: [{ required: true, message: this.$t('is_required') }],
        employee_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: []
      }
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
    disabledDateRegisterAt(time) {
      if (this.row && this.row.release) {
        return time.getTime() < new Date(this.row.itemfragmentation.fragmentation.extraction.register_at)
      } else {
        return time.getTime() < new Date(this.row.fragmentation.extraction.register_at)
      }
    },
    determineAction() {
      if (this.row && this.row.release) {
        const tempData = Object.assign({}, this.row)
        tempData.typehemocomponent = tempData.itemfragmentation.typehemocomponent
        tempData.fragmentation = tempData.itemfragmentation.fragmentation
        tempData.fragmentation.extraction = tempData.itemfragmentation.fragmentation
        tempData.donor_code = tempData.itemfragmentation.donor_code
        this.aux = tempData
        this.handleUpdate()
      } else {
        this.aux = Object.assign({}, this.row)
        this.handleCreate()
      }
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        register_at: new Date(),
        reason: '',
        observations: '',
        employee_id: undefined
      }
    },
    handleCreate() {
      this.isEdit = false
      this.resetTemp()
      const tempData = Object.assign({}, this.temp)
      tempData.register_at = moment().format('YYYY-MM-DD')
      tempData.employee_id = this.employee_id
      tempData.itemfragmentation_id = this.row.id
      this.temp = tempData
      this.aux = this.row

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      if (this.temp.register_at < this.aux.fragmentation.extraction.register_at) {
        this.$notify({
          title: 'Mensaje',
          message: 'No puede liberar en esta fecha, la liberacion se hace despues de la fecha de extraccion',
          type: 'error',
          duration: 2000
        })
        return
      }
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          tempData.register_at = moment(this.temp.register_at).format('YYYY-MM-DD')
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createRelease',
              query: releases.createRelease(),
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
    handleUpdate() {
      this.isEdit = true
      this.temp.id = this.aux.id
      this.temp.employee_id = this.aux.employee.id
      this.temp.register_at = this.aux.register_at
      this.temp.observations = this.aux.observations
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.itemfragmentation = tempData.itemfragmentation_id
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateRelease',
              query: releases.updateRelease(),
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

<style scoped>
  .orange {
    color: orangered;
  }
</style>
