import DistributionForm from '@/views/distributions/DistributionForm.vue'

describe('DistributionForm', () => {
  it('closes the item dialog before showing the success notification', () => {
    const context = {
      temp: { register_at: '2026-11-11 12:00:00', itemfragmentations: [] },
      innerVisible: true,
      pendingItemNotification: null,
      $notify: jest.fn()
    }
    const hemocomponent = {
      expiration_date: '2026-11-12',
      typehemocomponent: { name: 'Glóbulos rojos' }
    }

    DistributionForm.methods.handleAddItem.call(context, hemocomponent)

    expect(context.innerVisible).toBe(false)
    expect(context.pendingItemNotification.type).toBe('success')
    expect(context.$notify).not.toHaveBeenCalled()

    DistributionForm.methods.notifyAddedItem.call(context)

    expect(context.pendingItemNotification).toBe(null)
    expect(context.$notify).toHaveBeenCalledWith(expect.objectContaining({
      message: 'Hemocomponente Agregado',
      type: 'success'
    }))
  })

  it('removes only the selected item when multiple items share a type', () => {
    const context = {
      temp: {
        itemfragmentations: [
          { itemfragmentation: { id: 11, typehemocomponent: { id: 3 } } },
          { itemfragmentation: { id: 12, typehemocomponent: { id: 3 } } },
          { itemfragmentation: { id: 13, typehemocomponent: { id: 7 } } }
        ]
      }
    }

    DistributionForm.methods.handleRemoveItem.call(context, 1)

    expect(context.temp.itemfragmentations.map(item => item.itemfragmentation.id)).toEqual([11, 13])
  })
})
