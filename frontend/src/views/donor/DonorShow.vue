<template>
  <div v-if="donor_id" class="app-container">
    <donor-detail :donor-id="donor_id" />
  </div>
</template>

<script>
import DonorDetail from './DonorDetail'

export default {
  name: 'ProvisionList',
  components: { DonorDetail },
  directives: {},
  filters: {},
  data() {
    return {
      donor_id: undefined
    }
  },
  computed: {},
  created() {
    this.getDonor()
  },
  updated() {
  },
  methods: {
    getDonor() {
      this.donor_id = +(this.$route.params && this.$route.params.id)
    }
  }
}
</script>
