<template>
  <div>
    <el-row :gutter="20">
      <el-col :md="24">
        <div class="grid-content">
          <div class="createPost-container">
            <el-row :gutter="20">
              <el-col :md="16">
                <el-form
                  v-if="aux"
                  ref="dataForm"
                  :model="temp"
                  :rules="rules"
                  label-position="right"
                  label-width="200px"
                  style="width: 100%;"
                >
                  <el-form-item v-if="aux.type_irregular_antibody" label="Tipo de Anticuerpo Irregular">
                    <b>{{ aux.type_irregular_antibody.name }}</b>
                  </el-form-item>
                  <el-form-item :label="$t('models.discard.register_at')" prop="register_at">
                    <el-date-picker
                      v-model="temp.register_at"
                      :placeholder="$t('models.discard.register_at')"
                      format="dd-MM-yyyy"
                      type="date"
                      value-format="yyyy-MM-dd"
                    />
                  </el-form-item>
                  <el-form-item :label="$t('models.discard.reason')" prop="reason">
                    <el-input v-model="temp.reason" :rows="3" type="textarea" @input.native="setUpperCase(temp, 'reason', $event)" />
                  </el-form-item>
                  <el-form-item :label="$t('models.order.observations')" prop="observations">
                    <el-input v-model="temp.observations" :rows="3" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
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
                  <el-form-item>
                    <el-button v-if="isEdit" @click="updateData()">
                      {{ $t('confirm') }}
                    </el-button>
                    <el-button v-if="!isEdit" @click="createData()">
                      {{ $t('confirm') }}
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
import discards from '@/query/discard'
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import LaboratoryShow from '../LaboratoryShow.vue'

export default {
  name: 'DiscardForm',
  components: { LaboratoryShow },
  filters: {},
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
        reason: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
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
      if (this.row && this.row.discard) {
        return time.getTime() < new Date(this.row.itemfragmentation.fragmentation.extraction.register_at)
      } else {
        return time.getTime() < new Date(this.row.fragmentation.extraction.register_at)
      }
    },
    determineAction() {
      if (this.row && this.row.discard) {
        const tempData = Object.assign({}, this.row)
        tempData.typehemocomponent = tempData.itemfragmentation.typehemocomponent
        tempData.fragmentation = tempData.itemfragmentation.fragmentation
        tempData.fragmentation.extraction = tempData.itemfragmentation.fragmentation
        tempData.donor_code = tempData.itemfragmentation.donor_code
        this.aux = tempData
        this.handleUpdate()
      } else {
        const tempData = Object.assign({}, this.row)
        this.aux = tempData
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
      if (this.row.typediscard) {
        tempData.reason = this.row.typediscard.name
      }
      tempData.itemfragmentation_id = this.row.id
      this.temp = tempData
      this.aux = this.row
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          tempData.register_at = moment(tempData.register_at).format('YYYY-MM-DD')
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createDiscard',
              query: discards.createDiscard(),
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
    handleUpdate() {
      this.isEdit = true
      this.temp.id = this.aux.id
      this.temp.employee_id = this.aux.employee.id
      this.temp.register_at = this.aux.register_at
      this.temp.observations = this.aux.observations
      this.temp.reason = this.aux.reason
      this.temp.itemfragmentation_id = this.aux.itemfragmentation.id
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateDiscard',
              query: discards.updateDiscard(),
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

