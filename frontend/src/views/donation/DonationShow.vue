<template>
  <donor-detail :donation="donation" :donor-id="donation.donor.id" />
</template>

<script>
import DonorDetail from '../donor/DonorDetail'

export default {
  name: 'DonationShow',
  components: { DonorDetail },
  directives: {},
  filters: {
  },
  props: {
    donation: {
      type: Object,
      default: null
    }
  },
  data() {
    return {}
  },
  computed: {},
  methods: {}
}
</script>
