/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const distributionRouter = {
  path: '/distributions',
  component: Layout,
  redirect: '/distributions/distributions',
  name: 'area-distributions',
  meta: {
    title: 'distribution',
    icon: 'shopping',
    roles: ['index_distribution', 'index_patient']
  },
  children: [
    {
      path: 'medicals',
      component: () => import('@/views/medicals/MedicalList'),
      name: 'medicals',
      meta: { title: 'medical', roles: ['index_medical'] }
    },
    {
      path: 'patients',
      component: () => import('@/views/receptor/ReceptorList'),
      name: 'receptor',
      meta: { title: 'receptor', roles: ['index_patient'] }
    },
    {
      path: 'distributions',
      component: () => import('@/views/distributions/DistributionList'),
      name: 'distributions',
      meta: { title: 'distributions', roles: ['index_distribution'] }
    },
    {
      path: 'distribution-fast',
      component: () => import('@/views/distributions/DistributionFast'),
      name: 'distribution-fast',
      meta: { title: 'distribution', noCache: true, roles: ['index_distribution'] },
      hidden: true
    },
    {
      path: 'distributions/:id(\\d+)',
      component: () => import('@/views/distributions/DistributionForm'),
      name: 'distribution-edit',
      meta: { title: 'Detalle de Distribución', noCache: true, roles: ['view_distribution'] },
      hidden: true
    }
  ]
}
export default distributionRouter
