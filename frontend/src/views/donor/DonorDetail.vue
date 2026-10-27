<template>
  <div v-if="donor">
    <el-row>
      <el-col :md="14">
        <el-card class="box-card" shadow="never">
          <div slot="header" class="clearfix">
            <span class="title">{{ donor | fullName }}</span>
          </div>
          <div>
            <el-row :gutter="20">
              <el-col :span="24">
                <table class="example">
                  <tbody>
                    <tr>
                      <td class="text">Código</td>
                      <td class="text bold">{{ donor.code }}</td>
                    </tr>
                    <tr>
                      <td class="text">Códigos Secundarios</td>
                      <td class="text bold">{{ donor.code_other }}</td>
                    </tr>
                    <tr>
                      <td class="text">Fecha de Nacimiento</td>
                      <td class="text bold">{{ donor.birth_date | toHumanDate }}</td>
                    </tr>
                    <tr>
                      <td class="text">CI</td>
                      <td class="text bold">{{ donor.ci }} {{ donor.ci_extension }}</td>
                    </tr>
                    <tr>
                      <td class="text">Edad</td>
                      <td class="text bold">{{ donor.age }}</td>
                    </tr>
                    <tr>
                      <td class="text">Género</td>
                      <td class="text bold">{{ donor.gender }}</td>
                    </tr>
                    <tr>
                      <td class="text">Domicilio/Residencia</td>
                      <td class="text bold">{{ donor.residence }}</td>
                    </tr>
                    <tr>
                      <td class="text">Zona</td>
                      <td class="text bold">{{ donor.zone }}</td>
                    </tr>
                    <tr>
                      <td class="text">Departamento</td>
                      <td class="text bold">{{ donor.department | departmentOptionsFilter }}</td>
                    </tr>
                  </tbody>
                </table>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
      <el-col :md="5">
        <div v-if="$route.name === 'donationDetail'">
          <el-row :gutter="20" style="width: 100%;">
            <el-col :md="24">
              <el-tooltip
                v-if="donation && donation.exam && donation.exam.blood_group"
                content="PRE-TAMIZAJE"
                effect="dark"
                placement="bottom"
              >
                <span class="exam-text">
                  {{ getBloodGroupTextExam(donation.exam.blood_group) }}
                </span>
              </el-tooltip>
            </el-col>
            <el-col :md="24" class="text-center">
              <span v-if="donor && donor.group_abo" :inner-html.prop="(donor.group_abo + donor.factor_rh.substring(donor.factor_rh.length-1)) | bloodGroupSignedToHtml" class="fs-96" />
              <br>
              <span v-if="donor && donor.group_abo" style="font-size: 20px;">
                {{ getBloodGroupTextImmunohematology(donor.group_abo, donor.factor_rh) }}
              </span>
            </el-col>
          </el-row>
        </div>
        <div v-if="$route.name !== 'donationDetail'">
          <div v-if="bloodGroupInfo" class="text-center">
            <span v-if="bloodGroupInfo.type" :inner-html.prop="bloodGroupInfo.type | bloodGroupSignedToHtml" class="fs-96" />
            <span v-if="!bloodGroupInfo.type" class="">NO HAY REGISTRO DE GRUPO SANGUINEO</span><br>
            <span v-if="bloodGroupInfo.factor">{{ bloodGroupInfo.factor }}</span>
          </div>
        </div>
      </el-col>
      <el-col :md="5" class="text-center">
        <img
          v-if="donor.image === '' && donor.gender === 'M'"
          alt=""
          class="image"
          src="@/assets/global_images/hombre.png"
          width="200px"
        >
        <img
          v-if="donor.image === '' && donor.gender === 'F'"
          alt=""
          class="image"
          src="@/assets/global_images/mujer.png"
          width="200px"
        >
        <img
          v-if="donor.image && donor.image !== ''"
          :src="'https://siicobs-assets.s3.amazonaws.com/media/'+ donor.image"
          alt=""
          class="image"
          height="200px"
          width="200px"
        >
        <div style="padding: 14px;">
          <el-button
            v-if="checkPermission(['change_donor'])"
            icon="el-icon-upload"
            round
            type="primary"
            @click="handleOpenWebCam()"
          >Actualizar Fotografia
          </el-button>
        </div>
      </el-col>
    </el-row>
    <el-row style="margin-top: 8px">
      <el-col :md="24">
        <el-table
          :key="tableKey"
          :data="donor.donations"
          border
          fit
          highlight-current-row
          style="width: 100%;"
        >
          <el-table-column :label="$t('models.donation.register_at')" align="center" fixed width="150px">
            <template slot-scope="scope">
              <span>{{ scope.row.register_at | toHumanDate }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.donation.type_donation')" align="left" width="200px">
            <template slot-scope="scope">
              <span>{{ scope.row.type_donation | typeDonationFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.donation.place')" align="center" width="155px">
            <template slot-scope="scope">
              <span v-if="scope.row.place">{{ scope.row.place.name }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.donation.age_donor')" align="center" width="100px">
            <template slot-scope="scope">
              <span>{{ scope.row.age_donor }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.donation.last_donation_at')" align="center" width="200px">
            <template slot-scope="scope">
              <span>{{ scope.row.last_donation_at }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('models.donation.employee')" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.employee | fullName }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-dialog
      :visible.sync="webCamDialogVisible"
      center
      title="CAMARA"
      top="10px"
      width="80%"
      @close="closeCamera"
      @opened="resetCamera()"
    >
      <camera ref="Camera" :row="donorId" @dialogStatus="handleCloseWebCam" />
    </el-dialog>
  </div>
</template>

<script>
import checkPermission from '@/utils/permission'
import Camera from '../registry/components/camera'
import donors from '@/query/donor'
import { graphqlRequest } from '@/api/graphql'
import { DEPARTMENT_OPTIONS } from '@/utils/const'

const typeDonationOptions = [
  { key: 'VA', display_name: 'VOLUNTARIA ALTRUISTA' },
  { key: 'RS', display_name: 'REPOSICION SOLIDARIA' },
  { key: 'RE', display_name: 'REPOSICION EXIGIDA' },
  { key: 'DA', display_name: 'DONACION AUTOLOGA' }
]

const statusOptions = [
  { key: 'NU', display_name: 'NUEVO' },
  { key: 'EP', display_name: 'EN PROCESO' },
  { key: 'CO', display_name: 'COMPLETADO' },
  { key: 'RE', display_name: 'DIFERIDO' }
]

const typeDonationKeyValue = typeDonationOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

const departmentOptionsKeyValue = DEPARTMENT_OPTIONS.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'DonorDetail',
  components: { Camera },
  directives: {},
  filters: {
    filterBloodGroup(type) {
      const sign = type.substring(type.length - 1)
      const value = type.substring(0, type.length - 1)
      if (sign === '-') {
        return 'Rh (' + value + ') ' + 'NEGATIVO'
      } else {
        return 'Rh (' + value + ') ' + 'POSITIVO'
      }
    },
    departmentOptionsFilter(type) {
      return departmentOptionsKeyValue[type]
    },
    typeDonationFilter(type) {
      return typeDonationKeyValue[type]
    }
  },
  props: {
    donorId: {
      type: Number,
      default: null
    },
    donation: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      webCamDialogVisible: false,
      loading: false,
      departmentOptions: DEPARTMENT_OPTIONS,
      visible: false,
      donor: null,
      donations: null,
      statusOptions,
      bloodGroupInfo: null
    }
  },
  computed: {},
  created() {
    this.getDonor()
  },
  updated() {
  },
  methods: {
    checkPermission,
    // start methods camera component
    resetCamera() {
      this.$refs.Camera.reset()
    },
    closeCamera() {
      this.$refs.Camera.closeWebCam()
    },
    handleOpenWebCam() {
      this.webCamDialogVisible = true
    },
    handleCloseWebCam() {
      this.webCamDialogVisible = false
      this.getDonor()
    },
    // end methods camera component

    getDonor() {
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'donors',
          query: donors.showDonor(this.donorId)
        }
      ).then(response => {
        const data = response.data
        this.donor = data.donor
        this.setTagsViewTitle()
        this.getBloodGroup()
      })
    },
    setTagsViewTitle() {
      if (this.donor && this.$route.name !== 'donationDetail') {
        const title = 'Donante'
        const route = Object.assign({}, this.$route, { title: `${title}-${this.donor.code}` })
        this.$store.dispatch('tagsView/updateVisitedView', route)
      }
    },
    getStatus(row) {
      var type = 'info'
      if (row.exam) {
        type = ''
      }
      if (row.rejected) {
        type = 'danger'
      }
      return type
    },
    getBloodGroup() {
      this.bloodGroupInfo = { type: null, factor: null }
      if (this.donor.group_abo !== null && this.donor.factor_rh !== null) {
        this.bloodGroupInfo = {
          type: this.donor.group_abo + this.donor.factor_rh.substring(this.donor.factor_rh.length - 1),
          factor: this.getBloodGroupTextImmunohematology(this.donor.group_abo, this.donor.factor_rh)
        }
      } else if (this.donor && this.donor.donations) {
        let lastDonation = null
        for (const donation of this.donor.donations) {
          lastDonation = donation.exam && donation.exam.blood_group ? donation : lastDonation
        }
        if (lastDonation) {
          this.bloodGroupInfo = {
            type: lastDonation.exam.blood_group,
            factor: this.getBloodGroupTextExam(lastDonation.exam.blood_group)
          }
        }
      }
    },
    getBloodGroupTextImmunohematology(group_abo, factor_rh) {
      switch (factor_rh) {
        case 'RH+':
          return 'Rh (' + group_abo + ') ' + 'POSITIVO'
        case 'RHD':
          return 'Rh (' + group_abo + ') ' + 'DEBIL'
        case 'RH-':
          return 'Rh (' + group_abo + ') ' + 'NEGATIVO'
      }
    },
    getBloodGroupTextExam(blood_group) {
      if (blood_group) {
        const sign = blood_group.substring(blood_group.length - 1)
        const group_abo = blood_group.substring(0, blood_group.length - 1)
        if (sign === '-') {
          return 'Rh (' + group_abo + ') ' + 'NEGATIVO'
        } else {
          return 'Rh (' + group_abo + ') ' + 'POSITIVO'
        }
      }
      return ''
    }
  }
}
</script>
<style type="text/scss">
  .title {
    font-size: 15px;
    vertical-align: middle;
    text-transform: uppercase;
    font-weight: bold;
  }

  .bold {
    font-weight: bold;
  }

  .step {
    height: 300px;
    margin-top: 20px;
  }

  .text {
    padding-top: 5px;
    font-size: 12px;
  }

  .code {
    float: left;
    font-size: 15px;
    margin-right: 20px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }

  .mt-40 {
    margin-top: 40px;
  }

  .box-card {
    width: 100%;

    span {
      vertical-align: middle;
    }

    img {
      height: 140px;
    }
  }

  .box-card {
    width: 100%;
    height: auto;
  }

  table.example {
    border-collapse: collapse;
    width: 100%;
    background-color: #fff;
    font-size: 14px;
    margin-bottom: 45px;
    line-height: 1.5em
  }

  table.example strong {
    font-weight: 400
  }

  table.example td,
  table.example th {
    border-bottom: 1px solid #dcdfe6;
    padding: 0;
    max-width: 250px
  }

  table.example th {
    text-align: left;
    white-space: nowrap;
    color: #909399;
    font-weight: 400
  }

  table.example td {
    color: #606266
  }

  table.example td:first-child,
  table.example th:first-child {
    padding-left: 10px
  }

  @media (max-width: 768px) {
    table.example {
      overflow: auto;
      display: block
    }
  }
  .exam-text{
    font-size: 10px;
    float: right;
    margin-bottom: 20px
  }
  .fs-96 {
    font-size: 96px;
  }
</style>
