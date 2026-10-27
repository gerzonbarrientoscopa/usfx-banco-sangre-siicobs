/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const laboratoryRouter = {
  path: '/laboratories',
  component: Layout,
  redirect: '/laboratories/inmunohematologias',
  name: 'area-laboratories',
  meta: {
    title: 'laboratory',
    icon: 'list',
    roles: ['index_immunohematology', 'index_serologyprotocol', 'index_immunoserology']
  },
  children: [
    {
      path: 'inmunohematologias',
      component: () => import('@/views/laboratory/immunohematology/ImmunohematologyList'),
      name: 'inmunohematologias',
      meta: { title: 'inmunohematology', roles: ['index_immunohematology'] }
    },
    {
      path: 'serology-protocols',
      component: () => import('@/views/laboratory/serologyProtocol'),
      name: 'serology-protocols',
      meta: { title: 'serologyProtocol', roles: ['index_serologyprotocol'] }
    },
    {
      path: 'inmunoserologias',
      component: () => import('@/views/laboratory/immunoserology/ImmunoserologyList'),
      name: 'inmunoserologias',
      meta: { title: 'inmunoserology', roles: ['index_immunoserology'] }
    }
  ]
}
export default laboratoryRouter
