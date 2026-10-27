<template>
  <div class="app-container">
    <el-form
      ref="dataForm"
      :model="temp"
      :rules="rules"
      label-position="left"
      label-width="120px"
      style="width: 100%;"
    >
      <el-form-item :label="$t('models.exam.donation')" prop="donation_id">
        <span class="text-text-turquoise" style="font-weight: bolder">
          {{ donor | donorCodeFullName }}
        </span>
      </el-form-item>
      <el-form-item :label="$t('models.rejected.type')" prop="type">
        <el-radio-group v-model="temp.type" @change="getReason(temp.type)">
          <el-radio-button v-for="item in typeReasonOptions" :key="item.key" :label="item.key">
            {{ item.display_name }}
          </el-radio-button>
        </el-radio-group>
      </el-form-item>

      <el-form-item :label="$t('models.rejected.reason')" prop="reason_id">
        <el-select
          v-model="temp.reason_id"
          :loading="loadingReasons"
          :placeholder="$t('please_select')"
          automatic-dropdown
          class="filter-item"
          filterable
        >
          <el-option
            v-for="item in filteredReasons"
            :key="item.id"
            :label="item.name "
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item :label="$t('models.rejected.observations')" prop="observations">
        <el-input v-model="temp.observations" :rows="4" type="textarea" @input.native="setUpperCase(temp, 'observations', $event)" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button  @click="isEdit ? updateData() : createData()">{{ $t('rejected') }}</el-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import rejecteds from '@/query/rejected'
import reasons from '@/query/reason'
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
  name: 'Rejected',
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
    }
  },
  data() {
    return {
      isEdit: false,
      dialogFormVisible: false,
      typeReasonOptions,
      reasons: null,
      action: '',
      filteredReasons: null,
      loadingReasons: null,
      donor: undefined,
      listQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'type,name' },
      temp: {
        id: undefined,
        reason_id: undefined,
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: ''
      },
      rules: {
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
  created() {
    this.determineAction()
  },
  methods: {
    determineAction() {
      if (this.row && this.row.temp) {
        this.handleUpdate()
      } else {
        if (this.row) {
          this.handleCreate()
        }
      }
    },
    getReason(id) {
      this.filteredReasons = this.reasons.filter(function(item) {
        return item.type === id
      })
    },
    getListReasons() {
      this.loadingReasons = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'reasons',
          query: reasons.list(this.listQuery)
        }
      ).then(response => {
        const data = response.data
        this.reasons = data.reasons.results
        this.loadingReasons = false
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        reason_id: undefined,
        donation: undefined,
        type: '',
        observations: '',
        employee: undefined,
        resource_id: undefined,
        resource: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.getListReasons()
      this.isEdit = false
      this.donor = this.row.donation.donor

      const tempData = Object.assign({}, this.temp)
      tempData.donation_id = this.row.donation.id
      tempData.employee_id = this.employee_id
      tempData.resource_id = this.row.resource_id
      tempData.resource = this.row.resource
      this.temp = tempData

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.register_at = moment().format('YYYY-MM-DD')
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
    handleUpdate() {
      this.getListReasons()
      this.isEdit = true
      this.temp = this.row.temp.donation.rejected
      this.temp.type = this.row.temp.donation.rejected.reason.type
      if (this.reasons) {
        this.getReason(this.temp.type)
      }
      this.temp.reason_id = this.row.temp.donation.rejected.reason.id
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.rejected)
          tempData.reason_id = this.rejected.reason_id
          tempData.employee_id = this.employee_id
          tempData.register_at = moment().format('YYYY-MM-DD')
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

