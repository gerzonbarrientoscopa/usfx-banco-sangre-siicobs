/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const reportRouter = {
  path: '/reports',
  component: Layout,
  redirect: '/reports/index',
  name: 'reports',
  meta: {
    title: 'reports',
    icon: 'example',
    roles: ['index_donation', 'index_fragmentation', 'index_distribution', 'index_immunoserology', 'index_fragmentation', 'index_item']
  },
  children: [
    {
      path: 'daily',
      name: 'reports-daily',
      component: () => import('@/views/reports/daily'), // Parent router-view
      meta: {
        title: 'reportDaily',
        roles: ['index_donation', 'index_fragmentation', 'index_distribution']
      },
      redirect: '/reports/daily',
      children: [
        {
          path: 'donation',
          component: () => import('@/views/reports/Daily/dailyDonation'),
          name: 'reports-daily-donation',
          meta: { title: 'reportDonation', roles: ['index_donation'] }
        },
        {
          path: 'fragmentation',
          component: () => import('@/views/reports/Daily/dailyFragmentation'),
          name: 'reports-daily-fragmentation',
          meta: { title: 'reportFragmentation', roles: ['index_fragmentation'] }
        },
        {
          path: 'immunohematology',
          component: () => import('@/views/reports/Daily/dailyImmunohematology'),
          name: 'reports-daily-immunohematology',
          meta: { title: 'reportImmunohematology', roles: ['index_immunohematology'] }
        },
        {
          path: 'immunoserology',
          component: () => import('@/views/reports/Daily/dailyImmunoserology'),
          name: 'reports-daily-immunoseroloy',
          meta: { title: 'reportImmunoserology', roles: ['index_immunoserology'] }
        },
        {
          path: 'production',
          component: () => import('@/views/reports/Daily/dailyProduction'),
          name: 'reports-daily-production',
          meta: { title: 'reportProduction', roles: ['index_fragmentation'] }
        },
        {
          path: 'distribution',
          component: () => import('@/views/reports/Daily/DailyDistribution'),
          name: 'reports-daily-distribution',
          meta: { title: 'reportDistribution', roles: ['index_distribution'] }
        },
        {
          path: 'release',
          component: () => import('@/views/reports/Daily/dailyRelease'),
          name: 'reports-daily-release',
          meta: { title: 'reportRelease', roles: ['index_release'] }
        },
        {
          path: 'discard',
          component: () => import('@/views/reports/Daily/DailyDiscard'),
          name: 'reports-daily-discard',
          meta: { title: 'reportDiscard', roles: ['index_discard'] }
        }
      ]
    },
    {
      path: 'general',
      name: 'reports-general',
      component: () => import('@/views/reports/general/general'), // Parent router-view
      meta: {
        title: 'reportGeneral',
        roles: ['index_donation', 'index_fragmentation', 'index_distribution']
      },
      redirect: '/reports/general',
      children: [
        {
          path: 'donation',
          component: () => import('@/views/reports/general/GeneralDonation'),
          name: 'reports-general-donation',
          meta: { title: 'reportDonation', roles: ['index_donation'] }
        },
        {
          path: 'immunohematology',
          component: () => import('@/views/reports/general/generalImmunohematology'),
          name: 'reports-general-immunohematology',
          meta: { title: 'reportImmunohematology', roles: ['index_immunohematology'] }
        },
        {
          path: 'immunoserology',
          component: () => import('@/views/reports/general/generalImmunoserology'),
          name: 'reports-general-immunoseroloy',
          meta: { title: 'reportImmunoserology', roles: ['index_immunoserology'] }
        },
        {
          path: 'release',
          component: () => import('@/views/reports/general/GeneralRelease'),
          name: 'reports-general-release',
          meta: { title: 'reportRelease', roles: ['index_release'] }
        },
        {
          path: 'discard',
          component: () => import('@/views/reports/general/GeneralDiscard'),
          name: 'reports-general-discard',
          meta: { title: 'reportDiscard', roles: ['index_discard'] }
        }
      ]
    },
    {
      path: 'distribution',
      name: 'reports-distribution',
      component: () => import('@/views/reports/general/general'), // Parent router-view
      meta: {
        title: 'reportDistribution',
        roles: ['index_distribution']
      },
      redirect: '/reports/general/GeneralDistribution',
      children: [
        {
          path: 'distribution',
          component: () => import('@/views/reports/Distribution/GeneralDistribution'),
          name: 'reports-general-distribution',
          meta: { title: 'reportGeneralDistribution', roles: ['index_distribution'] }
        },
        {
          path: 'hemocomponents',
          component: () => import('@/views/reports/Distribution/DistributionHemocomponents'),
          name: 'reports-distribution-hemocomponents',
          meta: { title: 'reportDistributionHemocomponents', roles: ['index_distributionitemfragmentation'] }
        }
      ]
    }
    /*
    {
      path: 'inmunoserologia',
      component: () => import('@/views/reports/immunoserology'),
      name: 'report-immunoserology',
      meta: { title: 'reportImmunoserology', roles: ['index_immunoserology'] }
    },
    {
      path: 'fragmentacion',
      component: () => import('@/views/reports/fragmentation'),
      name: 'report-fragmentation',
      meta: { title: 'reportFragmentation', roles: ['index_fragmentation'] }
    },
    {
      path: 'general',
      component: () => import('@/views/reports/index'),
      name: 'report-general',
      meta: { title: 'reportSieve', roles: ['index_donation'] }
    }
    /*
    {
      path: 'events',
      component: () => import('@/views/configurations/employee'),
      name: 'report-event',
      meta: { title: 'Grupo Etario y Sexo' }
    },
    {
      path: 'donation',
      component: () => import('@/views/configurations/employee'),
      name: 'report-donation',
      meta: { title: 'Donacion Voluntaria' }
    },
    {
      path: 'serology',
      component: () => import('@/views/configurations/employee'),
      name: 'report-serology',
      meta: { title: 'Tamizaje Serológico' }
    },
    {
      path: 'production',
      component: () => import('@/views/configurations/employee'),
      name: 'report-production',
      meta: { title: 'Prod. Sangre y Hem.' }
    },
    {
      path: 'discart',
      component: () => import('@/views/configurations/employee'),
      name: 'report-discart',
      meta: { title: 'Desc. Sangre y Hem.' }
    },
    {
      path: 'distribution',
      component: () => import('@/views/configurations/employee'),
      name: 'report-distribution',
      meta: { title: 'Distribucion Hem.' }
    },
    {
      path: 'cardex',
      component: () => import('@/views/configurations/employee'),
      name: 'report-cardex',
      meta: { title: 'Cardex' }
    },
    {
      path: 'evangelized',
      component: () => import('@/views/configurations/employee'),
      name: 'report-evangelized',
      meta: { title: 'Sens. de Donantes' }
    },
    {
      path: 'quality',
      component: () => import('@/views/configurations/employee'),
      name: 'report-quality',
      meta: { title: 'Indicador de Calidad' }
    }*/
  ]
}
export default reportRouter
