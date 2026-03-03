// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Sunholo Blog',
  tagline: 'Insights on GenAI, agents, and cognitive design',
  favicon: 'img/favicon.ico',

  url: 'https://www.sunholo.com',
  baseUrl: '/blog/',

  organizationName: 'sunholo-data',
  projectName: 'blog',

  onBrokenLinks: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: false,
        blog: {
          routeBasePath: '/',
          showReadingTime: true,
          blogSidebarCount: 'ALL',
          blogSidebarTitle: 'All posts',
        },
        googleTagManager: {
          containerId: 'GTM-WLQZQF2P',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/eclipse1.png',
      navbar: {
        title: 'Sunholo Blog',
        logo: {
          alt: 'Sunholo Logo',
          src: 'img/eclipse1.png',
        },
        items: [
          {
            href: 'https://dev.sunholo.com',
            label: 'Dev Portal',
            position: 'left',
          },
          {
            href: 'https://www.sunholo.com',
            label: 'Multivac',
            position: 'right',
          },
          {
            href: 'https://github.com/sunholo-data/sunholo-py',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Resources',
            items: [
              {
                label: 'Dev Portal',
                href: 'https://dev.sunholo.com',
              },
              {
                label: 'Presentations',
                href: 'https://www.sunholo.com/presentations/',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'https://discord.gg/RANn65Rh9a',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/sunholo-data/sunholo-py',
              },
            ],
          },
        ],
        copyright: `Copyright \u00A9 ${new Date().getFullYear()} Holosun ApS`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
