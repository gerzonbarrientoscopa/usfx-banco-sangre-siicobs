import moment from 'moment'

export function defaultshorcouts() {
  return [{
    text: 'Mes Actual',
    onClick(picker) {
      const start = moment().startOf('month').format('YYYY-MM-DD')
      const end = moment().format('YYYY-MM-DD')
      picker.$emit('pick', [start, end])
    }
  }, {
    text: 'Mes Anterior',
    onClick(picker) {
      const start = moment().subtract(1, 'months').startOf('month').format('YYYY-MM-DD')
      const end = moment().subtract(1, 'months').endOf('month').format('YYYY-MM-DD')
      picker.$emit('pick', [start, end])
    }
  }, {
    text: 'Año Actual',
    onClick(picker) {
      var thisYear = (new Date()).getFullYear()
      var startDate = new Date('1/1/' + thisYear)
      const start = moment(startDate.valueOf()).format('YYYY-MM-DD')
      const end = moment().format('YYYY-MM-DD')
      picker.$emit('pick', [start, end])
    }
  }]
}

