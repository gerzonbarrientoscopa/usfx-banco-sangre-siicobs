<template>
  <donation-fast :is-edit="false" />
</template>

<script>
import DonationFast from './components/DonationFast'

export default {
  name: 'CreateForm',
  components: { DonationFast }
}
</script>

