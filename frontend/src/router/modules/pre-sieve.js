/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const preSieveRouter = {
  path: '/pre-sieves',
  component: Layout,
  redirect: '/pre-sieves/exams',
  name: 'preSieves',
  meta: {
    title: 'preSieves',
    icon: 'nested',
    roles: ['index_exam']
  },
  children: [
    {
      path: 'exams',
      component: () => import('@/views/pre-sieve/exams'),
      name: 'exams',
      meta: { title: 'preSieves', roles: ['index_exam'] }
    }
  ]
}
export default preSieveRouter
