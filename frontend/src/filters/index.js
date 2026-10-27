// import parseTime, formatTime and set to filter
/* Calendar Filter */
import moment from 'moment'
import {INSTITUTION_TYPE_OPTIONS} from "@/utils/const";

export { parseTime, formatTime } from '@/utils'

/**
 * Show plural label if time is plural number
 * @param {number} time
 * @param {string} label
 * @return {string}
 */
function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

/**
 * @param {number} time
 */
export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/**
 * Number formatting
 * like 10000 => 10k
 * @param {number} num
 * @param {number} digits
 */
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

/**
 * 10000 => "10,000"
 * @param {number} num
 */
export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

/**
 * Upper case first char
 * @param {String} string
 */
export function uppercaseFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

moment.locale('es')

export function toHumanDatetime(date) {
  return moment(date).format('DD-MM-YYYY - HH:mm')
}

export function toHumanDate(date) {
  return moment(date).format('DD-MM-YYYY')
}

export function toHumanDateMonthLetter(date) {
  return moment(date).format('DD MMMM YYYY')
}

export function toHumanDateLetter(date) {
  return moment(date).format('dddd, DD [de] MMMM [del] YYYY')
}

export function toHumanTime(date) {
  return moment(date).format('HH:mm')
}

/* donor complete name */

export function fullName(donor) {
  if (donor) {
    return donor.first_name + ' ' + donor.middle_name + ' ' + donor.last_name
  }
  return ''
}
/* donor complete name */
export function fullNameEmployee(employee) {
  if (employee) {
    return employee.first_name + ' ' + employee.middle_name + ' ' + employee.last_name
  }
  return ''
}

export function fullNameWithInstitution(medical) {
  if (medical) {
    return medical.first_name + ' ' + medical.middle_name + ' ' + medical.last_name + ' - ' + medical.institution.name
  }
  return ''
}

export function donorCodeFullName(donor) {
  if (donor) {
    return donor.code + ' ' + donor.first_name + ' ' + donor.middle_name + ' ' + donor.last_name
  }
  return ''
}

export function bloodGroupToHtml(value) {
  if (value) {
    switch (value) {
      case 'A':
        return 'A<sub>1</sub></span>'
      case 'A1':
        return 'A<sub>1</sub></span>'
      case 'A2':
        return 'A<sub>2</sub></span>'
      case 'AB':
        return 'A<sub>1</sub>B</span>'
      case 'A1B':
        return 'A<sub>1</sub>B</span>'
      case 'A2B':
        return 'A<sub>2</sub>B</span>'
      default:
        return value
    }
  }
  return ''
}

export function bloodGroupSignedToHtml(value) {
  const sign = value.substring(value.length - 1)
  value = value.substring(0, value.length - 1)
  let x = ''
  if (value) {
    switch (value) {
      case 'A':
        x = 'A<sub>1</sub></span>'
        break
      case 'A1':
        x = 'A<sub>1</sub></span>'
        break
      case 'A2':
        x = 'A<sub>2</sub></span>'
        break
      case 'AB':
        x = 'A<sub>1</sub>B</span>'
        break
      case 'A1B':
        x = 'A<sub>1</sub>B</span>'
        break
      case 'A2B':
        x = 'A<sub>2</sub>B</span>'
        break
      default:
        return value + sign
    }
  }
  return x + sign
}

export function yesNoFilter(value) {
  return value ? 'SI' : 'NO'
}

function genericFilter(options, key) {
  const states = options.reduce((acc, cur) => {
    acc[cur.key] = cur.display_name
    return acc
  }, {})

  return states[key]
}

export function institutionTypeValue(key) {
  return genericFilter(INSTITUTION_TYPE_OPTIONS, key)
}
