/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const fragmentationRouter = {
  path: '/fragmentations',
  component: Layout,
  redirect: '/fragmentations/fragmentations',
  name: 'area-fragmentations',
  meta: {
    title: 'fragmentation',
    icon: 'component',
    roles: ['index_fragmentation']
  },
  children: [
    {
      path: 'fragmentations',
      component: () => import('@/views/fragmentations/FragmentationList'),
      name: 'fragmentations',
      meta: { title: 'fragmentations', roles: ['index_fragmentation'] }
    }
  ]
}
export default fragmentationRouter
