/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const registryRouter = {
  path: '/registry',
  component: Layout,
  redirect: '/registry/donations',
  name: 'registration',
  meta: {
    title: 'registrations',
    icon: 'peoples',
    roles: ['index_donor', 'view_donor', 'index_donation', 'view_donation']
  },
  children: [
    {
      path: 'donors',
      component: () => import('@/views/donor/DonorList'),
      name: 'donor',
      meta: { title: 'donors', roles: ['index_donor'] }
    },
    {
      path: 'donors/:id(\\d+)',
      component: () => import('@/views/donor/DonorShow'),
      name: 'donorDetail',
      meta: { title: 'Detalle de Donante', noCache: true, roles: ['view_donor'] },
      hidden: true
    },
    {
      path: 'donations',
      component: () => import('@/views/registry/donation'),
      name: 'ListDonation',
      meta: { title: 'donations', roles: ['index_donation'] }
    },
    {
      path: 'donations/:id',
      component: () => import('@/views/donation/DonationEdit'),
      name: 'donationDetail',
      meta: { title: 'donationDetail', noCache: true, roles: ['view_donation'] },
      hidden: true
    }
  ]
}
export default registryRouter
