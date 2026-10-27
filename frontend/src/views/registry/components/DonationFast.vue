<template>
  <div class="app-container">
    <el-button v-if="active !== 0" :class="background_color + ' button-left'" type="success" @click="prev">
      Anterior
    </el-button>
    <el-button v-if="active !== 2" :class="background_color + ' button-right'" type="success" @click="next">
      Siguiente
    </el-button>
    <el-steps :active="active" :class="text_color" :finish-status="text_color" align-center>
      <el-step :description="descriptionSteps[0]" title="Receptor" />
      <el-step :description="descriptionSteps[1]" title="Donante" />
      <el-step :description="descriptionSteps[2]" title="Confirmar datos" />
    </el-steps>
    <small v-if="active=== 0" style="color: #bd3739">
      Sí es donacion voluntaria saltar este paso, presione el boton siguiente
    </small>
    <patient-list v-if="active === 0" @selectedReceptor="selectedReceptor" />
    <donor-list v-if="active === 1" @selectedDonor="selectedDonor" />
    <donation-form v-if="active === 2" :is-editing-parent="true" @selectedDonor="selectedDonor" />

    <el-dialog
      title="Elija tipo de Donación"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
      :close-delay="false"
      :show-close="false"
      :visible.sync="isCovid19DialogVisible"
      width="60%"
      center
      destroy-on-close
    >
      <donation-select-type @handleSelectedDonationType="handleChoiceCreateRoute" />
    </el-dialog>
  </div>
</template>

<script>
import PatientList from '../../receptor/ReceptorList'
import Cookies from 'js-cookie'
import DonorList from '../../donor/DonorList'
import DonationForm from '../DonationForm'
import DonationSelectType from '@/views/donation/DonationSelectType'
import { TYPE_PROCESS } from '@/utils/const'

export default {
  name: 'DonationFast',
  directives: {},
  components: {
    DonationSelectType,
    DonationForm,
    DonorList,
    PatientList
  },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      active: 0,
      descriptionSteps: { 0: 'Donación Voluntaria', 1: '', 2: '' },
      background_color: '',
      text_color: '',
      isCovid19DialogVisible: false

    }
  },
  created() {
    Cookies.set('donationDonor', undefined)
    Cookies.set('donationReceptor', undefined)
    this.isCovid19DialogVisible = true
  },
  methods: {
    handleChoiceCreateRoute() {
      const type_process = Cookies.get('type_process')
      switch (type_process) {
        case TYPE_PROCESS.NORMAL:
          this.background_color = ''
          this.text_color = 'success'
          break
        case TYPE_PROCESS.COVID19:
          this.background_color = 'bg-covid-19'
          this.text_color = 'finish'
          break
        case TYPE_PROCESS.NORMAL_APHERESIS:
          this.background_color = 'bg-apheresis'
          this.text_color = 'success'
          break
        case TYPE_PROCESS.COVID19_APHERESIS:
          this.background_color = 'bg-apheresis'
          this.text_color = 'finish'
          break
      }
      this.isCovid19DialogVisible = false
    },
    selectedReceptor() {
      const receptor = JSON.parse(Cookies.get('donationReceptor'))
      const tempData = Object.assign({}, this.descriptionSteps)
      tempData[0] = receptor.first_name + ' ' + receptor.middle_name + ' ' + receptor.last_name
      this.descriptionSteps = tempData
    },
    selectedDonor() {
      const donationDonor = Cookies.get('donationDonor')
      const donor = JSON.parse(donationDonor)
      const tempData = Object.assign({}, this.descriptionSteps)
      tempData[1] = donor.first_name + ' ' + donor.middle_name + ' ' + donor.last_name
      this.descriptionSteps = tempData
    },
    next() {
      const isSelectedDonor = Cookies.get('donationDonor')
      if (this.active === 1 && isSelectedDonor === 'undefined') {
        this.$notify({
          title: 'Falta Donante ',
          message: 'Selecciona un donante de la lista',
          type: 'warning',
          duration: 2000
        })
      } else {
        this.active++
      }
    },
    prev() {
      this.active--
    }
  }
}
</script>

<style type="text/scss">
  .button-right{
    margin-top: 12px; float: right;
  }
  .button-left{
    margin-top: 12px; float: left;
  }
</style>
