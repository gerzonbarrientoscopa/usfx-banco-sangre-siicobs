import { getDonationEligibility, getLastDonationDate } from '@/utils/donationEligibility'

describe('eligibilidad de donación', () => {
  it('detecta la primera donación cuando no hay extracciones previas', () => {
    expect(getLastDonationDate({ donations: [] })).toBeNull()
    expect(getDonationEligibility(null, '2026-11-09')).toEqual({
      type: 'success',
      message: 'El donante puede donar, es su primera donación.'
    })
  })

  it('usa la fecha de extracción completada más reciente', () => {
    const donor = {
      donations: [
        { register_at: '2026-01-10', extraction: { id: 1 }},
        { register_at: '2026-08-15', extraction: null },
        { register_at: '2026-05-20', extraction: { id: 2 }}
      ]
    }
    expect(getLastDonationDate(donor)).toBe('2026-05-20')
  })

  it('obtiene la última fecha de donación desde register_at', () => {
    const donor = {
      last_effective_donation_at: '2026-10-10',
      last_donation_at: '2026-10-11',
      donations: [
        { register_at: '2026-01-10', extraction: { id: 1 }},
        { register_at: '2026-08-08', extraction: { id: 2 }}
      ]
    }

    expect(getLastDonationDate(donor)).toBe('2026-08-08')
    expect(getLastDonationDate({ last_donation_at: '2026-10-11' })).toBeNull()
  })

  it('no usa la fecha previa almacenada en un donante precargado', () => {
    expect(getLastDonationDate({
      last_donation_at: '2026-08-08',
      donations: []
    })).toBeNull()
  })

  it('avisa para una última donación hace menos de tres meses', () => {
    expect(getDonationEligibility('2026-10-10', '2026-11-09').type).toBe('error')
  })

  it('avisa si han transcurrido exactamente tres meses', () => {
    expect(getDonationEligibility('2026-08-09', '2026-11-09')).toEqual({
      type: 'error',
      message: 'El donante no puede donar ya que aún no pasaron 3 meses desde la última donación.'
    })
  })

  it('permite donar cuando ya pasaron más de tres meses', () => {
    expect(getDonationEligibility('2026-08-08', '2026-11-09')).toEqual({
      type: 'success',
      message: 'El donante puede donar, ya transcurrieron más de 3 meses desde su última donación.'
    })
  })

  it('no muestra el aviso de tres meses ante una fecha futura inválida', () => {
    expect(getDonationEligibility('2026-11-10', '2026-11-09')).toBeNull()
  })
})
