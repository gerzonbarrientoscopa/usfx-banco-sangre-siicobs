<template>
  <div v-if="row">
    <el-row :gutter="20">
      <el-col :md="24">
        <div class="grid-content">
          <div class="createPost-container">
            <el-row :gutter="20">
              <el-col :md="16">
                <el-form ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="200px" style="width: 100%;">
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
                    <el-button :disabled="Object.keys(row).length===0" @click="createData('only')">
                      {{ 'Liberar' }}
                    </el-button>
                    <el-button :disabled="Object.keys(row).length===0" @click="createData('print')">
                      {{ 'Liberar e Imprimir' }}
                    </el-button>
                  </el-form-item>
                </el-form>
              </el-col>
              <el-col :md="24">
                <el-table :key="tableKey" :data="massiveReleases" border fit highlight-current-row style="width: 100%;">
                  <el-table-column :label="$t('models.storage.register_at')" align="center" fixed prop="register_at" width="100px">
                    <template slot-scope="scope">
                      <span>{{ scope.row.fragmentation.extraction.register_at | toHumanDate }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.code')" align="center" prop="donor_code" width="100px">
                    <template slot-scope="scope">
                      <strong v-if="scope.row.fragmentation">{{ scope.row.donor_code }}</strong>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.name')" width="400">
                    <template slot-scope="scope">
                      {{ scope.row.typehemocomponent.name }}
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.weight')" align="right" width="100">
                    <template slot-scope="scope">
                      <span>{{ scope.row.weight }} ml.</span>
                    </template>
                  </el-table-column>
                  <el-table-column
                    :label="$t('models.storage.expiration_date')"
                    align="center"
                    prop="expiration_date"
                    width="190px"
                  >
                    <template slot-scope="scope">
                      <span>{{ scope.row.expiration_date | toHumanDate }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.pre_discard')" align="center" width="155px">
                    <template slot-scope="scope">
                      <span>{{ scope.row.typediscard ? 'SI' : 'NO' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.status')" align="center" width="200px">
                    <template slot-scope="scope">
                      <el-tag
                        v-if="(!scope.row.fragmentation.extraction.donation.immunohematology && !scope.row.fragmentation.extraction.donation.immunoserology)"
                      >FALTA LABORATORIO
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('models.storage.employee')" align="center" width="250px">
                    <template slot-scope="scope">
                      <span>{{ scope.row.fragmentation.employee | fullName }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column :label="$t('actions')" align="center" class-name="small-padding" fixed="right" width="270">
                    <template slot-scope="scope">
                      <el-button size="mini" @click="handleRemove(scope.$index, scope.row)">
                        {{ $t('quit') }}
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-dialog :append-to-body="true" :title="titleReport" :visible.sync="reportDialogVisible" center top="10px" width="100%">
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { graphqlRequest } from '@/api/graphql'
import moment from 'moment'
import releases from '@/query/release'
import { reportMassiveBloodBags } from '@/api/release'
import ReportDialog from '../report-dialog/ReportDialog'

export default {
  name: 'ReleaseMassiveForm',
  components: { ReportDialog },
  filters: {
    reactiveStatus(data) {
      if (data === 'R') {
        return 'REACTIVO'
      } else if (data === 'P') {
        return 'PENDIENTE'
      } else {
        return 'NO REACTIVO'
      }
    },
    crossesStatus(data) {
      if (data === '-') {
        return 'NEGATIVO'
      } else {
        return data
      }
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
      pdf: null,
      reportDialogVisible: false,
      reportDialogLoading: false,
      titleReport: 'Reporte de Bolsas de Sangre',
      tableKey: 0,
      isEdit: false,
      massiveReleases: [],
      massiveReleaseIds: [],
      temp: {
        id: undefined,
        observations: '',
        register_at: undefined,
        employee_id: undefined,
        register_id: undefined,
        hemocomponents: []
      },
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
    handleRemove(index, row) {
      this.$emit('list-added', row)
      delete this.massiveReleases.splice(index, 1)
    },
    disabledDateRegisterAt(time) {
      let min = this.massiveReleases[0]
      for (const mr of this.massiveReleases) {
        if (min.fragmentation.extraction.register_at < mr.fragmentation.extraction.register_at) {
          min = mr
        }
      }
      return time.getTime() < new Date(min.fragmentation.extraction.register_at)
    },
    determineAction() {
      this.handleCreate()
    },
    resetTemp() {
      this.temp = {
        register_at: new Date(),
        employee_id: undefined,
        register_id: undefined,
        hemocomponents: [],
        observations: ''
      }
    },
    handleCreate() {
      this.isEdit = false
      this.resetTemp()

      const tempData = Object.assign({}, this.temp)
      tempData.register_at = moment().format('YYYY-MM-DD')
      tempData.employee_id = this.employee_id
      this.temp = tempData
      const arrayMassiveReleases = []
      const passRow = this.row

      Object.keys(this.row).forEach(function(key) {
        arrayMassiveReleases.push(passRow[key])
      })
      this.massiveReleases = arrayMassiveReleases

      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    verifyRegisterAt() {
      for (const mr of this.massiveReleases) {
        if (this.temp.register_at < mr.fragmentation.extraction.register_at) {
          this.$notify({
            title: 'Mensaje',
            message: 'No puede liberar en esta fecha, la liberacion se hace despues de la fecha de extraccion',
            type: 'error',
            duration: 2000
          })
          return
        }
      }
    },
    createData(method) {
      this.verifyRegisterAt()
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.employee_id = this.temp.employee_id
          tempData.register_id = this.employee_id
          tempData.register_at = moment(this.temp.register_at).format('YYYY-MM-DD')
          tempData.hemocomponents = this.formattedItems(this.massiveReleases)
          // TODO remplazar esto por una mutacion massiva

          if (tempData.hemocomponents === '') {
            this.$notify({
              title: 'Estado',
              message: 'No existen hemocomponentes',
              type: 'error',
              duration: 2000
            })
            return
          }
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createMassiveRelease',
              query: releases.createMassiveRelease(),
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
              if (method === 'print') {
                this.handlePrintMassiveBloodBags()
              }
              this.$emit('dialogStatus', false)
              this.$emit('clearItems', true)
              this.resetTemp()
              this.$notify({
                title: 'Estado',
                message: 'Registros creados',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    formattedItems(list) {
      const newListMenus = []
      list.forEach(function(obj, idx) {
        newListMenus.push({ id: obj.id })
      })
      return newListMenus
    },
    getItemFragmentationIds(massiveReleases) {
      const ids = []
      Object.keys(massiveReleases).forEach(function(key) {
        ids.push(massiveReleases[key].id)
      })
      return ids.join(',')
    },
    handlePrintMassiveBloodBags() {
      this.reportDialogVisible = true
      this.reportDialogLoading = true
      this.titleReport = 'Etiqueta de Bolsas'
      const data = this.getItemFragmentationIds(this.massiveReleases)
      reportMassiveBloodBags(data).then(
        response => {
          this.pdf = response
          this.reportDialogLoading = false
        }
      )
    }
  }
}
</script>

