/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const sieveRouter = {
  path: '/sieves',
  component: Layout,
  redirect: '/sieves/physical-analysis',
  name: 'sieves',
  meta: {
    title: 'sieves',
    icon: 'list',
    roles: ['index_physicalanalysis', 'index_clinicalhistoryanswer']
  },
  children: [
    {
      path: 'physical-analysis',
      component: () => import('@/views/sieve/physicalAnalisis'),
      name: 'physical-analysis',
      meta: { title: 'physicalAnalysis', roles: ['index_physicalanalysis'] }
    },
    {
      path: 'clinical-histories',
      component: () => import('@/views/sieve/clinicalHistory'),
      name: 'clinical-histories',
      meta: { title: 'clinicalHistories', roles: ['index_clinicalhistoryanswer'] }
    }
  ]
}
export default sieveRouter
