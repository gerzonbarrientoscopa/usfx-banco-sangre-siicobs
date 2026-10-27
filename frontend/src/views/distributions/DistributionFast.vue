<template>
  <div class="app-container">
    <distribution-form ref="Form" @distribution="getDistribution" />
  </div>
</template>

<script>
import DistributionForm from './DistributionForm'

export default {
  name: 'DistributionFast',
  directives: {},
  components: {
    DistributionForm
  },
  data() {
    return {}
  },
  created() {},
  methods: {
    getDistribution($event) {
      this.distribution = $event
    }
  }
}
</script>
