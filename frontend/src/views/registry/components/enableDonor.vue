<template>
  <div>
    <el-row :gutter="20">
      <el-col :md="24">
        <div class="grid-content">
          <div class="createPost-container">
            <el-form
              ref="dataForm"
              :rules="rules"
              :model="temp"
              label-position="right"
              label-width="200px"
              style="width: 100%;"
            >
              <el-form-item :label="$t('models.extraction.register_at')" prop="register_at">
                <el-date-picker
                  v-model="temp.register_at"
                  :placeholder="$t('models.extraction.register_at')"
                  type="date"
                  format="dd-MM-yyyy"
                  value-format="yyyy-MM-dd"
                />
              </el-form-item>
              <el-form-item :label="$t('models.enable-donor.reason')" prop="reason">
                <el-input v-model="temp.reason" :rows="4" type="textarea" @input.native="setUpperCase(temp, 'reason', $event)" />
              </el-form-item>
              <el-form-item>
                <el-button @click="createData()">
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
import moment from 'moment'
import donorHistories from '@/query/donorHistory'
import { graphqlRequest } from '@/api/graphql'

export default {
  name: 'EnableDonor',
  directives: {},
  filters: {},
  props: {
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      temp: { id: undefined },
      rules: {
        register_at: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        reason: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }]
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
    determineAction() {
      this.handleCreate()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        register_at: moment().format('YYYY-MM-DD')
      }
    },
    handleCreate() {
      this.resetTemp()
      const tempData = Object.assign({}, this.temp)
      tempData.donor_id = this.row.id
      this.temp = tempData
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.donor_id = this.row.id
          tempData.employee_id = this.employee_id
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createDonorHistory',
              query: donorHistories.createDonorHistory(),
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
                message: 'El Donante ha sido habilitado para realizar DONACIONES',
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

