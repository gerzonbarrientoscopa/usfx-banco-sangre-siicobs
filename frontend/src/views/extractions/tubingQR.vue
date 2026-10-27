<template>
  <div class="app-container">
    <el-form
      ref="dataqrForm"
      :model="qr"
      :rules="rulesqr"
      label-position="right"
      label-width="170px"
      style="width: 100%;"
    >
      <el-row :gutter="20">
        <el-col :md="24" :sm="24">
          <div class="grid-content">
            <template slot-scope="scope">
              <span>{{ scope.row.register_at | toHumanDatetime }}</span>
            </template>
            <el-form-item :label="$t('models.extraction.quantity')" prop="">
              <el-input-number v-model.number="qr.total" :max="5" :min="1" size="small" />
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="printQR()">{{ $t('confirm') }}</el-button>
    </span>

    <el-dialog
      :title="reportTitle"
      :visible.sync="reportDialogVisible"
      append-to-body
      center
      top="10px"
      width="100%"
    >
      <report-dialog v-if="!reportDialogLoading" :row="pdf" />
      <div v-if="reportDialogLoading" class="loading-report">
        <i class="el-icon-loading" style="font-size: 80px" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { printBCDonation } from '@/api/donation'
import ReportDialog from '../report-dialog/ReportDialog'

export default {
  name: 'TubingQR',
  components: { ReportDialog },
  props: {
    id: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      tableKey: 0,
      pdf: null,
      reportTitle: 'TUBOS DE ENSAYO',
      reportDialogVisible: false,
      reportDialogLoading: false,
      rulesqr: {
        total_: [{ required: true, trigger: 'blur', type: 'number', message: 'Debe ser número' }]
      },
      qr: {
        total: 1
      }
    }
  },
  mounted() {
    this.handlePrintQR(this.row)
  },
  methods: {
    resetQR() {
      this.qr = {
        total: 3
      }
    },
    handlePrintQR() {
      this.resetQR()
      this.$nextTick(() => {
        this.$refs['dataqrForm'].clearValidate()
      })
    },
    printQR() {
      this.$refs['dataqrForm'].validate((valid) => {
        if (valid) {
          this.reportDialogVisible = true
          this.reportDialogLoading = true
          printBCDonation(this.id, this.qr.total).then(
            (response) => {
              this.pdf = response
              this.reportDialogLoading = false
              this.resetQR()
            })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
