<template>
  <div v-if="donation" class="app-container">
    <donation-show :donation="donation" :is-editing-parent="false" @refreshDonation="donationGet" />
  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import donations from '@/query/donation'
import DonationShow from './DonationShow'

export default {
  name: 'DonationEdit',
  components: { DonationShow },
  directives: {},
  filters: {},
  props: {},
  data() {
    return {
      tableKey: 0,
      list: null,
      loading: false,
      visible: false,
      donation: undefined,
      listReasonQuery: { page: 1, limit: 50, offset: 0, search: '', ordering: 'name' }
    }
  },
  computed: {},
  created() {
    this.donationGet()
  },
  methods: {
    donationGet() {
      this.loading = true
      const id = this.$route.params && this.$route.params.id

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'getDonation',
          query: donations.getDonationEdit(id)
        }
      ).then(response => {
        this.donation = response.data.donation
        this.setTagsViewTitle()
        this.loading = false
      })
    },
    setTagsViewTitle() {
      const title = 'Donación'
      const route = Object.assign({}, this.$route, { title: `${title}-${this.donation.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
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
  .font-120 {
    font-size: 120px;
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
      height:140px;
    }
  }
  .box-card {
    width: 100%;
    height: auto;
  }
</style>
