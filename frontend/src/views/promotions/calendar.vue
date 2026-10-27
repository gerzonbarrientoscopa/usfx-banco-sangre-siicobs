<template>
  <div class="app-container">
    <div class="text-center">
      <el-radio v-model="stateView" border label="1">Por Eventos</el-radio>
      <el-radio v-model="stateView" border label="2">Por Fechas de Nacimientos</el-radio>
      <el-radio v-model="stateView" border label="3">Por Donantes Habilitados</el-radio>
    </div>
    <br>
    <full-calendar
      ref="calendar"
      :config="config"
      :events="events"
      :selectable="true"
      @event-selected="eventSelected"
      @view-render="changeView"
      @day-click="dayClick"
    />
    <el-dialog :before-close="handleCloseForm" :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" destroy-on-close width="60%">
      <div class="createPost-container">
        <el-form
          ref="dataForm"
          :model="temp"
          :rules="rules"
          label-position="right"
          label-width="250px"
          style="width: 100%;"
        >
          <el-form-item :label="$t('models.event.name')" prop="name">
            <el-input v-model="temp.name" @input.native="setUpperCase(temp, 'name', $event)" />
          </el-form-item>

          <el-form-item :label="$t('models.event.init_at')" prop="init_at">
            <el-date-picker
              v-model="temp.init_at"
              :placeholder="$t('models.event.init_at')"
              format="dd-MM-yyyy HH:mm"
              type="datetime"
            />
          </el-form-item>

          <el-form-item :label="$t('models.event.end_at')" prop="end_at">
            <el-date-picker
              v-model="temp.end_at"
              :placeholder="$t('models.event.end_at')"
              format="dd-MM-yyyy HH:mm"
              type="datetime"
            />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">{{ $t('cancel') }}</el-button>
          <el-button @click="dialogStatus==='create'?createData():updateData()">{{ $t('confirm') }}
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { FullCalendar } from 'vue-full-calendar'
import moment from 'moment'
import events from '@/query/event'
import { graphqlRequest } from '@/api/graphql'

export default {
  name: 'Calendar',
  components: { FullCalendar },
  directives: {},
  filters: {},
  data() {
    return {
      props: {
        events: {
          type: Array,
          required: true
        }
      },
      config: {
        defaultView: 'month',
        weekends: true,
        days: false,
        locale: 'es',
        navLinks: true,
        eventLimit: true,
        eventColor: '#42b983',
        displayEventTime: true,
        displayEventEnd: true,
        timezone: 'local',
        header: {
          left: 'today month listMonth',
          center: 'title',
          right: 'prevYear,prev,next,nextYear'
        },
        buttonText: {
          today: 'Hoy',
          month: 'Mes',
          week: 'Semana',
          day: 'Dia',
          list: 'Lista del Mes'
        }
      },
      editable: false,
      events: [],
      tableKey: 0,
      list: null,
      total: null,
      listLoading: true,
      listQuery: { page: 1, limit: 100, search: undefined, ordering: '-init_at' },
      temp: { id: undefined, name: '', init_at: '', end_at: '', is_active: true },
      rules: {
        name: [{ required: true, message: this.$t('is_required'), trigger: 'blur' }],
        init_at: [{ required: true, message: this.$t('is_required'), trigger: 'change' }],
        end_at: [{ required: true, message: this.$t('is_required'), trigger: 'change' }]
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: { update: 'Editando Evento', create: 'Creando Evento' },
      downloadLoading: false,
      dialogShowVisible: false,
      selectDate: '',
      selectDateEnd: '',
      selectDateMonth: '',
      stateView: '1'
    }
  },
  watch: {
    stateView: function() {
      this.getList()
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      const dateNow = this.selectDateMonth
      const filter = this.stateView
      graphqlRequest(
        {
          from: this.$route.name,
          service: 'list_for_calendar',
          query: events.list_for_calendar(),
          variables: { filter: filter, date: dateNow }
        }
      ).then(response => {
        const data = response.data
        this.events = data.calendar_events
        this.listLoading = false
      })
    },
    next() {
      this.$refs.calendar.fireMethod('next')
    },
    changeView(view) {
      this.selectDateMonth = moment(new Date((view.end + view.start) / 2)).format('YYYY/MM')
      this.getList()
    },
    dayClick: function(date) {
      if (this.stateView === '1') {
        this.selectDate = moment(date.format(), 'YYYY-MM-DD').add(8, 'hours').toISOString()
        this.selectDateEnd = moment(date.format(), 'YYYY-MM-DD').add(18, 'hours').toISOString()
        this.handleCreate()
      }
    },
    eventSelected: function(event) {
      if (this.stateView === '1') {
        let end = event.end
        if (end) {
          end = event.end.format()
        }
        const tempData = {
          id: event.id,
          name: event.title,
          init_at: event.start.format(),
          end_at: end,
          is_active: event.is_active
        }
        this.handleUpdate(tempData)
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.init_at = new Date(tempData.init_at).toISOString()
          tempData.end_at = new Date(tempData.end_at).toISOString()
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'createEvent',
              query: events.createEvent(),
              variables: tempData
            }
          ).then(response => {
            if (response.errors) {
              this.$notify({
                title: 'Estado',
                message: response.errors[0].message,
                type: 'error',
                duration: 2000
              })
            } else {
              this.dialogFormVisible = false
              this.getList()
              this.$notify({
                title: 'Estado',
                message: 'Registro creado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.init_at = new Date(tempData.init_at).toISOString()
          tempData.end_at = new Date(tempData.end_at).toISOString()
          graphqlRequest(
            {
              from: this.$route.name,
              service: 'updateEvent',
              query: events.updateEvent(),
              variables: tempData
            }
          ).then(response => {
            if (response.errors) {
              this.$notify({
                title: 'Estado',
                message: response.errors[0].message,
                type: 'error',
                duration: 2000
              })
            } else {
              this.dialogFormVisible = false
              this.getList()
              this.$notify({
                title: 'Estado',
                message: 'Se ha actualizado',
                type: 'success',
                duration: 2000
              })
            }
          })
        }
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        init_at: this.selectDate,
        end_at: this.selectDateEnd,
        is_active: true
      }
    },
    handleCloseForm() {
      this.dialogFormVisible = false
      this.getList()
    }
  }
}
</script>
