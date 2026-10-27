<template>
  <div class="app-container">
    <el-form
      ref="dataFormRejected"
      :model="rejected"
      :rules="rulesRejected"
      label-position="left"
      label-width="120px"
      style="width: 100%;"
    >
      <el-form-item :label="$t('models.rejected.type')" prop="type">
        <el-radio-group v-model="rejected.type" @change="getReason(rejected.type)">
          <el-radio-button v-for="item in typeReasonOptions" :key="item.key" :label="item.key">
            {{ item.display_name }}
          </el-radio-button>
        </el-radio-group>
      </el-form-item>

      <el-form-item :label="$t('models.rejected.reason')" prop="reason_id">
        <el-select
          v-model="rejected.reason_id"
          :loading="loadingReasons"
          :placeholder="$t('please_select')"
          automatic-dropdown
          class="filter-item"
          filterable
        >
          <el-option
            v-for="(item, index) in filteredReasons"
            :key="index"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('models.rejected.observations')" prop="observations">
        <el-input v-model="rejected.observations" :rows="4" type="textarea" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button  @click="isEdit ? updateRejectedData() : createRejectedData()">{{ $t('rejected') }}</el-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import rejecteds from '@/query/rejected'
import moment from 'moment'

const typeReasonOptions = [
  { key: 'TE', display_name: 'TEMPORAL' },
  { key: 'PE', display_name: 'PERMANENTE' }
]

const typeReasonKeyValue = typeReasonOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'RejectedForm',
  directives: {},
  filters: {
    typeReasonFilter(type) {
      return typeReasonKeyValue[type]
    }
  },
  props: {
    row: {
      type: Object,
      default: null
    },
    reasons: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      isEdit: false,
      donation: null,
      dialogFormVisible: false,
      typeReasonOptions,
      action: '',
      filteredReasons: [],
      loadingReasons: null,
      rejected_status: false,
      rejected: {
        id: undefined,
        reason_id: '',
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: '',
        register_at: ''
      },
      rulesRejected: {
        type: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        reason_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        observations: [{ required: false, message: this.$t('is_required'), trigger: 'blur' }]
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
    },
    'rejected.type': function(value) {
      if (value !== undefined || value !== null) {
        this.getReason(value)
      }
    }
  },
  mounted() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row.rejected) {
        this.handleUpdate()
      } else {
        this.handleCreate()
      }
    },
    handleCreate() {
      this.isEdit = false
      this.resetRejected()
      this.$nextTick(() => {
        this.$refs['dataFormRejected'].clearValidate()
      })
    },
    handleUpdate() {
      this.isEdit = true
      const tempData = Object.assign({}, this.row.rejected)
      tempData.type = tempData.reason.type
      tempData.reason_id = tempData.reason.id
      this.rejected = tempData
      this.$nextTick(() => {
        this.$refs['dataFormRejected'].clearValidate()
      })
    },
    getReason(id) {
      this.filteredReasons = this.reasons.filter(function(item) {
        return item.type === id
      })
    },
    resetRejected() {
      this.rejected = {
        id: undefined,
        reason_id: '',
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: '',
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    createRejectedData() {
      this.$refs['dataFormRejected'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.rejected)
          tempData.reason_id = this.rejected.reason_id
          tempData.donation_id = this.row.id
          tempData.employee_id = this.employee_id
          tempData.resource = 'ClinicalHistory'
          tempData.resource_id = this.row.clinicalhistoryanswer.id
          tempData.register_at = moment(this.row.register_at).format('YYYY-MM-DD')
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createRejected',
              query: rejecteds.createRejected(),
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
              this.$emit('dialogState', false)
              this.resetTemp()
              this.$notify({
                title: 'Estado',
                message: 'Registro de Diferimiento creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    updateRejectedData() {
      this.$refs['dataFormRejected'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.rejected)
          tempData.reason_id = this.rejected.reason_id
          tempData.donation_id = this.row.id
          tempData.employee_id = this.employee_id
          tempData.resource = 'ClinicalHistory'
          tempData.resource_id = this.row.clinicalhistoryanswer.id
          tempData.register_at = moment(this.row.register_at).format('YYYY-MM-DD')
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateRejected',
              query: rejecteds.updateRejected(),
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
              this.$emit('dialogState', false)
              this.$notify({
                title: 'Estado',
                message: 'Registro de Diferimiento actualizado',
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
<style>

</style>

