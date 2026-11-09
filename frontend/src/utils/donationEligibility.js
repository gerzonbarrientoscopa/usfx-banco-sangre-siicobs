import moment from 'moment'

export function getLastDonationDate(donor) {
  const donations = donor && Array.isArray(donor.donations) ? donor.donations : []
  const validDates = donations
    .filter(donation => donation && donation.extraction && donation.register_at)
    .map(donation => donation.register_at)
    .map(date => moment(String(date).substring(0, 10), 'YYYY-MM-DD', true))
    .filter(date => date.isValid())
    .sort((a, b) => b.valueOf() - a.valueOf())

  return validDates.length ? validDates[0].format('YYYY-MM-DD') : null
}

export function getDonationEligibility(lastDonationAt, donationAt) {
  if (!lastDonationAt) {
    return {
      type: 'success',
      message: 'El donante puede donar, es su primera donación.'
    }
  }

  const lastDonation = moment(String(lastDonationAt).substring(0, 10), 'YYYY-MM-DD', true)
  const currentDonation = moment(
    String(donationAt || moment().format('YYYY-MM-DD')).substring(0, 10),
    'YYYY-MM-DD',
    true
  )

  if (!lastDonation.isValid() || !currentDonation.isValid()) {
    return null
  }

  if (lastDonation.isAfter(currentDonation, 'day')) {
    return null
  }

  if (currentDonation.isAfter(lastDonation.clone().add(3, 'months'), 'day')) {
    return {
      type: 'success',
      message: 'El donante puede donar, ya transcurrieron más de 3 meses desde su última donación.'
    }
  }

  return {
    type: 'error',
    message: 'El donante no puede donar ya que aún no pasaron 3 meses desde la última donación.'
  }
}
