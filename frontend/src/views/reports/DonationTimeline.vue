<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :md="12">
        <el-form ref="dataForm" :model="temp" :rules="rules" label-position="right" label-width="170px" style="width: 100%;">
          <div class="grid-content">
            <el-form-item :label="$t('models.extraction.donation')" prop="donation_id">
              <el-select
                v-model="temp.donation_id"
                :loading="loadingDonation"
                :placeholder="$t('please_select')"
                :remote-method="remoteMethodDonation"
                automatic-dropdown
                class="filter-item"
                filterable
                remote
                @change="getDonation($event)"
              >
                <el-option
                  v-for="item in donations"
                  :key="item.id"
                  :label="item.donor | donorCodeFullName"
                  :value="item.id"
                >
                  <span style="float: left"><strong>{{ item.donor.code }}</strong> {{ item.donor | fullName }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.register_at| toHumanDateMonthLetter }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-form>
      </el-col>
      <el-col :md="12">
        <el-button :disabled="pdf===null" @click="handleDownload()">{{ $t('export') }} PDF</el-button>
      </el-col>
    </el-row>
    <div class="container">
      <iframe v-if="pdf && !loading" :src="pdf" allowfullscreen frameborder="0" />
      <div v-if="loading" class="text-center">
        <i class="el-icon-loading" style="font-size: 100px" />
      </div>
    </div>

  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import { mapGetters } from 'vuex'
import { reportDonationTimeline } from '@/api/report'
import moment from 'moment'
import donations from '@/query/donation'
import { graphqlRequest } from '@/api/graphql'

export default {
  name: 'DonationTimeline',
  data() {
    return {
      listDonationQuery: { page: 1, limit: 20, offset: 0, search: '', ordering: '-register_at, donor__code' },
      loadingDonation: false,
      loading: false,
      donations: null,
      pdf: null,
      response: null,
      temp: {
        id: undefined,
        donation_id: undefined,
        donation: null
      },
      rules: {
        donation_id: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
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
    this.getListDonations()
  },
  methods: {
    checkPermission,
    getDonation(event) {
      for (const donation of this.donations) {
        if (donation.id === event) {
          this.temp.donation = donation
          this.createReport()
        }
      }
    },
    getListDonations() {
      this.loadingDonation = true
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donations',
          query: donations.select(this.listDonationQuery)
        }
      ).then(response => {
        const data = response.data
        this.donations = data.donations.results
        this.loadingDonation = false
      })
    },
    remoteMethodDonation(query) {
      if (query !== '') {
        this.listDonationQuery.search = query
      } else {
        this.listDonationQuery.search = ''
      }
      this.getListDonations()
    },
    createReport() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.$notify({
            title: 'Generando Reporte',
            message: 'Se esta generando el reporte espere un momento !!!',
            type: 'info',
            duration: 4000
          })

          const tempData = Object.assign({}, this.temp)
          this.loading = true
          reportDonationTimeline(tempData).then(response => {
            this.response = response
            const blob = new Blob([response], { type: 'application/pdf' })
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            this.pdf = link
            this.loading = false
          })
        }
      })
    },
    handleDownload() {
      const tempData = Object.assign({}, this.temp)
      const today = moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
      const filename = 'Linea de tiempo ' + tempData.donation.donor.code + ' ' + tempData.donation.register_at + ' ' + today
      const url = window.URL.createObjectURL(new Blob([this.response]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename + '.pdf')
      document.body.appendChild(link)
      link.click()
    }
  }
}
</script>

<style scoped>
  iframe {
    height:calc(100vh - 125px);
    width:calc(100vw - 50px);
    box-sizing: border-box;
  }
</style>
