/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const configurationRouter = {
  path: '/configurations',
  component: Layout,
  redirect: '/configurations/employees',
  name: 'configuration',
  meta: {
    title: 'configurations',
    icon: 'example',
    roles: ['index_rejected', 'index_employee', 'index_institution', 'index_clinicalhistoryquestion', 'index_refreshment', 'index_menu',
      'index_settingphisical', 'index_reason', 'index_typeadversereaction', 'index_typesolution', 'index_otherindication']
  },
  children: [
    {
      path: 'rejecteds',
      component: () => import('@/views/configurations/rejected'),
      name: 'rejecteds',
      meta: {
        title: 'rejecteds', roles: ['index_rejected']
      }
    },
    {
      path: 'personals',
      component: () => import('@/views/configurations/employee'),
      name: 'personals',
      meta: { title: 'staffs', roles: ['index_employee'] }
    },
    {
      path: 'institutions',
      component: () => import('@/views/institutions/InstitutionList'),
      name: 'institutions',
      meta: { title: 'institutions', roles: ['index_institution'] }
    },
    {
      path: 'menus',
      component: () => import('@/views/configurations/menus/MenuList'),
      name: 'menus',
      meta: { title: 'menus', roles: ['index_menu'] }
    },
    {
      path: 'type-adverse-reactions',
      component: () => import('@/views/configurations/typeAdverseReaction'),
      name: 'typeAdverseReaction',
      meta: { title: 'typeAdverseReaction', roles: ['index_typeadversereaction'] }
    },
  ]
}
export default configurationRouter
