/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const fragmentationRouter = {
  path: '/promotions',
  component: Layout,
  redirect: '/promotions/events',
  name: 'area-promotions',
  meta: {
    title: 'promotion',
    icon: 'component',
    roles: ['index_event', 'index_donor', 'index_donation']
  },
  children: [
    {
      path: 'calendar',
      component: () => import('@/views/promotions/calendar'),
      name: 'promotions-calendar',
      meta: { title: 'calendar', roles: ['index_event'] }
    },
    {
      path: 'events',
      component: () => import('@/views/events/EventList'),
      name: 'promotions-list-event',
      meta: { title: 'events', roles: ['index_event'] }
    },
    {
      path: 'events/:id(\\d+)',
      component: () => import('@/views/events/EventEdit'),
      name: 'eventDetail',
      meta: { title: 'Detalle de Evento', noCache: true, roles: ['view_event'] },
      hidden: true
    },
    {
      path: 'donors',
      component: () => import('@/views/donor/DonorList'),
      name: 'promotions-donor',
      meta: { title: 'donors', roles: ['index_donor'] }
    },
    {
      path: 'donations',
      component: () => import('@/views/registry/donation'),
      name: 'promotions-donation',
      meta: { title: 'donations', roles: ['index_donation'] }
    }
  ]
}
export default fragmentationRouter
