<template>
  <div v-if="event" class="app-container">
    <el-row style="margin-top: 8px">
      <el-col :md="24">
        <el-tabs stretch type="card" @tab-click="determineTab">
          <el-tab-pane>
            <span slot="label"><font-awesome-icon icon="user" /> Detalle</span>
            <event-detail :row="event" @refreshEvent="eventGet" />
            <hr>
          </el-tab-pane>
          <el-tab-pane>
            <span slot="label"><font-awesome-icon icon="vials" /> Donaciones sin Evento</span>
            <event-add-donations :row="event" @refreshEvent="eventGet" />
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { graphqlRequest } from '@/api/graphql'
import events from '@/query/event'
import EventDetail from './tab/EventDetail'
import EventAddDonations from './tab/EventAddDonations'

export default {
  name: 'EventEdit',
  components: { EventDetail, EventAddDonations },
  directives: {},
  filters: {},
  props: {},
  data() {
    return {
      tableKey: 0,
      list: null,
      loading: false,
      visible: false,
      event: undefined
    }
  },
  computed: {},
  created() {
    this.eventGet()
  },
  methods: {
    determineTab(ev) {
      this.eventGet()
    },
    eventGet() {
      this.loading = true
      const id = this.$route.params && this.$route.params.id

      graphqlRequest(
        {
          from: this.$route.name,
          service: 'getEvent',
          query: events.getEvent(id)
        }
      ).then(response => {
        this.event = response.data.event
        this.setTagsViewTitle()
        this.loading = false
      })
    },
    setTagsViewTitle() {
      const title = 'Evento'
      const route = Object.assign({}, this.$route, { title: `${title}-${this.event.id}` })
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
