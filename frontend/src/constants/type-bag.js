export const TYPE_BAG_OPTIONS = [
  { key: 'SIMPLE', display_name: 'SIMPLE', bags_quantity: 1 },
  { key: 'DOBLE', display_name: 'DOBLE', bags_quantity: 2 },
  { key: 'TRIPLE', display_name: 'TRIPLE', bags_quantity: 3 },
  { key: 'CUADRUPLE', display_name: 'CUADRUPLE', bags_quantity: 4 },
  { key: 'CUADRUPLE_CON_FILTRO', display_name: 'CUADRUPLE CON FILTRO', bags_quantity: 4 },
  { key: 'SET_AFERESIS', display_name: 'SET DE AFERESIS', bags_quantity: 2 }
]

export const TYPE_BAG_LABELS = TYPE_BAG_OPTIONS.reduce((labels, option) => {
  labels[option.key] = option.display_name
  return labels
}, {})

export const BAGS_QUANTITY_BY_TYPE = TYPE_BAG_OPTIONS.reduce((quantities, option) => {
  quantities[option.key] = option.bags_quantity
  return quantities
}, {})
