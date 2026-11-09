/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const extractionRouter = {
  path: '/area-extraction',
  component: Layout,
  redirect: '/area-extraction/extractions',
  name: 'area-extraction',
  meta: {
    title: 'extraction',
    icon: 'star',
    roles: ['index_extraction', 'index_adversereaction', 'index_extractionrefreshment', 'index_patient']
  },
  children: [
    {
      path: 'extractions',
      component: () => import('@/views/extractions/extraction/ExtractionList'),
      name: 'extraction',
      meta: { title: 'extractions', roles: ['index_extraction'] }
    },
    {
      path: 'patients',
      component: () => import('@/views/receptor/ReceptorList'),
      name: 'extraction-receptor',
      meta: { title: 'receptor', roles: ['index_patient'] }
    },
    {
      path: 'extractions/:id',
      component: () => import('@/views/extractions/extraction/ExtractionEdit'),
      name: 'extractionDetail',
      meta: { title: 'extractionDetail', noCache: true, roles: ['view_extraction'] },
      hidden: true
    },
    {
      path: 'adverse-reactions',
      component: () => import('@/views/extractions/adverseReaction'),
      name: 'adverse-reactions',
      meta: { title: 'adverseReactions', roles: ['index_adversereaction'] }
    },
    {
      path: 'refreshments',
      component: () => import('@/views/extractions/refreshment/ExtractionRefreshmentList'),
      name: 'extraction-refreshment',
      meta: { title: 'refreshments', roles: ['index_extractionrefreshment'] }
    },
    {
      path: 'selfexclusion',
      component: () => import('@/views/extractions/SelfExclusion'),
      name: 'extraction-selfexclusion',
      meta: { title: 'selfexclusion', roles: ['index_selfexclusion'] }
    }
  ]
}
export default extractionRouter
