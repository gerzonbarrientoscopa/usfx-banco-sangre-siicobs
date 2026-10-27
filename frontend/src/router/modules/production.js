/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const warehouseRouter = {
  path: '/production',
  component: Layout,
  redirect: '/production/quarantine',
  name: 'area-production',
  meta: {
    title: 'production',
    icon: 'tab',
    roles: ['index_itemfragmentation', 'index_discard', 'index_release']
  },
  children: [
    /* {
      path: 'release-requests',
      component: () => import('@/views/production/releaseRequest'),
      name: 'releaseRequests',
      meta: { title: 'releaseRequests', roles: ['index_releaserequest'] }
    },*/
    {
      path: 'hemocomponents',
      component: () => import('@/views/production/hemocomponent/HemocomponentList'),
      name: 'hemocomponents',
      meta: { title: 'hemocomponents', roles: ['index_itemfragmentation'] }
    },
    {
      path: 'quarantine',
      component: () => import('@/views/production/storage'),
      name: 'quarantine',
      meta: { title: 'quarantine', roles: ['index_itemfragmentation'] }
    },
    {
      path: 'discards',
      component: () => import('@/views/production/discard/DiscardList'),
      name: 'discards',
      meta: { title: 'discards', roles: ['index_discard'] }
    },
    {
      path: 'releases',
      component: () => import('@/views/production/release/ReleaseList'),
      name: 'releases',
      meta: { title: 'releases', roles: ['index_release'] }
    }
  ]
}
export default warehouseRouter
